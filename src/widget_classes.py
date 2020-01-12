from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl

import os

from src.project_file_interface import ProjectFI

class ModelSelector(QComboBox):
	def __init__(self, py_file_name: str, state, g_view, project, parent=None):
		super().__init__(parent)
		self.state = state  # connector's global data
		self.g_view = g_view  # graphics view
		self.project = project

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
		for c in self.mdl_typ:
			if s == c.name:
				self.g_view.scene().addWidget(c.create(self.state, self.g_view, (400, 200), self.project.project))
				print(s, c, self.mdl_typ)


class ProjectRootEdit(QPushButton):
	def __init__(self, mngr, start=os.path.expanduser("~")):
		super().__init__()
		self.mngr = mngr  # project manager class
		self.dir = ""
		self.lastText = start  # starting directory; start with the *start* directory

		self.setText(start)

		self.clicked.connect(lambda checked: self.onClick(checked))

	def onClick(self, clicked):
		""" creates the file dialogue """
		self.wind = QMainWindow()
		self.wind.setWindowTitle("File Dialogue")
		self.wind.setGeometry(0, 0, 1000, 400)

		self.file_dialog = QFileDialog()
		self.file_dialog.setFileMode(self.file_dialog.DirectoryOnly)
		self.file_dialog.setViewMode(self.file_dialog.List)

		self.file_dialog.fileSelected.connect(lambda dir: self.setDir(dir))

		self.wind.setMenuWidget(self.file_dialog)
		self.wind.show()

	def setDir(self, url):
		self.dir = url+"/"
		self.setText(self.dir)
		self.wind.close()  # closes the window
		print("===")
		self.mngr.project = ProjectFI(self.dir)
		self.mngr.project.create_project()
		self.mngr.project.load_project()


class ProjectDirectory(QFileDialog):
	def __init__(self, url):
		super().__init__()
		self.setFileMode(self.DirectoryOnly)
