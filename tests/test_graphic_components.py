from src.gfx.connector import Connector
from src.gfx.connection import Connection
from src.gfx.node import Node

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import QPoint, QLineF

def test_connection_selector():
    parent = Connector((0,0,10,10), "TAG_INP", ["TAG_OUT"], ("FIELD_NAME", "FIELD_TYPE"), QGraphicsView)
    cnc = Connection(QPoint(100,100),QPoint(100,100), parent, None)

    assert cnc.connector_a == parent
    assert cnc.connector_b is None

    ln: QLineF = cnc.line()
    assert ln.x1() == ln.x2()
    assert ln.y1() == ln.y2()

    cnc.update_end(QPoint(200,200))
    ln: QLineF = cnc.line()
    assert ln.x1() != ln.x2()
    assert ln.y1() != ln.y2()

    assert ln.x2() == 200
    assert ln.y2() == 200


def test_connection_connectors():  #todo
    parent = Connector((0, 0, 10, 10), "TAG_INP", ["TAG_OUT"], ("FIELD_NAME", "FIELD_TYPE"), QGraphicsView)
    other = Connector((0, 0, 10, 10), "TAG_OUT", ["TAG_INP"], ("FIELD_NAME", "FIELD_TYPE"), QGraphicsView)
    cnc = Connection(QPoint(100,100),QPoint(100,100), parent, other)

    assert cnc.connector_a == parent
    assert cnc.connector_b == other
    assert cnc.connector_a.tag in cnc.connector_b.en


def test_connection_connectors_multiple():
    parent = Connector((0, 0, 10, 10), "TAG_INP", ["TAG_OUT"], ("FIELD_NAME", "FIELD_TYPE"), QGraphicsView)
    other = Connector((0, 0, 10, 10), "TAG_OUT", ["TAG_INP", "TAG_OTHER"], ("FIELD_NAME", "FIELD_TYPE"), QGraphicsView)


def test_connection_connectors_failed():
    parent = Connector((0, 0, 10, 10), "TAG_INP", ["TAG_OUT"], ("FIELD_NAME", "FIELD_TYPE"), QGraphicsView)
    other = Connector((0, 0, 10, 10), "TAG_OUT", ["TAG_OTHER_A", "TAG_OTHER_B"], ("FIELD_NAME", "FIELD_TYPE"), QGraphicsView)

