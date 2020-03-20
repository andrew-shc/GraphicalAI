# from __future__ import annotations

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsView

from typing import Optional

# from src.gfx.connector import Connector

class Connection(QGraphicsLineItem):  # This is an instance class, not a manager class
	def __init__(self, p1, p2, parent: 'Connector', external: Optional['Connector'], color=Qt.black):
		super().__init__(parent)

		self.connector_a = parent  # parent; internal connector
		self.connector_b = external  # connectee; external connector

		self.setPen(color)
		l = self.line()
		l.setP1(p1)
		l.setP2(p2)
		self.setLine(l)

	def __getstate__(self):
		dct = self.__dict__.copy()
		return dct

	def __setstate__(self, state):
		super().__init__()
		self.__dict__ = state

	def update_end(self, p2):
		l = self.line()
		l.setP2(p2)
		self.setLine(l)

	# updates the position of the connection (the line that is connecting between the connectors) IF the connector is movable
	def update_pair(self):
		O = self.connector_b.mapRectToItem(self.connector_a, self.connector_b.rect())
		self.update_end(QPoint(O.x()+O.width()/2, O.y()+O.height()/2))

