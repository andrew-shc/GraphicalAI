from src.debug import *
from src.gfx.model import Model as Model
from src.gfx.constant_models import LineInput, FileDialog, CheckBox, ModelSelectors
from src.project_file_interface import ProjectFI

from io import StringIO, BytesIO
import pickle

import sklearn as skl
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression


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


# class LinearRegression:
# 	title = "LinearRegression"
# 	name = "Linear Regression"
#
# 	@classmethod
# 	def create(cls, state, w, pos):
# 		cls.field = {
# 			"input": [("input", "list")],
# 			"output": [("output", "type")],
# 			"constant": [],
# 		}
#
# 		return Model(state, w, pos, cls)
#
# 	@staticmethod
# 	def execute(inp, const, out, inst):
#
# 		df = pd.read_csv( StringIO("\n".join(inp["input"])) )
#
# 		result = df['species']
# 		# print("RES", result)
#
# 		data = df.drop('species', axis=1)
# 		# print("DAT", data)
#
# 		model = linear_model.LinearRegression()
# 		model.fit(data, result)
# 		# y = mx + b
#
# 		result = model.predict([[1, 2, 3, 4]])
#
# 		pkl_buf = BytesIO()
# 		pickle.dump(model, pkl_buf)
#
# 		out["output"] = [bytearray(pkl_buf.getvalue())]
# 		return out


class LogisticRegression:
	title = "LogisticRegression"
	name = "Logistic Regression"

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

		model = linear_model.LogisticRegression()
		model.fit(data, result)

		# result = model.predict([[1, 2, 3, 4]])

		pkl_buf = BytesIO()
		pickle.dump(model, pkl_buf)

		out["output"] = [bytearray(pkl_buf.getvalue())]
		return out

class CSVInputFormatter:
	title = "CSVInputFormatter"
	name = "CSV Parser"

	@classmethod
	def create(cls, state, w, pos):
		cls.field = {
			"input": [],
			"output": [("Y", "type"), ("X", "type")],
			"constant": [("file name", FileDialog()), ("transpose", CheckBox())],
		}
		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		print("transpose", const["transpose"])

		FILE_NAME = "iris.csv"
		RESULT_COLUMN = "5"  # the result name for the header on column
		TRANSPOSE = True
		NUMBER = True

		# reading into dataframe
		df = pd.read_csv(const["file name"])

		if TRANSPOSE: df = df.T
		if NUMBER: RESULT_COLUMN = int(RESULT_COLUMN)

		# result
		result = df[RESULT_COLUMN]

		# data
		data = df.drop(RESULT_COLUMN, axis=1)

		print(result)
		print(data)

		out["output"] = 0
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


class PredictValue:
	title = "PredictValue"
	name = "Predict Value"

	@classmethod
	def create(cls, state, w, pos):
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



####################################################


class CSVInput:
	title = "CSVInput"
	name = "Read CSV"

	@classmethod
	def create(cls, state, w, pos):
		cls.field = {
			"input": [],
			"output": [("x", "type"), ("y", "type")],
			"constant": [("file input", FileDialog()), ("result column", LineInput()), ("transpose", CheckBox()), ("result numerical", CheckBox()),],
		}
		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		# reading into dataframe
		df = pd.read_csv(const["file input"])

		if const["transpose"]: df = df.T
		if const["result numerical"]: res_col = int(const["result column"])
		else: res_col = const["result column"]

		# result
		if res_col != "":
			y = df[res_col]
		else:
			y = None

		# data
		if res_col != "":
			x = df.drop(res_col, axis=1)
		else:
			x = df

		out["x"] = x
		out["y"] = y

		return out


class CSVOutput:
	title = "CSVOutput"
	name = "Write CSV"

	@classmethod
	def create(cls, state, w, pos):
		cls.field = {
			"input": [("data", "type")],
			"output": [],
			"constant": [("file output", FileDialog()), ("transpose", CheckBox()), ("seperator", LineInput(","))],
		}
		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		if type(inp["data"]) in [set, dict, list, pd.DataFrame, np.ndarray]:
			dat: pd.DataFrame = pd.DataFrame(inp["data"])  # convert all the listed above data types into pd.Dataframe

			if const["transpose"]: dat = dat.T

			dat.to_csv(const["file output"], sep=const["seperator"])
		else:
			print(f"[NODE] [ERROR]: The input type <{type(inp['data'])}> is not part of [<{set}>, <{dict}>, <{list}>, <{pd.DataFrame}>, <{np.ndarray}>,]")
		return out


class LinearRegressionMDL:
	title = "LinearRegression"
	name = "Linear Regression"

	@classmethod
	def create(cls, state, w, pos):
		cls.field = {
			"input": [("x", "type"), ("y", "type"), ("test", "type")],
			"output": [("result", "type")],
			"constant": [],
		}
		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		print(inp)
		print(const)

		mdl = LinearRegression()
		mdl.fit(inp["x"], inp["y"])

		print(inp["test"])
		out["result"] = mdl.predict(inp["test"]) #const["test input file"])

		return out


class LogisticRegressionMDL:
	title = "LogisticRegression"
	name = "Logistic Regression"

	@classmethod
	def create(cls, state, w, pos):
		cls.field = {
			"input": [("x", "type"), ("y", "type"), ("test", "type")],
			"output": [("result", "type")],
			"constant": [],
		}
		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		print(inp)
		print(const)

		mdl = LogisticRegression()
		mdl.fit(inp["x"], inp["y"])

		print(inp["test"])
		out["result"] = mdl.predict(inp["test"]) #const["test input file"])

		return out