from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPalette, QColor

from src.components.model_manager import ModelWorkspace

"""
"This is where would the model result\n"
               "and prediction graphs will be.\n"
               "And graphs such as, Error Rate\n"
               "and ML settings like settings\n"
               "each batch size."
"""

class VisualResult(QWidget):
    model: ModelWorkspace = None

    def __init__(self):
        super().__init__()
        self.inst_gui()

    def inst_gui(self):
        base = QHBoxLayout()
        base.addWidget(QLabel("Graphing Available"))
        base.addStretch(2)

        self.setLayout(base)

    def model_update(self, model: ModelWorkspace):
        self.model = model
