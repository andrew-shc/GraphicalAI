from __base__ import *  # ~~~ automatically generated by __autoinject__.py ~~~

from typing import List
from PySide6.QtWidgets import *
from PySide6.QtCore import Slot, Signal, QFile, QCoreApplication
from PySide6.QtGui import QFont, QPixmap, QImageReader

from node_graph.nodes import NodeState


APP_ROOT = "C:/users/andrew shen/desktop/graphicalai-ii"


class IOField(QWidget):
    def __init__(self, attr_nm: str, state: NodeState, parent=None):
        super().__init__(parent=parent)

        lyt_main = QHBoxLayout()

        state_txt = "ERROR TYPE"
        pixmap_label = QLabel()
        if state == NodeState.INPUT:
            state_txt = "Input"
            pixmap_label.setPixmap(QPixmap(APP_ROOT+"/res/arrow-left.png"))
        elif state == NodeState.OUTPUT:
            state_txt = "Output"
            pixmap_label.setPixmap(QPixmap(APP_ROOT+"/res/arrow-right.png"))

        wl_state = QLabel(state_txt)
        qf_state: QFont = wl_state.font()
        qf_state.setBold(True)
        qf_state.setPixelSize(10)
        wl_state.setFont(qf_state)

        wl_attr = QLabel(attr_nm)
        qf_attr: QFont = wl_attr.font()
        qf_attr.setPixelSize(14)
        wl_attr.setFont(qf_attr)

        lyt_left = QVBoxLayout()
        lyt_left.addWidget(wl_state)
        lyt_left.addWidget(wl_attr)

        qcb_opts = QComboBox()
        qcb_opts.addItems(["file", "console"])

        lyt_right = QVBoxLayout()
        lyt_right.addWidget(qcb_opts)

        lyt_main.addLayout(lyt_left)
        lyt_main.addWidget(pixmap_label)
        lyt_main.addLayout(lyt_right)

        self.setLayout(lyt_main)


class ModelIOConfigurator(QListWidget):
    """
    Icons made by "https://www.flaticon.com/authors/flat-icons"
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setStyleSheet("QListWidget::item { border-bottom: 1px solid black; }")
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        a = QListWidgetItem()
        a1 = IOField("node1linreg", NodeState.INPUT)
        self.addItem(a)
        self.setItemWidget(a, a1)
        a.setSizeHint(a1.sizeHint())

        b = QListWidgetItem()
        b1 = IOField("node2linreg", NodeState.OUTPUT)
        self.addItem(b)
        self.setItemWidget(b, b1)
        b.setSizeHint(b1.sizeHint())

        c = QListWidgetItem()
        c1 = IOField("node3linreg", NodeState.INPUT)
        self.addItem(c)
        self.setItemWidget(c, c1)
        c.setSizeHint(c1.sizeHint())

        d = QListWidgetItem()
        d1 = IOField("node4linreg", NodeState.OUTPUT)
        self.addItem(d)
        self.setItemWidget(d, d1)
        d.setSizeHint(d1.sizeHint())

    # TODO: wheel scrolling to quickly, you cant see the lists items are scrolling up or down

    # def wheelEvent(self, e: QWheelEvent) -> None:
    #     # super().wheelEvent(e)
    #     print("WHEEL", e.pixelDelta(), e.angleDelta(), )
    #     self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()+1)


class ConsoleIO(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setLineWrapMode(QTextEdit.NoWrap)
        qf_console: QFont = self.font()
        qf_console.setFamily("Courier New")
        self.setFont(qf_console)

        self.append("LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOONGGGGGGGGGGGGGGGGGGGGGGGGGGGG TEXXXXXXXXXXXXXXXXXXXXT")
