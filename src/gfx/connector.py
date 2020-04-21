from __future__ import annotations

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QGraphicsRectItem, QWidget, QStyleOptionGraphicsItem, QGraphicsItem
from PyQt5.QtGui import QPainter, QPolygonF

from src.debug import print
from src.gfx.connection import Connection
from src.components.workspace.connector_type import ConnectorType as CT

from typing import Optional, Tuple

"""
Blue Square = Matrix Type
Red Square = Array/List Type
Green (Semi)Circle = Scalar Type - Numerical

Black Triangle = Misc. Type  (TRY TO MINIMALLY USE MISC. TYPE)
"""

class nConnector(QGraphicsItem):
	def __init__(self, cnc_typ: CT, tag, en, field, view, parent=None):
		super().__init__(parent=parent)
		self.setPos(QPoint(500, 500))
		S = QRect(0,0,10,10)

		self.connections = []  # list of `Connection` class
		self.selector = Connection(QPoint(S.x()+S.width()/2, S.y()+S.height()/2),
		                           QPoint(S.x()+S.width()/2, S.y()+S.height()/2), self, external=None, color=Qt.red)
		self.type = cnc_typ  # connector type
		self.tag = tag  # the tag identifies what group this connector is
		self.en = en  # the en attribute is a list of tag (or a specific group) it allows to connect with
		self.field = field  # the field name of the connector
		self.view = view

		self.polygon = QPolygonF()
		self.polygon << QPoint(-100, 500)
		self.polygon << QPoint(-100, 1000)
		self.polygon << QPoint(200, 1000)
		self.polygon << QPoint(200, 500)

	def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem, widget) -> None:
		painter.setBrush(Qt.cyan)
		painter.drawPolygon(self.polygon)

	def boundingRect(self) -> QtCore.QRectF:
		return QtCore.QRectF(0.0,0.0,2000.0,2000.0)


class hConnector(QGraphicsItem):
	clicked = False

	SIZE = (8, 8)

	CUBE     = 10
	CIRCLE   = 11
	TRIANGLE = 12

	FNAME = 0
	FTYPE = 1

	def __init__(self, pos: QPoint, tag, en, field: Tuple[str, CT], view):
		pos = QPoint(pos.x()+self.SIZE[0], pos.y()+self.SIZE[1])

		super().__init__()
		self.spos = pos  # static position
		self.setPos(pos)

		self.connections = []  # list of `Connection` class
		self.selector = Connection(self.spos, self.spos, self, external=None, color=Qt.red)

		self.tag = tag  # the tag identifies what group this connector is
		self.en = en  # the en attribute is a list of tag (or a specific group) it allows to connect with
		self.field = field  # the field data of the connector (field name, field type)
		self.view = view

		self.selector.hide()

	def _create_polygon(self):
		""" Only draws non-circular figure
		"""
		M = self.spos  # get the center position

		self.polygon = QPolygonF()
		if self.field[hConnector.FTYPE] == CT.Any:
			self.polygon << QPoint(M.x()-self.SIZE[0], M.y()-self.SIZE[1])
			self.polygon << QPoint(M.x()-self.SIZE[0], M.y()+self.SIZE[1])
			self.polygon << QPoint(M.x()+self.SIZE[0], M.y()+self.SIZE[1])
			self.polygon << QPoint(M.x()+self.SIZE[0], M.y()-self.SIZE[1])
		else:
			self.polygon << QPoint(M.x()             , M.y()+self.SIZE[1]/1.5)
			self.polygon << QPoint(M.x()+self.SIZE[0], M.y()                 )
			self.polygon << QPoint(M.x()             , M.y()-self.SIZE[1]/1.5)
			self.polygon << QPoint(M.x()-self.SIZE[0], M.y()                 )

			# self.polygon << QPoint(M.x()-self.SIZE[0], M.y()-self.SIZE[1])
			# self.polygon << QPoint(M.x()-self.SIZE[0], M.y()+self.SIZE[1])
			# self.polygon << QPoint(M.x()+self.SIZE[0], M.y()+self.SIZE[1])
			# self.polygon << QPoint(M.x()+self.SIZE[0], M.y()-self.SIZE[1])

	def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
		if self.field[hConnector.FTYPE] & CT.Int == CT.Int:
			painter.setBrush(Qt.cyan)
		elif self.field[hConnector.FTYPE] & CT.Float == CT.Float:
			painter.setBrush(Qt.blue)
		elif self.field[hConnector.FTYPE] & CT.Bool == CT.Bool:
			painter.setBrush(Qt.red)
		elif self.field[hConnector.FTYPE] & CT.String == CT.String:
			painter.setBrush(Qt.green)
		elif self.field[hConnector.FTYPE] & CT.Any == CT.Any:
			painter.setBrush(Qt.black)

		if self.field[hConnector.FTYPE] & CT.Matrix == CT.Matrix:
			painter.drawPolygon(self.polygon)
		elif self.field[hConnector.FTYPE] & CT.Scalar == CT.Matrix:
			painter.drawEllipse(self.spos, self.SIZE[0], self.SIZE[1])

	def boundingRect(self) -> QtCore.QRectF:
		self._create_polygon()
		return QtCore.QRectF(self.spos.x()-self.SIZE[0]-1,self.spos.y()-self.SIZE[1]-1, self.SIZE[0]*2+1,self.SIZE[1]*2+1)

	# due to the dynamic nature of the geometric shape of the node, this is to set the position at any time
	def set_selector(self):
		# S = self.rect()
		self.view.scene().removeItem(self.selector)  # synchronize items to the `view`
		self.selector = Connection(self.spos, self.spos, self, external=None, color=Qt.red)
		self.selector.hide()

	def mousePressEvent(self, event):
		sp = self.mapFromItem(self, event.pos())

		self.selector.update_end(sp)
		self.selector.show()

	def mouseMoveEvent(self, event):
		sp = self.mapFromItem(self, event.pos())

		# self.selector.show()
		self.selector.update_end(sp)

	def mouseReleaseEvent(self, event):
		sp = self.mapToScene(event.pos())

		obj: hConnector
		for obj in filter(lambda x: isinstance(x, hConnector), self.view.items()):
			is_duplicate = obj in map(lambda x: x.connector_b, self.connections)

			o: QPoint = obj.mapToScene(obj.spos)  # GLOBAL SCREEN external object rect
			if o.x()-obj.SIZE[0] < sp.x() < o.x()+obj.SIZE[0] and o.y()-obj.SIZE[1] < sp.y() < o.y()+obj.SIZE[1] and \
					obj.tag in self.en and not is_duplicate:
				S = self.mapToItem(self, self.spos)
				O = obj.mapToItem(self, obj.spos)

				conc = Connection(S, O, self, obj, color=Qt.green)
				self.connections.append(conc)
		self.selector.hide()


class Connector(QGraphicsRectItem):
	clicked = False

	def __init__(self, rect, tag, en, field, view):
		super().__init__()
		S = self.rect()

		self.setBrush(Qt.cyan)
		self.setRect(*rect)

		self.connections = []  # list of `Connection` class
		self.selector = Connection(QPoint(S.x()+S.width()/2, S.y()+S.height()/2),
		                           QPoint(S.x()+S.width()/2, S.y()+S.height()/2), self, external=None, color=Qt.red)
		self.tag = tag  # the tag identifies what group this connector is
		self.en = en  # the en attribute is a list of tag (or a specific group) it allows to connect with
		self.field = field  # the field name of the connector
		self.view = view

		self.selector.hide()

	# due to the dynamic nature of the geometric shape of the node, this is to set the position at any time
	def set_selector(self):
		S = self.rect()
		self.view.scene().removeItem(self.selector)  # synchronize items to the `view`
		self.selector = Connection(QPoint(S.x()+S.width()/2, S.y()+S.height()/2),
		                           QPoint(S.x()+S.width()/2, S.y()+S.height()/2), self, external=None, color=Qt.red)
		self.selector.hide()

	def mousePressEvent(self, event):
		vp = event.pos()
		sp = self.mapFromItem(self, vp)

		self.selector.update_end(sp)
		self.selector.show()

	def mouseMoveEvent(self, event):
		vp = event.pos()
		sp = self.mapFromItem(self, vp)

		self.selector.show()
		self.selector.update_end(sp)

	def mouseReleaseEvent(self, event):
		vp = event.pos()
		self.sp = self.mapRectToScene(vp.x(), vp.y(), 0, 0)

		for obj in filter(lambda x: isinstance(x, Connector), self.view.items()):
			is_duplicate = obj in map(lambda x: x.connector_b, self.connections)

			o = obj.mapRectToScene(obj.rect())  # GLOBAL SCREEN external object rect
			if o.x() < self.sp.x() < o.x()+o.width() and o.y() < self.sp.y() < o.y()+o.height() and \
					obj.tag in self.en and not is_duplicate:
				S = self.mapRectToItem(self, self.rect())  # LOCAL SELF self rect
				O = obj.mapRectToItem(self, obj.rect())  # LOCAL SELF external object rect; uses this obj's pos to map

				conc = Connection(QPoint(S.x()+S.width()/2, S.y()+S.height()/2),
				                  QPoint(O.x()+O.width()/2, O.y()+O.height()/2), self, obj, color=Qt.green)
				self.connections.append(conc)
		self.selector.hide()
