import sys

from PyQt5.QtCore import Qt

from src.debug import *
from src.widgets import *
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

"""
ai models to add
--------
SVC - Support Vector Classification
GPR - Gaussian Process Regression
DT,C - Decision Tree Classifier
PP,NRM - Normalization

"""

def load_proj(proj, dir):
	proj.project = ProjectFI(dir)
	proj.project.load_project()
	# proj.project.new_ai_model(["1"], "vision models")
	# proj.project.new_ai_model(["N"], "listening models")

def new_proj(proj, dir):
	proj.project = ProjectFI(dir)
	proj.project.create_project()

def save_project(state):
	if state.project is not None:
		state.project.save_project()
	else:
		ErrorBox(ErrorBox.E001)

def project_settings(state, p_rootDir):
	menu_left = QVBoxLayout()

	root_dir = QHBoxLayout()
	root_dir.addWidget(QLabel("Set Project Directory: "))
	root_dir.addWidget(p_rootDir)

	save_proj = QPushButton("Save Project")
	save_proj.clicked.connect(lambda clicked: state.project.save_project())

	menu_left.addLayout(root_dir)
	menu_left.addWidget(save_proj)
	menu_left.addStretch()

	base = QHBoxLayout()
	base.addLayout(menu_left)
	base.addStretch(2)

	central = QWidget()
	central.setLayout(base)

	return central

def tab_ai_model(state, manager, p_rootDir):
	scene = QGraphicsScene(0,0,1920,1080)
	view = QGraphicsView(scene)
	view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setDragMode(view.NoDrag)

	# view.scene().addItem(Connector(cnc, (10, 10, 50, 50), "A", TAG_EXT, [TAG_EXT]))
	# view.scene().addItem(Connector(cnc, (10, 100, 50, 50), "A", TAG_EXT, [TAG_EXT]))

	b_addModel = ModelSelector(__import__("models.ai_models").__dict__["ai_models"], state, view, manager)
	b_saveProj = QPushButton("Save Models")
	b_saveProj.clicked.connect(lambda checked: model_saver(state.model_dt, view.items(), p_rootDir.dir, "ai_skl.dat"))
	b_clearProj = QPushButton("Clear Models")
	b_clearProj.clicked.connect(lambda checked: [scene.removeItem(i) for i in scene.items()])

	inner_menu = QVBoxLayout()
	inner_menu.addWidget(b_addModel)
	inner_menu.addWidget(b_saveProj)
	inner_menu.addWidget(b_clearProj)
	inner_menu.addStretch()

	inspector = QVBoxLayout()
	inspector.addWidget(QLabel("This is the inspector panel"))

	ai_model = QHBoxLayout()
	ai_model.addLayout(inner_menu)
	ai_model.addWidget(view)
	ai_model.addLayout(inspector)

	central = QWidget()
	central.setLayout(ai_model)

	return central

def addTabModel(tab: QTabWidget, state, manager, p_rootDir):
	scene = QGraphicsScene(0,0,1920,1080)
	view = QGraphicsView(scene)
	view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setDragMode(view.NoDrag)

	# view.scene().addItem(Connector(cnc, (10, 10, 50, 50), "A", TAG_EXT, [TAG_EXT]))
	# view.scene().addItem(Connector(cnc, (10, 100, 50, 50), "A", TAG_EXT, [TAG_EXT]))

	b_addModel = ModelSelector(__import__("nodes"), state, view, manager)
	b_saveProj = QPushButton("Save Models")
	b_saveProj.clicked.connect(lambda checked: model_saver(state.model_dt, view.items(), p_rootDir.dir, "ml_skl.dat"))
	b_clearProj = QPushButton("Clear Models")
	b_clearProj.clicked.connect(lambda checked: [scene.removeItem(i) for i in scene.items()])

	inner_menu = QVBoxLayout()
	inner_menu.addWidget(b_addModel)
	inner_menu.addWidget(b_saveProj)
	inner_menu.addWidget(b_clearProj)
	inner_menu.addStretch()

	inspector = QVBoxLayout()
	inspector.addWidget(QLabel("This is the inspector panel"))

	ml_model = QHBoxLayout()
	ml_model.addLayout(inner_menu)
	ml_model.addWidget(view)
	ml_model.addLayout(inspector)

	central = QWidget()
	central.setLayout(ml_model)

	tab.addTab(central, "New Model")

def tab_model(state, manager, p_rootDir):
	base = QHBoxLayout()

	model_tab = QTabWidget()
	add_tab = QPushButton("New Tab")
	add_tab.clicked.connect(lambda checked: addTabModel(model_tab, state, manager, p_rootDir))

	base.addWidget(add_tab)
	base.addWidget(model_tab)

	central = QWidget()
	central.setLayout(base)
	return central




# Client code
def main():
	app = QApplication(sys.argv)

	win = QMainWindow()
	win.setWindowTitle("GUI AI Application")
	win.setGeometry(0, 0, 1920, 1080)

	state = StateHolder()
	p_rootDir = ProjectRootEdit(state)

	outer_layout = QVBoxLayout()
	project_main = QHBoxLayout()

	from src.model_manager import ModelManager

	mdl = ModelManager(state)

	prj_tab = QTabWidget()
	prj_tab.addTab(project_settings(state, p_rootDir), "Project Setup")  # QLabel("This is where defining a new training model will be.")
	prj_tab.addTab(mdl.getCurrentModel(state), "Model")
	prj_tab.addTab(QLabel("This is where would the model result\n"
	                      "and prediction graphs will be.\n"
	                      "And graphs such as, Error Rate\n"
	                      "and ML settings like settings\n"
	                      "each batch size."), "Result")
	prj_tab.addTab(QLabel("Testing models input real time"), "Test Input")
	prj_tab.addTab(QLabel("Deploying this onto a portable and usable AI/ML model to their destination"), "Deployment")
	prj_tab.addTab(QLabel("Project Settings such as Theme, Node Size, and related."), "Project Settings")

	project_main.addWidget(prj_tab)

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

print("PROGRAM START", l=INF)
if __name__ == '__main__':
	main()
print("PROGRAM END", l=INF)
