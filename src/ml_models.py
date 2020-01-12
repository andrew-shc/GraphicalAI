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


class FileOutput:
	title = "FileOutput"
	name = "File Saver"

	@classmethod
	def create(cls, state, w, pos, proj):
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


class BFileOutput:
	title = "BFileOutput"
	name = "Binary File Saver"

	@classmethod
	def create(cls, state, w, pos, proj):
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

class ModelInput:
	title = "DFileInput"
	name = "Model Inputs"

	@classmethod
	def create(cls, state, w, pos, proj: ProjectFI):
		cls.field = {
			"input": [],
			"output": [("model", "type")],
			"constant": [( "tag", ModelSelectors(proj.project_dat["model"]["tag"]) )],
		}

		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		out["model"] = inst["project"].read_models(const["tag"])
		return out


class PredictValue:
	title = "PredictValue"
	name = "Predict Value"

	@classmethod
	def create(cls, state, w, pos, proj):
		cls.field = {
			"input": [("model", "binary"), ("test data", "type")],
			"output": [("output", "type")],
			"constant": [],
		}
		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		print(inp, const, out, inst)

		mdl = pickle.loads(b"".join(inp["model"][0]))
		test_val = [int(i) for i in inp["test data"][0].split(" ")]

		result = mdl.predict([test_val])
		print(result)

		out["output"] = [str(result[0])]
		return out
