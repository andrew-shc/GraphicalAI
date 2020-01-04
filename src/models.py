from src.model import Model as Model
from src.constant_models import LineInput, FileDialog

from io import StringIO, BytesIO
import pickle

from sklearn import linear_model
import pandas as pd


class GenericModel:
	title = "Generic"  # internal namespace ID
	name = "Generic"  # to be shown on the front-end (user's end)

	@classmethod
	def create(cls, state, w, pos):
		""" Model Creator
			Uses the create() method to create the model.
		return: Model Class
		"""

		# a field should have an input, output, and constant with each of the key having a list of tuple consisting \
		# only the field name and the type of the field
		cls.field = {
			"input": [("input1", "type"), ("input2", "type"), ("input3", "type")],
			"output": [("merge", "type"), ("secondary", "type")],
			"constant": [("isYes", LineInput())],
		}  # NOTE: each model must have a UNIQUE field name

		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		""" Executor StaticMethod
			This is used to execute model data at a different time
		inp: Input Field Data (Constant at Execution Time)
		const: User Input (Constant at Execution Time) Field Data
		out: Output Field Data; to output data
		inst: Project instance settings (e.g. File Location), (Constant at Execution Time)

		return: Output Field Data

		---
		inp.[FIELD NAME]
		const.[FIELD NAME]
		out.[FIELD NAME] = value

		return out
		"""
		out.merge = None
		out.secondary = None
		return out


class FileInput:
	title = "FileInput"
	name = "File Receiver"

	@classmethod
	def create(cls, state, w, pos):
		cls.field = {
			"input": [],
			"output": [("data out", "type")],
			"constant": [("file", FileDialog("open file"))],
		}

		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		out["data out"] = []
		with open(const["file"], "r") as fbj:
			out["data out"] = [ln.strip("\n") for ln in fbj.readlines()]
		return out


class FileOutput:
	title = "FileOutput"
	name = "File Saver"

	@classmethod
	def create(cls, state, w, pos):
		cls.field = {
			"input": [("data in", "type")],
			"output": [],
			"constant": [("file", FileDialog("open file"))],
		}

		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		with open(const["file"], "w") as fbj:
			fbj.writelines([ln+"\n" for ln in inp["data in"]])
		return out


class BFileInput:
	title = "BFileInput"
	name = "Binary File Receiver"

	@classmethod
	def create(cls, state, w, pos):
		cls.field = {
			"input": [],
			"output": [("data out", "type")],
			"constant": [("file", FileDialog("open file"))],
		}

		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		out["data out"] = []
		with open(const["file"], "rb") as fbj:
			out["data out"] = fbj.readlines()
		return out


class BFileOutput:
	title = "BFileOutput"
	name = "Binary File Saver"

	@classmethod
	def create(cls, state, w, pos):
		cls.field = {
			"input": [("data in", "type")],
			"output": [],
			"constant": [("file", FileDialog("open file"))],
		}

		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		with open(const["file"], "wb") as fbj:
			fbj.writelines(inp["data in"])
		return out


class LinearRegression:
	title = "LinearRegression"
	name = "Linear Regression"

	@classmethod
	def create(cls, state, w, pos):
		cls.field = {
			"input": [("input", "list")],
			"output": [("output", "type")],
			"constant": [],
		}

		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):

		df = pd.read_csv( StringIO("\n".join(inp["input"])) )

		result = df['species']
		# print("RES", result)

		data = df.drop('species', axis=1)
		# print("DAT", data)

		model = linear_model.LinearRegression()
		model.fit(data, result)
		# y = mx + b

		result = model.predict([[1, 2, 3, 4]])

		pkl_buf = BytesIO()
		pickle.dump(model, pkl_buf)

		out["output"] = [bytearray(pkl_buf.getvalue())]
		return out
