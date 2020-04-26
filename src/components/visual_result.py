from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPalette, QColor

from src.components.model_manager import ModelWorkspace
from src.components.graphs import *

import pandas as pd

class VisualResult(QWidget):
    model: ModelWorkspace = None

    def __init__(self):
        super().__init__()
        self.inst_gui()

    def inst_gui(self):
        base = QVBoxLayout()
        base.addWidget(QLabel("Graph Testing v0.1"))
        base.addStretch(2)

        df = pd.read_csv("iris.csv")
        df = df.drop("species", axis=1)

        cv = MplLinearReg(5, 5, dpi=100)
        cv.plot_data(df)
        for row in cv.graphs:
            for graph in row:
                base.addWidget(graph)

        self.setLayout(base)

    def model_update(self, model: ModelWorkspace):
        self.model = model
