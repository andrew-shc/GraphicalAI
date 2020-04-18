from PyQt5.QtWidgets import QMenuBar, QMenu


class CustomMenu(QMenuBar):
    def __init__(self):
        super().__init__()

        menu = QMenu("File")
        menu.addAction("Project")

        file: QMenu = self.addMenu("File")
        file.addAction("New Project")
        file.addAction("Load Project")
        file.addAction("Save Project")
        file.addSeparator()
        file.addAction("Project Settings")
        file.addSeparator()
        file.addAction("New Model Workspace")
        file.addAction("Save Model Workspace")

        file: QMenu = self.addMenu("Add")
        file.addAction("Nodes")

        file: QMenu = self.addMenu("Run")
        file.addAction("Execute Current Model")
