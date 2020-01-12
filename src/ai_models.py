from src.model import Model as Model
from src.constant_models import LineInput, FileDialog, ModelSelectors
from src.project_file_interface import ProjectFI

from io import StringIO, BytesIO
import pickle

from sklearn import linear_model
import pandas as pd


class FileInput:
	title = "FileInput"
	name = "File Receiver"

	@classmethod
	def create(cls, state, w, pos, proj):
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


class BFileInput:
	title = "BFileInput"
	name = "Binary File Receiver"

	@classmethod
	def create(cls, state, w, pos, proj):
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


class ModelOutput:
	title = "DFileOutput"
	name = "Model Output"

	@classmethod
	def create(cls, state, w, pos, proj: ProjectFI):
		cls.field = {
			"input": [("data in", "type")],
			"output": [],
			"constant": [("tag", LineInput())],
		}

		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		print(inp, const, out, inst)
		inst["project"].write_ai_model(const["tag"], inp["data in"])
		return out


class LinearRegression:
	title = "LinearRegression"
	name = "Linear Regression"

	@classmethod
	def create(cls, state, w, pos, proj):
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


class LogisticRegression:
	title = "LogisticRegression"
	name = "Logistic Regression"

	@classmethod
	def create(cls, state, w, pos, proj):
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

		model = linear_model.LogisticRegression()
		model.fit(data, result)

		# result = model.predict([[1, 2, 3, 4]])

		pkl_buf = BytesIO()
		pickle.dump(model, pkl_buf)

		out["output"] = [bytearray(pkl_buf.getvalue())]
		return out
