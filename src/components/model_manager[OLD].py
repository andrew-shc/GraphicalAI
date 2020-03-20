from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from src.debug import *
from src.widgets import *
from src.executor import *
from src.state import StateHolder

from src.gfx.connector import Connector
from src.gfx.connection import Connection
from src.gfx.node import Node

import pickle


class ModelWorkspace:  # instance class
	central = None  # the central widget
	name = None  # the model workspace name

	def __init__(self, state):
		self.scene = QGraphicsScene(0, 0, 1920, 1080)
		self.view = QGraphicsView(self.scene)
		self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.view.setDragMode(self.view.NoDrag)

		inspector = QVBoxLayout()
		inspector.addWidget(QLabel("This is the inspector panel"))

		model = QHBoxLayout()
		model.addWidget(self.view)
		model.addLayout(inspector)

		self.central = QWidget()
		self.central.setLayout(model)

	@classmethod
	def load(cls, fdata):
		pass

	def save(self) -> "list of str":
		pass


class ModelWorkspace_:
	def __init__(self, state, name=None):
		self.central = QWidget()
		self.name = name  # starting name

		b_addModel = NodeSelector(__import__("nodes"), state, view)
		b_modelName = QLineEdit("Model Name")
		b_saveProj = QPushButton("Save Model")
		b_saveProj.clicked.connect(
			lambda checked: self.updateModel(state.project, view.items(), b_modelName.text(), state))
		b_clearProj = QPushButton("Clear Model")
		b_clearProj.clicked.connect(lambda checked: [scene.removeItem(i) for i in scene.items()])
		b_execProj = QPushButton("Execute Model")
		b_execProj.clicked.connect(lambda checked: self.execute(state))

		inner_menu = QVBoxLayout()
		inner_menu.addWidget(b_currModel)
		inner_menu.addWidget(b_addModel)
		inner_menu.addWidget(b_modelName)
		inner_menu.addWidget(b_saveProj)
		inner_menu.addWidget(b_clearProj)
		inner_menu.addWidget(QHLine())
		inner_menu.addWidget(b_execProj)
		# inner_menu.addWidget(ErrorDialogue())
		inner_menu.addStretch()

		layout = QHBoxLayout()

		layout.addLayout(inner_menu)
		layout.addWidget(mdl_wrkspc.central)


class _ModelManager:  # manager class
	def __init__(self, _state):
		models = []  # list of model workspace
		index = 0  # current choice of model workspace

	def getCurrentModel(self, state): pass


class ModelManager:  # manager class
	models = []  # list of model tab reference
	index = 0  # current choice of the model

	def __init__(self, state):
		self.newModel(state)

	def getCurrentModel(self, state):
		if 0 <= self.index < len(self.models):
			mdl_wrkspc = self.models[self.index]
			view = mdl_wrkspc.view
			scene = mdl_wrkspc.scene

			b_currModel = ModelWorkspaceSelector(self.models)
			b_addModel = NodeSelector(__import__("nodes"), state, view)
			b_modelName = QLineEdit("Model Name")
			b_saveProj = QPushButton("Save Model")
			b_saveProj.clicked.connect(lambda checked: self.updateModel(state.project, view.items(), b_modelName.text(), state))
			b_clearProj = QPushButton("Clear Model")
			b_clearProj.clicked.connect(lambda checked: [scene.removeItem(i) for i in scene.items()])
			b_execProj = QPushButton("Execute Model")
			b_execProj.clicked.connect(lambda checked: self.execute(state))

			inner_menu = QVBoxLayout()
			inner_menu.addWidget(b_currModel)
			inner_menu.addWidget(b_addModel)
			inner_menu.addWidget(b_modelName)
			inner_menu.addWidget(b_saveProj)
			inner_menu.addWidget(b_clearProj)
			inner_menu.addWidget(QHLine())
			inner_menu.addWidget(b_execProj)
			# inner_menu.addWidget(ErrorDialogue())
			inner_menu.addStretch()

			layout = QHBoxLayout()

			layout.addLayout(inner_menu)
			layout.addWidget(mdl_wrkspc.central)

			central = QWidget()
			central.setLayout(layout)

			return central
		print(f"Model index <{self.index}> is invalid because the length of the model list is <{len(self.models)}>", l=ERR)
		return None

	def updateModel(self, project, items, model_name, state):

		#================== SERIALIZE DATA ==================#
		self.model_serializer(items, "model.yaml")
		print("~~~")
		item_list = self.model_deserializer(state, "model.yaml")

		if project is not None:
			self.model_serializer(items, str(self.index)+".yaml")
			project.model_saver([i for i in items if isinstance(i, Node)], items, model_name)
		else:
			ErrorBox(**ErrorBox.E001).exec()

	def newModel(self, state):
		self.models.append(ModelWorkspace(state))

	def changeModel(self, ind):
		self.index = ind

	def execute(self, state):
		if state.project is not None:
			self.executor = ModelExecutor(state.project, "MODEL_4.dat")
			self.executor.beginExecution()
		else:
			ErrorBox(**ErrorBox.E001).exec()

	def model_serializer(self, items: list, fname: str):  # items -> A list of items such as from the QGraphicsView
		with open("../MODEL_0.dat", "wb") as fbj:
			print("<<<", items)
			pickle.dump(items, fbj)

	def model_deserializer(self, state, fname: str):
		items = []
		with open("../MODEL_0.dat", "rb") as fbj:
			items = pickle.load(fbj)
			print(">>>", items)
		return items


if __name__ == '__main__':
	mdl = ModelManager.model_deserializer(None, StateHolder(), "model.yaml")
	print(mdl)

"""
select models
save model (current)
	- name
clear model (current)
execute model (current)

"""