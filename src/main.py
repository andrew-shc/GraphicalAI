import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtWidgets import *

from src.model import Model
from src.widget_classes import *
from src.state import StateHolder
from src.executor import *

TAG_EXT = None

PROJ_ROOT = "../tmp/"
"""
project root v1
	skeleton.dat
	model.exec
	training data
		group1
			...
		group2
			...
	testing data
		...
	
"""

def tab_ai_model(state):
	scene = QGraphicsScene(0,0,1920,1080)
	view = QGraphicsView(scene)
	view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setDragMode(view.NoDrag)

	# view.scene().addItem(Connector(cnc, (10, 10, 50, 50), "A", TAG_EXT, [TAG_EXT]))
	# view.scene().addItem(Connector(cnc, (10, 100, 50, 50), "A", TAG_EXT, [TAG_EXT]))

	p_rootDir = ProjectRootEdit("project root directory")

	b_addModel = ModelSelector("models", state, view)
	b_saveProj = QPushButton("Save Project")
	b_saveProj.clicked.connect(lambda checked: model_saver(state.model_dt, view.items(), p_rootDir.dir))
	b_clearProj = QPushButton("Clear Project")
	b_clearProj.clicked.connect(lambda checked: [scene.removeItem(i) for i in scene.items()])
	b_execProj = QPushButton("Execute Project")
	b_execProj.clicked.connect(lambda checked: dat_file_loader(p_rootDir.dir))
	b_loadProj = QPushButton("[ABSTRACT] Load Project")
	b_newProj = QPushButton("[ABSTRACT] New Project")

	inner_menu = QVBoxLayout()
	inner_menu.addWidget(b_addModel)
	inner_menu.addWidget(b_saveProj)
	inner_menu.addWidget(b_clearProj)
	inner_menu.addWidget(b_execProj)
	inner_menu.addWidget(p_rootDir)
	inner_menu.addWidget(b_loadProj)
	inner_menu.addWidget(b_newProj)
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

	outer_layout = QVBoxLayout()
	project_main = QHBoxLayout()

	prj_tab = QTabWidget()
	prj_tab.addTab(tab_ai_model(state), "AI Model")
	prj_tab.addTab(QLabel("Machine Learning: Training and Testing"), "ML")
	prj_tab.addTab(QLabel("This is where would the model result\n"
	                      "and prediction graphs will be.\n"
	                      "And graphs such as, Error Rate\n"
	                      "and ML settings like settings\n"
	                      "each batch size."), "Model Result and Prediction")
	prj_tab.addTab(QLabel("Project Settings such as Theme, Node Size, and related."), "Project Settings")

	inspector = QVBoxLayout()
	inspector.addWidget(QLabel("This is the inspector panel"))

	project_main.addWidget(QLabel("Project Directory"))
	project_main.addWidget(prj_tab)
	project_main.addLayout(inspector)

	outer_layout.addLayout(project_main)

	w = QWidget()
	w.setLayout(outer_layout)
	win.setCentralWidget(w)

	menu = QHBoxLayout()
	menu.addWidget(QLabel("file"))
	menu.addWidget(QLabel("run"))
	menu.addWidget(QLabel("ML"))
	menu.addStretch()

	m = QWidget()
	m.setLayout(menu)
	win.setMenuWidget(m)

	win.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
