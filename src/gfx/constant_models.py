from PyQt5.QtWidgets import *
from PyQt5.Qt import QValidator, QIntValidator, QDoubleValidator

import os.path

from src.debug import *


class ConstantModels:
	def __init__(self): pass

	def value(self): pass  # used in retrieving value for execution purpose; for *.exec.dat
	def save(self): pass  # used in serializing the class; for *.proj.dat
	def load(self): pass  # use for deserializing the data into class; for *.proj.dat


class LineInput(QLineEdit):
	def __init__(self, *args, numerical=False):
		super().__init__(*args)
		self.setStyleSheet("background: rgb(255, 255, 255);")
		self.numerical = numerical

		if self.numerical:
			self.setValidator(QIntValidator())
			self.setStyleSheet("background: rgb(225, 255, 225);")

	def value(self):
		return self.text()

	def save(self):
		return {"numerical": self.numerical, "text": self.text()}

	@staticmethod
	def load(dat):
		ln = LineInput(numerical=dat["numerical"])
		ln.setText(dat["text"])
		return ln


class FileDialog(QPushButton):
	def __init__(self, *args, single=True):
		super().__init__(*args)
		self.url = ""
		self.single = single  # store only a single file's directory url

		self.clicked.connect(lambda checked: self.onClick(checked))

		self.file_dialog = None

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
			if self.file_dialog is None: print("WARNING: NO FILES SELECTED")
			elif len(self.file_dialog.selectedFiles()) == 0:
				print("WARNING: NO FILES SELECTED")
			elif self.single and len(self.file_dialog.selectedFiles()) > 0:
				return self.file_dialog.selectedFiles()[0]
			else:
				return self.file_dialog.selectedFiles()
		print("WARNING: NO FILES SELECTED")
		return ""

	def save(self):
		return {"single": self.single, "url": self.url, "text": self.text()}

	@staticmethod
	def load(dat):
		obj = FileDialog(single=dat["single"])
		obj.url = dat["url"]
		obj.setText(dat["text"])
		return obj


class Selector(QComboBox):
	def __init__(self, tags: dict, default=None):
		super().__init__(parent=None)
		self.tag = ""
		self.tags = tags
		self.default = default

		[self.addItem(self.tags[t]) for t in self.tags]

		if self.default is not None:
			self.tag = self.tags[self.default]

		self.textActivated.connect(lambda s: self.setTag(s))

	def setTag(self, s):
		self.tag = s

	def value(self):
		return self.tag

	def save(self):
		return {"tag": self.tag, "tags": self.tags, "default": self.default}

	@staticmethod
	def load(dat):
		obj = Selector(dat["tags"], default=dat["default"])
		obj.tag = dat["tag"]
		return obj


class CheckBox(QCheckBox):
	def __init__(self):
		super(CheckBox, self).__init__()

	def value(self):
		return self.isChecked()

	def save(self):
		return {"checked": self.isChecked()}

	@staticmethod
	def load(dat):
		obj = CheckBox()
		obj.setChecked(dat["checked"])
		return obj
