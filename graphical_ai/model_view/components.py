from PySide6.QtWidgets import *
from PySide6.QtCore import QRectF, QSize, Qt
from PySide6.QtGui import QPalette, QIntValidator


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

    def bin_serialize(self):
        return self.wx.bin_serialize()

    def bin_deserialize(self, bdt):
        self.wx.bin_deserialize(bdt)

# def boundingRect(self) -> QRectF:
# 	return QRectF()


class IntLineInput(QLineEdit):
    """
    A single line input where the user can type in arbitrary numbers (integer only line input)
    """

    def __init__(self, default: int, parent=None):
        super().__init__(parent=parent)
        self.setValidator(QIntValidator())

        self.num: int = default

    def value(self):
        return 0

    def serialize(self):
        return "<None>"

    def deserialize(self, dt):
        print(dt)

    def bin_serialize(self):
        return b"\x00Null"

    def bin_deserialize(self, bdt):
        print(bdt)


class LineInput(QLineEdit):
    """
    A single line input where the user can type in anything
    """

    def __init__(self, default: str, parent=None):
        super().__init__(parent=parent)

        self.text: str = default
        self.setText(self.text)

    def value(self):
        return 0

    def serialize(self):
        return "<None>"

    def deserialize(self, dt):
        print(dt)

    def bin_serialize(self):
        return b"\x00Null"

    def bin_deserialize(self, bdt):
        print(bdt)


class ComboBox(QComboBox):
    """
    A combo box where the users can select the pre-defined items of the drop-down list
    """

    def __init__(self, selc: list, parent=None):
        super().__init__(parent=parent)

        self.selc = selc  # selections
        for s in self.selc:
            self.addItem(s)

    def value(self):
        return 0

    def serialize(self):
        return "<None>"

    def deserialize(self, dt):
        print(dt)

    def bin_serialize(self):
        return b"\x00Null"

    def bin_deserialize(self, bdt):
        print(bdt)


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
        return "<None>"

    def deserialize(self, dt):
        print(dt)

    def bin_serialize(self):
        return b"\x00Null"

    def bin_deserialize(self, bdt):
        print(bdt)


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

    def bin_deserialize(self, bdt):
        print(bdt)


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

    def bin_deserialize(self, bdt):
        print(bdt)

