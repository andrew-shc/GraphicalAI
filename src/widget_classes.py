from PyQt5.QtWidgets import QComboBox, QLineEdit


class ModelSelector(QComboBox):
	def __init__(self, py_file_name: str, state, g_view, parent=None):
		super().__init__(parent)
		self.state = state  # connector's global data
		self.g_view = g_view  # graphics view

		fl_dt = __import__(py_file_name)  # import the models from a single file
		self.mdl_typ = [fl_dt.__dict__[c] for c in fl_dt.__dir__()
		                if type(fl_dt.__dict__[c]) == type
		                if fl_dt.__dict__[c].__module__ == fl_dt.__name__
		                ]

		[self.addItem(c.name) for c in self.mdl_typ]

		self.textActivated.connect(lambda s: self.addModel(s))

	def addModel(self, s):
		# there should only be one model that have a unique name thus it should have only one item in the list
		# and each item in the list must be model class meaning it has the method create()

		[self.g_view.scene().addWidget(c.create(self.state, self.g_view, (100, 200)))
		 for c in self.mdl_typ if s == c.name]


import os


class ProjectRootEdit(QLineEdit):
	# TODO: this is class will be replaced with a better project setup

	def __init__(self, *args):
		super().__init__(*args)
		self.dir = ""
		self.lastText = ""

		self.returnPressed.connect(lambda: self.setRoot())

	def setRoot(self):
		if os.path.isdir(self.text()):
			self.dir = self.text()+"/"
			self.lastText = self.text()+"/"
		else:
			print("[ERROR]: Create an empty directory for a new project directory!")
			self.setText(self.lastText)
