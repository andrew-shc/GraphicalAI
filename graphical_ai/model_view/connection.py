from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QLineF, QPointF
from PySide6.QtGui import *


class Connection(QGraphicsLineItem):
    def __init__(self, a: QPointF, b: QPointF, parent=None):
        super().__init__(parent=parent)
        self.setPen(QPen("#00CC00"))

        self._a: QPointF = a
        self._b: QPointF = b
        self.setLine(QLineF(self.a, self.b))

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, val: QPointF):
        self._a = val
        self.setLine(QLineF(self.a, self.b))

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, val: QPointF):
        self._b = val
        self.setLine(QLineF(self.a, self.b))


class TempConnection(QGraphicsLineItem):
    def __init__(self, pos, parent=None):
        super().__init__(parent=parent)
        self.setPen(QPen("#FFAA00"))

        self.anchor = pos

        self.setLine(QLineF(self.anchor[0], self.anchor[1], self.anchor[0], self.anchor[1]))

    def drag_line(self, follow_pos):
        self.setLine(QLineF(self.anchor[0], self.anchor[1], follow_pos[0], follow_pos[1]))
