# from __future__ import annotations

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsView

from typing import Optional

# from src.gfx.connector import Connector

class Connection(QGraphicsLineItem):
	def __init__(self, p1: QPoint, p2: QPoint, parent: 'Connector', external: Optional['Connector'], color=Qt.black):
		# Selector Connection (cnc_a: Cnc, cnc_b: None); appears when the line follows the cursor waiting to be selected
		# Connector Connection (cnc_a: Cnc, cnc_b: Cnc); appears as when a line connects from one end to another end

		super().__init__(parent)

		self.connector_a = parent  # parent; internal connector
		self.connector_b = external  # connectee; external connector

		self.setPen(color)
		l = self.line()
		l.setP1(p1)
		l.setP2(p2)
		self.setLine(l)

	def update_end(self, p2):
		l = self.line()
		l.setP2(p2)
		self.setLine(l)

	# updates the position of the connection (the line that is connecting between the connectors) IF the connector is movable
	def update_pair(self):
		O = self.connector_b.mapToItem(self.connector_a, self.connector_b.spos)
		self.update_end(O)
