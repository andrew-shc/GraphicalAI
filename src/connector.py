from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsRectItem


class Connector(QGraphicsRectItem):
	def __init__(self, dat, rect, parent, tag, en, field):
		super().__init__()

		self.setBrush(Qt.cyan)
		self.setRect(*rect)
		self.dat = dat
		self.dat.rect.append(self)

		self.connectees = []  # the connector that is connecting to this connector
		self.connections = []  # list of line object to render each connection to each connector which corresponds to the self.connectees attribute
		self.parent = parent  # class reference to its parent
		self.tag = tag  # the tag identifies what group this connector is
		self.en = en  # the en attribute is a list of tag (or a specific group) it allows to connect with
		self.field = field  # the field name of the connector

		self.line = self.createLine(QPoint(rect[0]+rect[2]/2, rect[1]+rect[3]/2), QPoint(0, 0), color=Qt.red)
		self.line.hide()

	def mousePressEvent(self, event):
		vp = event.pos()
		sp = self.mapFromItem(self, vp)
		print(self.connections)
		self.line.show()
		self.updateEnd(self.line, sp)

		self.dat.clicked = self
		# self.ungrabMouse()

	def mouseMoveEvent(self, event):
		vp = event.pos()
		sp = self.mapFromItem(self, vp)

		self.line.show()
		self.updateEnd(self.line, sp)

	def mouseReleaseEvent(self, event):
		vp = event.pos()
		sp = self.mapRectToScene(vp.x(), vp.y(), 0, 0)

		for obj in self.dat.rect:
			o = obj.mapRectToScene(obj.rect())  # GLOBAL SCREEN external object rect
			if o.x() < sp.x() < o.x()+o.width() and o.y() < sp.y() < o.y()+o.height() and obj != self.dat.clicked and \
					obj.tag in self.en and obj not in self.connectees:  # {not in} prevents duplicates
				S = self.mapRectToItem(self, self.rect())  # LOCAL SELF self rect
				O = obj.mapRectToItem(self, obj.rect())  # LOCAL SELF external object rect; uses this obj's pos to map instead its own
				self.connectees.append(obj)
				self.connections.append(self.createLine(QPoint(S.x()+S.width()/2, S.y()+S.height()/2),
				                                        QPoint(O.x()+O.width()/2, O.y()+O.height()/2), color=Qt.green))
		self.line.hide()

	# updates the position of the connection (the line that is connecting between the connectors) IF the connector is movable
	def updatePairedPos(self):
		for obj, oline in zip(self.connectees, self.connections):
			O = obj.mapRectToItem(self, obj.rect())
			self.updateEnd(oline, QPoint(O.x()+O.width()/2, O.y()+O.height()/2))

	# creates a line object
	def createLine(self, p1, p2, color=Qt.black) -> QGraphicsLineItem:
		line = QGraphicsLineItem(self)
		line.setPen(color)
		l = line.line()
		l.setP1(p1)
		l.setP2(p2)
		line.setLine(l)
		return line

	# this updates the endpoint (Point #2) of a line object
	def updateEnd(self, line, p2) -> QGraphicsLineItem:
		l = line.line()
		l.setP2(p2)
		line.setLine(l)
		return line
