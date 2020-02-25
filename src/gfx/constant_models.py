from PyQt5.QtWidgets import *
from PyQt5.Qt import QValidator, QIntValidator, QDoubleValidator

import os.path

from src.debug import *

class LineInput(QLineEdit):
	def __init__(self, *args, numerical=False):
		super().__init__(*args)
		self.setStyleSheet("background: rgb(255, 255, 255);")

		if numerical:
			self.setValidator(QIntValidator())
			self.setStyleSheet("background: rgb(225, 255, 225);")

	def value(self):
		return self.text()

class FileDialog(QPushButton):
	def __init__(self, *args, single=True):
		super().__init__(*args)
		self.url = ""
		self.single = single  # store only a single file's directory url

		self.clicked.connect(lambda checked: self.onClick(checked))

	def onClick(self, clicked):
		self.configDialog()

	def configDialog(self):
		self.wind = QMainWindow()
		self.wind.setWindowTitle("File Dialogue")
		self.wind.setGeometry(0, 0, 1000, 400)

		self.file_dialog = QFileDialog()
		self.file_dialog.setFileMode(self.file_dialog.ExistingFile)
		self.file_dialog.setViewMode(self.file_dialog.List)

		self.file_dialog.filesSelected.connect(lambda url: self.setUrl(url))

		self.wind.setMenuWidget(self.file_dialog)
		self.wind.show()

	def setUrl(self, url):
		self.url = url
		self.setText(os.path.basename(self.url[0]))
		self.wind.close()  # closes the window

	def value(self):
		if hasattr(self, "file_dialog"):
			if len(self.file_dialog.selectedFiles()) == 0:
				print("WARNING: NO FILES SELECTED")
			elif self.single and len(self.file_dialog.selectedFiles()) > 0: return self.file_dialog.selectedFiles()[0]
			else: return self.file_dialog.selectedFiles()
		print("WARNING: NO FILES SELECTED")
		return ""


class Selector(QComboBox):
	def __init__(self, tags: dict, default=None):
		super().__init__(parent=None)
		self.tag = ""

		[self.addItem(tags[t]) for t in tags]

		if default is not None:
			self.tag = tags[default]

		self.textActivated.connect(lambda s: self.setTag(s))

	def setTag(self, s):
		self.tag = s

	def value(self):
		return self.tag


class CheckBox(QCheckBox):
	def __init__(self):
		super(CheckBox, self).__init__()

	def value(self):
		return self.isChecked()
