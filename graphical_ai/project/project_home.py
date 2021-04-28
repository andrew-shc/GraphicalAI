from PySide6.QtWidgets import *
from PySide6.QtCore import Slot

from file_handler import ProjectFileHandler


class ProjectHomepage(QWidget):
    def __init__(self, fhndl: ProjectFileHandler, parent=None):
        super().__init__(parent=parent)

        lyt_main = QVBoxLayout()
        lyt_main.addWidget(QLabel("Welcome to your new project!"))
        lyt_main.addWidget(QLabel(f"Project name: {fhndl.name}"))

        self.setLayout(lyt_main)
