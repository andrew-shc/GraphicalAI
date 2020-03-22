import sys

from src.debug import print  # type: ignore

from src.widgets import *  # type: ignore
from src.executor import *  # type: ignore
from src.components.project_setup import ProjectSetup  # type: ignore
from src.components.model_manager import ModelManager  # type: ignore


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

# Client code
def main():
	app = QApplication(sys.argv)

	win = QMainWindow()
	win.setWindowTitle("GUI AI Application")
	win.setGeometry(0, 0, 1920, 1080)

	outer_layout = QVBoxLayout()
	project_main = QHBoxLayout()

	prj = ProjectSetup()
	mdl = ModelManager(prj.project)
	prj.projectCreated.connect(lambda proj: mdl.new_prj(proj))
	prj.projectLoaded.connect(lambda proj: mdl.load_prj(proj))

	prj_tab = QTabWidget()
	prj_tab.addTab(prj, "Project Setup")
	prj_tab.addTab(mdl, "Model")
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
	sys.exit(app.exec())


print("PROGRAM START")
if __name__ == '__main__':
	main()
print("PROGRAM END")
