from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
# from PyQt5.QtGui import QLine

from src.debug import *
from src.components.workspace.nodes import Nodes

from typing import List, Dict, Optional
from pathlib import Path
import os


def row(widget_a, widget_b):
	section = QHBoxLayout()
	section.addWidget(widget_a)
	section.addWidget(widget_b)
	return section


class NodeMenu(QTreeWidget):
	START_POS = [500, 200]
	DIFF = (30, 10)  # move in what direction
	MAX_DIFF = 5  # maximum amount of times before reset the counter

	def __init__(self, view: QGraphicsView, menu_data: Dict[str, List[Nodes]], parent=None):
		super().__init__(parent=parent)
		self.view = view
		self.inst_pos = NodeMenu.START_POS.copy()  # node instantiate position
		self.counter = 0  # counting for # of times the user added the node; for the diff. node pos

		self.nodes = {}  # node title to node class reference mapping
		self.items: List[QTreeWidgetItem] = []
		for cat in menu_data:
			self.items.append(QTreeWidgetItem(self, [cat]))
			self.items[-1].addChildren([
				QTreeWidgetItem([nds.title])
				for nds in menu_data[cat]
			])
			for nds in menu_data[cat]: self.nodes[nds.title] = nds

		self.setHeaderHidden(True)
		self.addTopLevelItems(self.items)

		self.itemActivated.connect( lambda itm, col: self.addModel(self.nodes.get(itm.text(col))) )

	def addModel(self, nd_cls: Optional[Nodes]):
		# there should only be one model that have a unique name thus it should have only one item in the list
		# and each item in the list must be model class meaning it has the method create()

		if nd_cls is not None:
			self.view.scene().addItem(nd_cls.create(self.view, self.inst_pos))

			if self.counter > self.MAX_DIFF:
				print(NodeMenu.START_POS)
				self.inst_pos = NodeMenu.START_POS.copy()
				self.counter = 0
			self.inst_pos[0] += self.DIFF[0]
			self.inst_pos[1] += self.DIFF[1]
			self.counter += 1


class InputDialog(QPushButton):
	inputSelected = pyqtSignal(str)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.txt = ""

		self.clicked.connect(lambda checked: self.on_click())

	def on_click(self):
		self.wind = QMainWindow()
		self.wind.setWindowTitle("Input Dialogue")
		self.wind.setGeometry(200, 300, 300, 100)  # todo: GLOBAL POSITION; may not position it correctly
		self.wind.setWindowModality(Qt.ApplicationModal)

		self.inp_dialog = QInputDialog()
		self.inp_dialog.setLabelText("Input your model's name: ")

		self.inp_dialog.textValueSelected.connect(lambda txt: self.set_txt(txt))
		self.inp_dialog.finished.connect(lambda code: self.wind.close())

		self.wind.setMenuWidget(self.inp_dialog)
		self.wind.show()

	def set_txt(self, s: str):
		self.txt = s
		self.inputSelected.emit(s)


class PrjPathDialog(QDialog):
	BACK = ".."

	accepted = pyqtSignal(str, str)  # accept(path, project name)
	canceled = pyqtSignal()  # cancel

	def __init__(self, parent=None, default="C:/Users/"):
		self.USERNAME = os.getlogin()
		self.dir = default+self.USERNAME

		super().__init__(parent=parent)
		self.icon = QFileIconProvider().icon(QFileIconProvider.Folder)
		self.dirs = QListWidget()
		self.dirs.itemActivated.connect(lambda itm: self.set_dir(itm.text()))
		self.dirs.itemClicked.connect(lambda itm: self.dirs.setCurrentItem(itm))

		b_cancel = QPushButton("Cancel")
		b_accept = QPushButton("Accept")
		b_cancel.clicked.connect(lambda checked: self.canceled.emit())

		self.i_path = QLineEdit()
		self.i_path.returnPressed.connect(lambda: self.set_dir(self.i_path.text()))

		i_name = QLineEdit()

		b_accept.clicked.connect(lambda checked: self.accepted.emit(self.i_path.text(), i_name.text()))

		inp = QFormLayout()
		inp.addRow(QLabel("Path: "), self.i_path)
		inp.addRow(QLabel("Name"), i_name)

		submit = QHBoxLayout()
		submit.addStretch(1)
		submit.addWidget(b_cancel)
		submit.addWidget(b_accept)

		central = QVBoxLayout()
		central.addWidget(self.dirs, 5)
		central.addLayout(inp, 1)
		central.addLayout(submit, 1)

		self.setLayout(central)
		self.set_dir(None)

	def set_dir(self, selected: Optional[str]):
		if selected is not None:
			if selected == PrjPathDialog.BACK:
				self.dir = str(Path(self.dir).parent)
			else:
				self.dir = os.path.join(self.dir, selected)

		if os.path.exists(self.dir):
			self.dirs.clear()
			self.dirs.addItem(QListWidgetItem(self.icon, PrjPathDialog.BACK))
			for folder in os.listdir(self.dir):
				if os.path.isdir(os.path.join(self.dir, folder)):
					self.dirs.addItem(QListWidgetItem(self.icon, folder))
		else:
			self.dir = str(Path(self.dir).parent)
			ErrorBox(**ErrorBox.E011).exec()
		self.i_path.setText(self.dir)


class NewProject(QPushButton):  # todo: a mess of code; revisit for some aesthetic & maintenance issue
	inputSelected = pyqtSignal(str, str)  # inputSelected(path, name)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.name: Optional[str] = None
		self.path: Optional[str] = None

		self.clicked.connect(lambda checked: self.on_click())

	def on_click(self):
		self.wind = QMainWindow(parent=self)
		self.wind.setWindowTitle("New Project")

		pos: QPoint = self.wind.mapToGlobal(QPoint(100, 300))
		self.wind.setGeometry(pos.x(), pos.y(), 400, 500)  # todo: GLOBAL POSITION; may not position it correctly

		self.wind.setWindowModality(Qt.WindowModal)

		inp_dlg = PrjPathDialog()
		# inp_dlg.setGeometry(0, 0, 400, 500)
		inp_dlg.accepted.connect(lambda path, name: self.set_txt(path, name))
		inp_dlg.canceled.connect(lambda: self.wind.close())

		self.wind.setCentralWidget(inp_dlg)
		self.wind.show()

	def set_txt(self, path: str, name: str):
		self.wind.close()
		self.name = name
		self.path = path

		self.inputSelected.emit(path, name)


class LoadProject(QPushButton):
	inputSelected = pyqtSignal(str)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.dir = ""

		self.clicked.connect(lambda checked: self.on_click())

	def on_click(self):
		self.wind = QMainWindow()
		self.wind.setWindowTitle("File Dialogue")
		self.wind.setGeometry(200, 300, 1000, 400)  # todo: GLOBAL POSITION; may not position it correctly
		self.wind.setWindowModality(Qt.ApplicationModal)

		self.fl_dlg = QFileDialog()
		self.fl_dlg.fileSelected.connect(lambda s: self.set_txt(s))
		self.fl_dlg.finished.connect(lambda code: self.wind.close())

		self.wind.setMenuWidget(self.fl_dlg)
		self.wind.show()

	def set_txt(self, dir: str):
		self.dir = dir
		self.inputSelected.emit(dir)
		self.wind.close()


#https://stackoverflow.com/questions/5671354/how-to-programmatically-make-a-horizontal-line-in-qt
class QHLine(QFrame):
	def __init__(self, visible=True):
		super().__init__()
		self.setFrameShape(QFrame.HLine)
		if not visible: self.setLineWidth(-1)
		self.setFrameShadow(QFrame.Sunken)


class QVLine(QFrame):
	def __init__(self, visible=True):
		super().__init__()
		self.setFrameShape(QFrame.VLine)
		if not visible: self.setLineWidth(-1)
		self.setFrameShadow(QFrame.Sunken)


class ErrorBox(QMessageBox):
	I = QMessageBox.Information
	W = QMessageBox.Warning
	C = QMessageBox.Critical

	# once the error is created, it can not be removed from the list unless it was removed before a commit
	E000 = {"code": "E000", "level": I, "title": "No Title","txt": "No Text"}
	E001 = {"code": "E001", "level": C, "title": "Application", "txt": "The project directory has not been set."}
	E002 = {"code": "E002", "level": W, "title": "Project", "txt": "Invalid project file"}
	E003 = {"code": "E003", "level": W, "title": "Project", "txt": "Invalid project directory"}
	E004 = {"code": "E004", "level": W, "title": "Project", "txt": "Invalid project key\n(You have not set the model name)"}
	E005 = {"code": "E005", "level": C, "title": "Executor","txt": "Runtime Error"}
	E006 = {"code": "E006", "level": C, "title": "Project", "txt": "Executor file failed to load"}
	E007 = {"code": "E007", "level": C, "title": "Project", "txt": "Model file failed to load"}
	E008 = {"code": "E008", "level": W, "title": "Application", "txt": "A model name is required"}
	E009 = {"code": "E009", "level": C, "title": "Project", "txt": "The directory is not empty"}
	E010 = {"code": "E010", "level": C, "title": "Application", "txt": "Missing input"}
	E011 = {"code": "E011", "level": W, "title": "Application", "txt": "Invalid directory"}

	def __init__(self, code="E000", title="No Title", level=QMessageBox.Information, txt="No Text"):
		super().__init__()
		self.setIcon(level)
		self.setText(txt)
		self.setWindowTitle(code+" - "+title)


class ModelWorkspaceSelector(QComboBox):
	def __init__(self, items: list, parent=None):
		super().__init__(parent)
		self.items = items

		# self.textActivated.connect(lambda s: self.selected_workspace(s))
		# self.currentIndexChanged.connect(lambda ind: self.selection_chng(ind))

		self.update_list(items)

	def update_list(self, items):
		txt = self.currentText()
		self.clear()
		self.items = items
		[self.addItem("<undefined>" if c.name is "" else c.name) for c in items]
		if txt in [i.name for i in items]:
			self.setCurrentText(txt)

	def retrieve_name(self):
		return self.items[self.currentIndex()]


if __name__ == '__main__':
    pass
