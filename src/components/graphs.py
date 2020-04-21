import matplotlib as mpl
mpl.use("Qt5Agg")

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as MplQTCanvas
from matplotlib.figure import Figure
from matplotlib import axes
import numpy as np
import pandas as pd


class GraphType:
    LINE = 0xF0
    DOTS = 0xF1


class MplSimpleLinearReg(MplQTCanvas):
    def __init__(self, title: str, width=5, height=4, dpi=100):
        self.title = title

        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.suptitle(title)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

    def plot_data(self, data: pd.Series, *, bias: float, result: float,
                  ylabel="", xlabel="", disp_typ: GraphType = GraphType.LINE):
        """
        :param data: The training data
        :param result: The resulting weight of the regression
        :param disp_typ: How to display the result
        """
        marker = {
            GraphType.LINE: "b-",
            GraphType.DOTS: "b.",
        }[disp_typ]

        self.axes.plot(range(data.size), data, marker)
        self.axes.plot(range(data.size), [i*result+bias for i in range(data.size)], "r-")



class MplLinearReg(MplQTCanvas):
    def __init__(self, width, height, parent=None, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.graphs = [[]]  # a list of internal graphs for multi-variables
        super().__init__(fig)

    def plot_data(self, data: pd.DataFrame):
        # print(len(data), data)
        # print([i for i in data.columns])
        # print(data['sepal_length'])
        # print(type(data['sepal_length']))
        graph = MplSimpleLinearReg("sepal_length")
        graph.plot_data(data['sepal_length'], bias=3, result=0.02)
        graph2 = MplSimpleLinearReg("sepal_width")
        graph2.plot_data(data['sepal_width'], bias=4, result=0.01)
        self.graphs = [[graph, graph2]]
        # self.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

