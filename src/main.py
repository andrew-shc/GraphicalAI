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

# Client code
def main():
	app = QApplication(sys.argv)

	win = QMainWindow()
	win.setWindowTitle("GUI AI Application")
	win.setGeometry(0, 0, 1920, 1080)

	state = StateHolder()

	scene = QGraphicsScene(0,0,1920,1080)
	view = QGraphicsView(scene)
	view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	view.setDragMode(view.NoDrag)

	# w.scene().addItem(Connector(cnc, (10, 10, 50, 50), "A", TAG_EXT, [TAG_EXT]))
	# w.scene().addItem(Connector(cnc, (10, 100, 50, 50), "A", TAG_EXT, [TAG_EXT]))

	p_rootDir = ProjectRootEdit("project root directory")

	b_addModel = ModelSelector("models", state, view)
	b_saveProj = QPushButton("Save Project")
	b_saveProj.clicked.connect(lambda checked: model_saver(state.model_dt, view.items(), p_rootDir.dir))
	b_clearProj = QPushButton("Clear Project")
	b_clearProj.clicked.connect(lambda checked: [scene.removeItem(i) for i in scene.items()])
	b_execProj = QPushButton("Execute Project")
	b_execProj.clicked.connect(lambda checked: dat_file_loader(p_rootDir.dir))


	outer_layout = QVBoxLayout()
	project_main = QHBoxLayout()

	inner_menu = QVBoxLayout()
	inner_menu.addWidget(b_addModel)
	inner_menu.addWidget(b_saveProj)
	inner_menu.addWidget(b_clearProj)
	inner_menu.addWidget(b_execProj)
	inner_menu.addWidget(p_rootDir)
	inner_menu.addStretch()

	inspector = QVBoxLayout()

	project_main.addLayout(inner_menu)
	project_main.addWidget(view)
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
