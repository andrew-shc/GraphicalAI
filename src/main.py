import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import *

from src.model import Model
from src.widget_classes import *
from src.state import StateHolder
from src.executor import *
from src.project_file_interface import ProjectFI

TAG_EXT = None

# PROJ_ROOT = "../tmp/"


"""
menu tab
--------
project
	save project as
	save project
	new project
	load project
	delete project
	-
	project settings
run
	run project model
	run project ML
	run project (real input)
"""

class ProjectManager:
	def __init__(self, prj=None):
		self.__project: ProjectFI = prj

	@property
	def project(self):
		if self.__project is None:
			print("[WARNING]: The Project attribute is set to None")
		return self.__project

	@project.setter
	def project(self, proj: ProjectFI):
		print("[WARNING]: The Project attribute is set")
		self.__project = proj

	@project.deleter
	def project(self):
		print("[WARNING]: The Project attribute is deleted")
		self.__project = None


def load_proj(proj, dir):
	proj.project = ProjectFI(dir)
	proj.project.load_project()
	# proj.project.new_ai_model(["1"], "vision models")
	# proj.project.new_ai_model(["N"], "listening models")

def new_proj(proj, dir):
	proj.project = ProjectFI(dir)
	proj.project.create_project()

def project_settings(state, manager, p_rootDir):
	menu = QVBoxLayout()
	menu.addWidget(p_rootDir)
	menu.addStretch()

	ai_model = QHBoxLayout()
	ai_model.addLayout(menu)
	ai_model.addStretch(2)

	central = QWidget()
	central.setLayout(ai_model)

	return central

def tab_ai_model(state, manager, p_rootDir):
	scene = QGraphicsScene(0,0,1920,1080)
	view = QGraphicsView(scene)
	view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setDragMode(view.NoDrag)

	# view.scene().addItem(Connector(cnc, (10, 10, 50, 50), "A", TAG_EXT, [TAG_EXT]))
	# view.scene().addItem(Connector(cnc, (10, 100, 50, 50), "A", TAG_EXT, [TAG_EXT]))

	b_addModel = ModelSelector("ai_models", state, view, manager)
	b_saveProj = QPushButton("Save Models")
	b_saveProj.clicked.connect(lambda checked: model_saver(state.model_dt, view.items(), p_rootDir.dir, "ai_skl.dat"))
	b_clearProj = QPushButton("Clear Models")
	b_clearProj.clicked.connect(lambda checked: [scene.removeItem(i) for i in scene.items()])
	b_execProj = QPushButton("Execute Models")
	b_execProj.clicked.connect( lambda checked: executor(*dat_file_loader(p_rootDir.dir, "ai_skl.dat"), manager.project, AI) )

	inner_menu = QVBoxLayout()
	inner_menu.addWidget(b_addModel)
	inner_menu.addWidget(b_saveProj)
	inner_menu.addWidget(b_clearProj)
	inner_menu.addWidget(b_execProj)
	inner_menu.addStretch()

	ai_model = QHBoxLayout()
	ai_model.addLayout(inner_menu)
	ai_model.addWidget(view)

	central = QWidget()
	central.setLayout(ai_model)

	return central

def tab_ml_model(state, manager, p_rootDir):
	scene = QGraphicsScene(0,0,1920,1080)
	view = QGraphicsView(scene)
	view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setDragMode(view.NoDrag)

	# view.scene().addItem(Connector(cnc, (10, 10, 50, 50), "A", TAG_EXT, [TAG_EXT]))
	# view.scene().addItem(Connector(cnc, (10, 100, 50, 50), "A", TAG_EXT, [TAG_EXT]))

	b_addModel = ModelSelector("ml_models", state, view, manager)
	b_saveProj = QPushButton("Save Models")
	b_saveProj.clicked.connect(lambda checked: model_saver(state.model_dt, view.items(), p_rootDir.dir, "ml_skl.dat"))
	b_clearProj = QPushButton("Clear Models")
	b_clearProj.clicked.connect(lambda checked: [scene.removeItem(i) for i in scene.items()])
	b_execProj = QPushButton("Execute Models")
	b_execProj.clicked.connect( lambda checked: executor(*dat_file_loader(p_rootDir.dir, "ml_skl.dat"), manager.project, ML) )

	inner_menu = QVBoxLayout()
	inner_menu.addWidget(b_addModel)
	inner_menu.addWidget(b_saveProj)
	inner_menu.addWidget(b_clearProj)
	inner_menu.addWidget(b_execProj)
	inner_menu.addStretch()

	ai_model = QHBoxLayout()
	ai_model.addLayout(inner_menu)
	ai_model.addWidget(view)

	central = QWidget()
	central.setLayout(ai_model)

	return central


# Client code
def main():
	app = QApplication(sys.argv)

	win = QMainWindow()
	win.setWindowTitle("GUI AI Application")
	win.setGeometry(0, 0, 1920, 1080)

	state = StateHolder()
	manager = ProjectManager()
	p_rootDir = ProjectRootEdit(manager)

	outer_layout = QVBoxLayout()
	project_main = QHBoxLayout()

	prj_tab = QTabWidget()
	prj_tab.addTab(project_settings(state, manager, p_rootDir), "Project Setup")  # QLabel("This is where defining a new training model will be.")
	prj_tab.addTab(tab_ai_model(state, manager, p_rootDir), "AI Model")
	prj_tab.addTab(tab_ml_model(state, manager, p_rootDir), "ML Model")  # QLabel("Machine Learning: Training and Testing")
	prj_tab.addTab(QLabel("This is where would the model result\n"
	                      "and prediction graphs will be.\n"
	                      "And graphs such as, Error Rate\n"
	                      "and ML settings like settings\n"
	                      "each batch size."), "Result")
	prj_tab.addTab(QLabel("Testing models input"), "Test Input")
	prj_tab.addTab(QLabel("Project Settings such as Theme, Node Size, and related."), "Project Settings")

	inspector = QVBoxLayout()
	inspector.addWidget(QLabel("This is the inspector panel"))

	project_main.addWidget(ProjectDirectory("C:/"))
	project_main.addWidget(prj_tab)
	project_main.addLayout(inspector)

	outer_layout.addLayout(project_main)

	w = QWidget()
	w.setLayout(outer_layout)
	win.setCentralWidget(w)

	menu =  QMenuBar()
	menu.addMenu("project")
	menu.addSeparator()
	menu.addMenu("run")

	# m = QWidget()
	# m.setLayout(menu)
	win.setMenuWidget(menu)

	win.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
