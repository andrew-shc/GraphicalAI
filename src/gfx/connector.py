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

class Connector(QGraphicsItem):
	clicked = False

	SIZE = (8, 8)

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

	def __del__(self):
		# removes all the connection referring to this Connector class
		self.view.scene().removeItem(self.selector)
		cnntn: Connection
		[self.view.scene().removeItem(cnntn) for cnntn in self.connections]
		del self.connections[:]

	def _create_polygon(self):
		""" Only draws non-circular figure
		"""
		M = self.spos  # get the center position

		self.polygon = QPolygonF()
		if self.field[Connector.FTYPE] & CT.Optional == CT.Optional:  # Excotic Shape - means special wrapper type
			self.polygon << QPoint(M.x()-self.SIZE[0]    , M.y()-self.SIZE[1])
			self.polygon << QPoint(M.x()-self.SIZE[0]*0.6, M.y())
			self.polygon << QPoint(M.x()-self.SIZE[0]    , M.y()+self.SIZE[1])
			self.polygon << QPoint(M.x()+self.SIZE[0]*1.2, M.y()+self.SIZE[1])
			self.polygon << QPoint(M.x()+self.SIZE[0]*0.6, M.y()             )
			self.polygon << QPoint(M.x()+self.SIZE[0]*1.2, M.y()-self.SIZE[1])
		elif self.field[Connector.FTYPE] & CT.Matrix == CT.Matrix:  # Cube
			self.polygon << QPoint(M.x()-self.SIZE[0], M.y()-self.SIZE[1])
			self.polygon << QPoint(M.x()-self.SIZE[0], M.y()+self.SIZE[1])
			self.polygon << QPoint(M.x()+self.SIZE[0], M.y()+self.SIZE[1])
			self.polygon << QPoint(M.x()+self.SIZE[0], M.y()-self.SIZE[1])
		elif self.field[Connector.FTYPE] & CT.Any == CT.Any:  # Triangle
			self.polygon << QPoint(M.x()             , M.y()+self.SIZE[1]/1.5)
			self.polygon << QPoint(M.x()+self.SIZE[0], M.y()                 )
			self.polygon << QPoint(M.x()             , M.y()-self.SIZE[1]/1.5)
			self.polygon << QPoint(M.x()-self.SIZE[0], M.y()                 )

			# self.polygon << QPoint(M.x()-self.SIZE[0], M.y()-self.SIZE[1])
			# self.polygon << QPoint(M.x()-self.SIZE[0], M.y()+self.SIZE[1])
			# self.polygon << QPoint(M.x()+self.SIZE[0], M.y()+self.SIZE[1])
			# self.polygon << QPoint(M.x()+self.SIZE[0], M.y()-self.SIZE[1])

	def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
		if self.field[Connector.FTYPE] & CT.Int == CT.Int:         painter.setBrush(Qt.cyan)
		elif self.field[Connector.FTYPE] & CT.Float == CT.Float:   painter.setBrush(Qt.blue)
		elif self.field[Connector.FTYPE] & CT.Bool == CT.Bool:     painter.setBrush(Qt.red)
		elif self.field[Connector.FTYPE] & CT.String == CT.String: painter.setBrush(Qt.green)
		elif self.field[Connector.FTYPE] & CT.Any == CT.Any:       painter.setBrush(Qt.black)

		if self.field[Connector.FTYPE] & CT.Optional == CT.Optional:
			painter.drawPolygon(self.polygon)
		elif self.field[Connector.FTYPE] & CT.Matrix == CT.Matrix:
			painter.drawPolygon(self.polygon)
		elif self.field[Connector.FTYPE] & CT.Scalar == CT.Scalar:
			painter.drawEllipse(self.spos, self.SIZE[0], self.SIZE[1])
		else:  # if no wrapper type was turned in, it will assume its a Scalar
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

		obj: Connector
		for obj in filter(lambda x: isinstance(x, Connector), self.view.items()):
			is_duplicate = obj in map(lambda x: x.connector_b, self.connections)

			o: QPoint = obj.mapToScene(obj.spos)  # GLOBAL SCREEN external object rect
			if o.x()-obj.SIZE[0] < sp.x() < o.x()+obj.SIZE[0] and o.y()-obj.SIZE[1] < sp.y() < o.y()+obj.SIZE[1] and \
					obj.tag in self.en and not is_duplicate:
				S = self.mapToItem(self, self.spos)
				O = obj.mapToItem(self, obj.spos)

				conc = Connection(S, O, self, obj, color=Qt.green)
				self.connections.append(conc)
		self.selector.hide()

