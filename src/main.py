import sys

from src.widgets import *
from src.components.workspace.executor import *
from src.components.project_setup import ProjectSetup
from src.components.model_manager import ModelManager
from src.components.visual_result import VisualResult
from src.components.menu_bar import CustomMenu
from src.components.status_bar import CustomStatus

"""
menu tab
--------
project
	save project as*
	save project
	new project
	load project
	-
	project settings
	-
	new model workspace
	save model workspace
add
	nodes
run
	execute current model
"""

"""
Models Wish List
----------------
GPR - Gaussian Process Regression
NRM - Normalization
LBGM - LightBGM

"""

"""
PyQt5 - graphical application library 

NumPy - matrix/array numerical operation
Pandas - external data formatting 
Seaborn - model visualization
Tensorflow - Artificial Intelligence backend
LightGBM - Machine Learning backend

PyTest - general testing

(NumExpr) - Number expression optimizer (a strict accompaniment to NumPy)

cx_Freeze - for building executables for deployment purposes.
"""

"""
Project Board:

Add visualization tab
Revamp `nodes.py` configuration
Add testing tab
Add working menu bars
Add status bars
"""

VERSION = ("Indev", 13, 3)  # todo: future version; add strict versioning implementation


def main():
	app = QApplication(sys.argv)

	win = QMainWindow()
	win.setWindowTitle("GUI AI Application")
	win.setGeometry(0, 0, 1920, 1080)

	outer_layout = QVBoxLayout()
	project_main = QHBoxLayout()

	prj = ProjectSetup()
	mdl = ModelManager(prj.project)
	res = VisualResult()

	prj.projectCreated.connect(lambda proj: mdl.new_prj(proj))
	prj.projectLoaded.connect(lambda proj: mdl.load_prj(proj))
	mdl.modelUpdate.connect(lambda obj: res.model_update(obj))

	prj_tab = QTabWidget()
	prj_tab.addTab(prj, "Project Setup")
	prj_tab.addTab(mdl, "Model")
	prj_tab.addTab(res, "Result")
	prj_tab.addTab(QLabel("Testing models input real time"), "Test Input")
	prj_tab.addTab(QLabel("Deploying this onto a portable and usable AI/ML model to their destination"), "Deployment")

	project_main.addWidget(prj_tab)

	outer_layout.addLayout(project_main)

	w = QWidget()
	w.setLayout(outer_layout)
	win.setCentralWidget(w)

	menu = CustomMenu()
	win.setMenuWidget(menu)

	stat = CustomStatus()
	win.setStatusBar(stat)

	win.show()
	sys.exit(app.exec())


print("PROGRAM START")
if __name__ == '__main__':
	main()
print("PROGRAM END")
