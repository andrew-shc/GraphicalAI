from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt5.QtCore import Qt, QRectF, QPointF


class WorkspaceScene(QGraphicsScene):
    def __init__(self, *args, **kwargs):
        self.clicked = False
        super().__init__(*args, **kwargs)


class WorkspaceView(QGraphicsView):
    def __init__(self, scene: WorkspaceScene):
        self.clicked = False
        self.shift = False  # uses to move the view when pressing shift (on-trigger) with mouse right-click (continuous)
        self.prev_pos = QPointF(0.0, 0.0)

        super().__init__(scene)
        self.area = self.scene().sceneRect()  # internal rect area

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("background-color: #FFFFFF")

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        QGraphicsView.keyPressEvent(self, event)
        if event.key() == Qt.Key_Shift: self.shift = True

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        QGraphicsView.keyReleaseEvent(self, event)
        if self.shift: self.shift = False

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        QGraphicsView.mousePressEvent(self, event)
        if self.shift and event.button() == Qt.LeftButton:
            self.clicked = True
            self.prev_pos = event.pos()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        QGraphicsView.mouseMoveEvent(self, event)
        if self.clicked:
            dp = self.prev_pos-event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()+int(dp.x()))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value()+int(dp.y()))
            rect = self.sceneRect()
            self.scene().setSceneRect(QRectF(
                rect.x()+dp.x(), rect.y()+dp.y(),
                rect.width(), rect.height()
            ))

            self.prev_pos = event.pos()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        QGraphicsView.mouseReleaseEvent(self, event)
        if event.button() == Qt.LeftButton:
            self.clicked = False
            self.prev_pos = event.pos()

