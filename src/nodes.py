from src.debug import *
from src.gfx.model import Model as Model
from src.gfx.constant_models import LineInput, FileDialog, CheckBox, ModelSelectors

import sklearn as skl
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans


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
		mdl = LinearRegression()
		mdl.fit(inp["x"], inp["y"])

		out["result"] = mdl.predict(inp["test"])
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
		mdl = LogisticRegression()
		mdl.fit(inp["x"], inp["y"])

		out["result"] = mdl.predict(inp["test"])
		return out


class KMeansMDL:
	title = "KMeans"
	name = "K-Means Cluster"

	@classmethod
	def create(cls, state, w, pos):
		cls.field = {
			"input": [("x", "type"), ("test", "type")],
			"output": [("result", "type")],
			"constant": [("cluster", LineInput(numerical=True))],
		}
		return Model(state, w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = KMeans(n_clusters=int(const["cluster"]))  # it is assume the LineInput() takes care of integer
		mdl.fit(inp["x"])

		out["result"] = mdl.predict(inp["test"])
		return out