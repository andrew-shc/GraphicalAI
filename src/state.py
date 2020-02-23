from src.debug import *


class StateHolder:
	def __init__(self, prj=None):

		# connector's global variable for connection
		self.clicked = None
		self.rect = []

		# models data global
		self.model_dt = []

		# project's file interface's project attribute
		self.__project = prj

	@property
	def project(self):
		if self.__project is None:
			print("[STATE] [ERROR] The Project attribute has set to None")
		return self.__project

	@project.setter
	def project(self, proj):
		print("[STATE] The Project attribute is set")
		self.__project = proj

	@project.deleter
	def project(self):
		print("[STATE] The Project attribute is deleted")
		self.__project = None
