from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from typing import List, Optional

from src.debug import *
from src.widgets import *
from src.executor import *

from src.gfx.connector import Connector
from src.gfx.connection import Connection
from src.gfx.node import Node

import pickle

"""
### GUI Layout (under Model Tab) ###
Model Selector  (ModelManager)
--------------------------------
Model      | Model     | Inspector
Interface  | Central   | Panel
           | Workspace |
* all 3 subsection are part of (ModelWorkspace:QWidget)
"""


class ModelWorkspace(QWidget):
	name = "Unnamed"
	key: Optional[int] = None

	nameChanged = pyqtSignal(str)

	def __init__(self, proj: ProjectFI, parent=None):
		super().__init__(parent=parent)
		self.project = proj

		self.inst_ui()

	def inst_ui(self):
		# Graphics Scene: Where the node will be selected
		scene = QGraphicsScene(0, 0, 1920, 1080)
		self.view = QGraphicsView(scene)
		self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.view.setDragMode(self.view.NoDrag)

		b_add_nd = NodeSelector(__import__("nodes"), self.view)
		self.b_name = QLabel(self.name)
		name_fnt = self.b_name.font()
		name_fnt.setPointSize(14)
		self.b_name.setFont(name_fnt)
		b_inp_nd = InputDialog("Set Name")  # model name input
		b_inp_nd.inputSelected.connect(lambda s: self.set_name( s, self.b_name))

		b_save_mdl = QPushButton("Save Model")  # save model
		b_save_mdl.clicked.connect(lambda checked: self.save_model())
		b_clear_mdl = QPushButton("Clear Model")
		b_clear_mdl.clicked.connect(lambda checked: self.clear_model())
		b_exec_mdl = QPushButton("Execute Model")
		b_exec_mdl.clicked.connect(lambda checked: self.execute())

		intf_menu = QVBoxLayout()  # interface menu
		intf_menu.addWidget(self.b_name)
		intf_menu.addWidget(b_inp_nd)
		intf_menu.addWidget(QHLine())
		intf_menu.addWidget(b_add_nd)
		intf_menu.addWidget(b_save_mdl)
		intf_menu.addWidget(b_clear_mdl)
		intf_menu.addWidget(b_exec_mdl)
		intf_menu.addStretch()

		insp_menu = QVBoxLayout()  # inspector menu
		insp_menu.addWidget(QLabel("This is the Inspector Menu"))

		central = QHBoxLayout()
		central.addLayout(intf_menu)
		central.addWidget(self.view)
		central.addLayout(insp_menu)

		self.setLayout(central)

	def update_proj(self, proj: ProjectFI): self.project = proj

	def set_name(self, name: str, label: QLabel):
		if self.project is not None:
			self.name = name
			label.setText(name)
			self.nameChanged.emit(name)

			if self.key is None:
				reg_key = self.project.get_key(name)
				if reg_key is not None:
					self.key = reg_key
				else:
					print(f"[ERROR] The model name <{name}> is currently an active name; NO DUPLICATE NAMES")
			else:
				self.project.change_name(self.key, name)
			self.project.save()
		else:
			ErrorBox(**ErrorBox.E001).exec()

	def save_model(self):
		if self.project is not None:
			if self.key is not None:
				self.project.save_mdl_exec(self.key, self.view.items())
				self.project.save_mdl_proj(self.key, self.view.items())
				self.project.save()
			else:
				print("Error: Project File Interface key is empty")
		else:
			ErrorBox(**ErrorBox.E001).exec()

	def clear_model(self):
		if self.project is not None:
			[self.view.scene().removeItem(i) for i in self.view.scene().items()]
		else:
			ErrorBox(**ErrorBox.E001).exec()

	def execute(self):
		if self.project is not None:
			if self.key is not None:
				self.executor = ModelExecutor(self.project, self.key)
				self.executor.beginExecution()
			else:
				print("Error: Project File Interface key is empty")
		else:
			ErrorBox(**ErrorBox.E001).exec()


class ModelManager(QWidget):
	models: List[ModelWorkspace] = []

	def __init__(self, proj: ProjectFI, parent=None):
		super().__init__(parent=parent)
		self.spacer = QVLine(visible=False)  # vertical spacer
		self.spacer.hide()
		self.cur_mdl: Optional[ModelWorkspace] = None
		self.project: Optional[ProjectFI] = None

		self.inst_ui(proj)
		self.add_model(proj)

	def inst_ui(self, proj: ProjectFI):
		self.mdl_slctr = ModelWorkspaceSelector(self.models)
		self.mdl_slctr.activated.connect(lambda ind: self.select_model(ind))
		b_new_mdl = QPushButton("New Model")
		b_new_mdl.clicked.connect(lambda checked: self.add_model(proj))
		b_rem_mdl = QPushButton("Remove Current Model")
		b_rem_mdl.clicked.connect(lambda checked: self.rem_model(self.cur_mdl))

		# b_rfr_mdl = QPushButton("Refresh")
		# b_rfr_mdl.clicked.connect(lambda checked: self.mdl_slctr.update_list(self.models))

		upper_menu = QHBoxLayout()
		upper_menu.addWidget(self.mdl_slctr)
		upper_menu.addWidget(b_new_mdl)
		upper_menu.addWidget(b_rem_mdl)
		# upper_menu.addWidget(b_rfr_mdl)

		self.cur_mdl = None if len(self.models) == 0 else self.models[self.mdl_slctr.currentIndex()]

		self.central = QVBoxLayout()
		self.central.addLayout(upper_menu)
		self.central.addWidget(self.cur_mdl)
		self.central.addWidget(self.spacer)

		self.setLayout(self.central)

	def add_model(self, proj: ProjectFI):
		mdl_wksp = ModelWorkspace(proj)
		mdl_wksp.nameChanged.connect(lambda s: self.mdl_slctr.update_list(self.models))
		self.models.append(mdl_wksp)
		self.mdl_slctr.update_list(self.models)
		self.spacer.hide()

		self.select_model(self.mdl_slctr.count()-1)

	def select_model(self, ind: int):
		self.mdl_slctr.setCurrentIndex(ind)

		if self.cur_mdl is not None: self.cur_mdl.hide()
		self.cur_mdl = self.models[ind]
		self.cur_mdl.show()
		self.central.addWidget(self.cur_mdl)

	def rem_model(self, mdl_wrkspc: ModelWorkspace):
		if self.mdl_slctr.count() >= 2:
			self.models.remove(mdl_wrkspc)
			self.mdl_slctr.update_list(self.models)
			self.select_model(0)
		elif self.mdl_slctr.count() == 1:
			self.models.remove(mdl_wrkspc)
			self.mdl_slctr.update_list(self.models)
			self.cur_mdl.hide()
			self.central.removeWidget(mdl_wrkspc)
			self.spacer.show()
		else:
			print("Error: No more models!")

	def new_prj(self, proj: ProjectFI):  # the model workspace would be stayed as same
		print("PROJECT NEW")
		self.project = proj
		[mdl.update_proj(proj) for mdl in self.models]

	def load_prj(self, proj: ProjectFI):  # the loaded model workspace would APPEND the current workspace
		print("PROJECT LOAD")
		self.project = proj
		[mdl.update_proj(proj) for mdl in self.models]

		for mdl_key in self.project.project["model"]["tag"]:
			mdl_wksp = ModelWorkspace(self.project)
			mdl_wksp.key = mdl_key
			mdl_wksp.name = self.project.project["model"]["tag"][mdl_key]
			mdl_wksp.b_name.setText(mdl_wksp.name)
			for itm in self.project.read_mdl_proj(mdl_key).items()[::-1]:
				mdl_wksp.view.scene().addItem(itm)
			print(":::", mdl_wksp.view.items())
			self.models.append(mdl_wksp)
		self.mdl_slctr.update_list(self.models)

		print(self.project.project["model"]["tag"])


