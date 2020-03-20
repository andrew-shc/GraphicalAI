from __future__ import annotations

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsRectItem

from src.debug import print
from src.gfx.connection import Connection

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

	def __getstate__(self):
		dct = self.__dict__.copy()
		dct.pop("view")
		return dct

	def __setstate__(self, state):
		self.__dict__ = state

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
