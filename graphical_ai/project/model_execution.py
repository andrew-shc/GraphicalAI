from PySide6.QtWidgets import *
from PySide6.QtCore import Slot


class ExecutionPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        lyt_main = QVBoxLayout()
        lyt_main.addWidget(QLabel(
            "Execution page. This will include execute (run) button. I/O runtime configurator/set-up which includes user GUI/console input."))

        self.setLayout(lyt_main)
