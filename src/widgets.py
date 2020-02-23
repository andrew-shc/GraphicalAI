from PyQt5.QtWidgets import *

import os

from src.debug import *
from src.project_file_interface import ProjectFI

class NodeSelector(QComboBox):
	def __init__(self, py_fobj, state, g_view, parent=None):
		super().__init__(parent)
		self.state = state  # connector's global data
		self.g_view = g_view  # graphics view

		self.mdl_typ = [py_fobj.__dict__[c] for c in py_fobj.__dir__()
		                if type(py_fobj.__dict__[c]) == type
		                if py_fobj.__dict__[c].__module__ == py_fobj.__name__
		                ]

		[self.addItem(c.name) for c in self.mdl_typ]

		self.textActivated.connect(lambda string: self.addModel(string, state))

	def addModel(self, string, state):
		# there should only be one model that have a unique name thus it should have only one item in the list
		# and each item in the list must be model class meaning it has the method create()

		for c in self.mdl_typ:
			if string == c.name:
				self.g_view.scene().addWidget(c.create(self.state, self.g_view, (400, 200)))

class ProjectRootEdit(QPushButton):
	def __init__(self, state, start=os.path.expanduser("~")):
		super().__init__()
		self.dir = ""
		self.lastText = start  # starting directory; start with the *start* directory

		self.setText(start)

		self.clicked.connect(lambda checked: self.onClick(checked, state))

	def onClick(self, clicked, state):
		""" creates the file dialogue """
		self.wind = QMainWindow()
		self.wind.setWindowTitle("File Dialogue")
		self.wind.setGeometry(0, 0, 1000, 400)

		self.file_dialog = QFileDialog()
		self.file_dialog.setFileMode(self.file_dialog.DirectoryOnly)
		self.file_dialog.setViewMode(self.file_dialog.List)

		self.file_dialog.fileSelected.connect(lambda dir: self.setDir(state, dir))

		self.wind.setMenuWidget(self.file_dialog)
		self.wind.show()

	def setDir(self, state, url):
		self.dir = url+"/"
		self.setText(self.dir)
		self.wind.close()  # closes the window\

		state.project = ProjectFI(self.dir)
		state.project.create_project()
		state.project.load_project()


class ProjectDirectory(QFileDialog):
	def __init__(self, url):
		super().__init__()
		self.setFileMode(self.DirectoryOnly)


#https://stackoverflow.com/questions/5671354/how-to-programmatically-make-a-horizontal-line-in-qt
class QHLine(QFrame):
	def __init__(self):
		super(QHLine, self).__init__()
		self.setFrameShape(QFrame.HLine)
		self.setFrameShadow(QFrame.Sunken)



class ErrorBox(QMessageBox):
	E000 = {"level":QMessageBox.Information, "title":"No Title", "txt":"No Text"}
	E001 = {"level":QMessageBox.Critical, "title":"State", "txt":"The project directory has not been set."}

	def __init__(self, title="No Title", level=QMessageBox.Information, txt="No Text"):
		super().__init__()
		self.setIcon(level)
		self.setText(txt)
		self.setWindowTitle(title)


########################EXPERIMENTAL######################################

class ModelWorkspaceSelector(QComboBox):
	def __init__(self, items, parent=None):
		super().__init__(parent)
		self.selected = None

		[self.addItem(c.name) for c in items]

		self.textActivated.connect(lambda string: self.selectedWorkspace(string))

	def selectedWorkspace(self, string):
		self.selected = string