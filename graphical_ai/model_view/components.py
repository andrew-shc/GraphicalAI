from PySide6.QtWidgets import *
from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QPalette, QIntValidator

import math


class InteractiveComponent(QGraphicsProxyWidget):
    def __init__(self, wx: QWidget, size: tuple, parent=None):
        super().__init__(parent=parent)
        self.wx = wx
        self.ctag = self.wx.__class__.__name__

        try:
            self.wx.setMinimumSize(QSize(size[0]-1, size[1]-1))
            self.wx.setMaximumSize(QSize(size[0]-1, size[1]-1))
        except Exception as e:
            print(f"debug: self.wx is {self.wx} with type of {type(self.wx)}")
            print("suggestion: if the type of the self.wx is some internal type, "
                  "check nodes.py file which node is causing this")
            raise e

        self.setWidget(self.wx)

    def value(self):  # values used in execution
        return self.wx.value()

    def serialize(self):
        return self.wx.serialize()

    def deserialize(self, dt):
        self.wx.deserialize(dt)

    def bin_serialize(self) -> bytes:
        sdt = self.wx.bin_serialize()
        if type(sdt) == bytes: return sdt
        else:
            print("debug:", self.wx)
            raise TypeError("debug: binary serialization expected to return bytes")


# def boundingRect(self) -> QRectF:
# 	return QRectF()


class IntLineInput(QLineEdit):
    """
    A single line input where the user can type in arbitrary numbers (integer only line input)
    """

    def __init__(self, default: int, parent=None):
        super().__init__(parent=parent)
        self.setValidator(QIntValidator())

        self.default_num: int = default
        self.setText(str(self.default_num))

    def value(self):
        return int(self.text())

    def serialize(self):
        return self.text()

    def deserialize(self, dt):
        self.setText(dt)

    def bin_serialize(self):
        return int(self.text()).to_bytes(int(math.log2(int(self.text()))//8 + 1), "big")

    @staticmethod
    def bin_deserialize(bdt):
        return int.from_bytes(bdt, "big")


class LineInput(QLineEdit):
    """
    A single line input where the user can type in anything
    """

    def __init__(self, default: str, parent=None):
        super().__init__(parent=parent)

        self.default: str = default
        self.setText(self.default)

    def value(self):
        return self.text()

    def serialize(self):
        return self.text()

    def deserialize(self, dt):
        self.setText(dt)

    def bin_serialize(self):
        if len(self.text()) != 0: return self.text().encode("ASCII")
        else: return b"\x05"  # to signify the input field is empty

    @staticmethod
    def bin_deserialize(bdt):
        if bdt != b"\x05": return bdt.decode("ASCII")
        else: return ""


class ComboBox(QComboBox):
    """
    A combo box where the users can select the pre-defined items of the drop-down list
    """

    def __init__(self, selc: list, parent=None):
        super().__init__(parent=parent)

        self.selc = selc  # selections
        for s in self.selc:
            self.addItem(s)

    def value(self):  # just useless
        return 0

    def serialize(self):
        return self.currentText()

    def deserialize(self, dt):
        self.setCurrentText(dt)

    def bin_serialize(self):
        return self.currentText().encode("ASCII")

    @staticmethod
    def bin_deserialize(bdt):
        return bdt.decode("ASCII")


class CheckBox(QCheckBox):
    """
    A check box where the users can check/toggle
    """

    def __init__(self, default=False, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet("background-color: transparent")

        self.check = default
        if self.check: self.setChecked(Qt.Checked)

    def value(self):
        return 0

    def serialize(self):
        return self.checkState() == Qt.Checked

    def deserialize(self, dt):
        if dt: self.setCheckState(Qt.Checked)
        else: self.setCheckState(Qt.Unchecked)

    def bin_serialize(self):
        return b"\xff" if self.checkState() == Qt.Checked else b"\x00"

    @staticmethod
    def bin_deserialize(bdt):
        if bdt == b"\xff": return True
        else: return False


class VariableSelector(QComboBox):
    """
    A specific type of widget that allows the users to select variables from where variables are defined separately
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def value(self):
        return 0

    def serialize(self):
        return "<None>"

    def deserialize(self, dt):
        print(dt)

    def bin_serialize(self):
        return b"\x00Null"

    @staticmethod
    def bin_deserialize(bdt):
        print(bdt)
        return bdt


class MultiComboBox(QComboBox):
    """
    A combo box that allows users to select multiple options under the combo box
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def value(self):
        return 0

    def serialize(self):
        return "<None>"

    def deserialize(self, dt):
        print(dt)

    def bin_serialize(self):
        return b"\x00Null"

    @staticmethod
    def bin_deserialize(bdt):
        print(bdt)
        return bdt

