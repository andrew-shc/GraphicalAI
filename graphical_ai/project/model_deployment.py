from PySide6.QtWidgets import *
from PySide6.QtCore import Slot


class DeploymentPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        lyt_main = QVBoxLayout()
        lyt_main.addWidget(QLabel(
            "Model deployment page. Running configs to produce a deployable model through programming languages and some other ways."))

        self.setLayout(lyt_main)
