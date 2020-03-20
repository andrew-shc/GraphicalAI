from src.debug import *
from src.gfx.node import Node as Node
from src.gfx.constant_models import *

import sklearn as skl
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

"""
class name suffix:

MDL - Generic Node
REG - Regression (a continuum result)
CLF - Classifier (a discrete (labeled) result)
NN - Neural Network

"""


class CSVInput:
	title = "CSVInput"  # back-end oriented
	name = "Read CSV"  # user oriented

	@classmethod
	def create(cls, w, pos):
		cls.field = {
			"input": [],
			"output": [("x", "type"), ("y", "type")],
			"constant": [("file input", FileDialog()), ("result column", LineInput()), ("transpose", CheckBox()),
			             ("result numerical", CheckBox()), ],
		}
		return Node(w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		# reading into dataframe
		df = pd.read_csv(const["file input"])

		if const["transpose"]: df = df.T
		if const["result numerical"]:
			res_col = int(const["result column"])
		else:
			res_col = const["result column"]

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
	def create(cls, w, pos):
		cls.field = {
			"input": [("data", "type")],
			"output": [],
			"constant": [("file output", FileDialog()), ("transpose", CheckBox()), ("seperator", LineInput(","))],
		}
		return Node(w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		if type(inp["data"]) in [set, dict, list, pd.DataFrame, np.ndarray]:
			dat: pd.DataFrame = pd.DataFrame(inp["data"])  # convert all the listed above data types into pd.Dataframe

			if const["transpose"]: dat = dat.T

			dat.to_csv(const["file output"], sep=const["seperator"])
		else:
			print(
				f"[NODE] [ERROR]: The input type <{type(inp['data'])}> is not part of [<{set}>, <{dict}>, <{list}>, <{pd.DataFrame}>, <{np.ndarray}>,]")
		return out


class LinearRegressionREG:
	title = "LinearRegression"
	name = "Linear Regression"

	@classmethod
	def create(cls, w, pos):
		cls.field = {
			"input": [("x", "type"), ("y", "type"), ("proto", "type")],
			"output": [("result", "type")],
			"constant": [],
		}
		return Node(w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = LinearRegression()
		mdl.fit(inp["x"], inp["y"])

		out["result"] = mdl.predict(inp["proto"])
		return out


class LogisticRegressionREG:
	title = "LogisticRegression"
	name = "Logistic Regression"

	@classmethod
	def create(cls, w, pos):
		cls.field = {
			"input": [("x", "type"), ("y", "type"), ("proto", "type")],
			"output": [("result", "type")],
			"constant": [],
		}
		return Node(w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = LogisticRegression()
		mdl.fit(inp["x"], inp["y"])

		out["result"] = mdl.predict(inp["proto"])
		return out


class KMeansCLF:
	title = "KMeans"
	name = "K-Means Cluster"

	@classmethod
	def create(cls, w, pos):
		cls.field = {
			"input": [("x", "type"), ("proto", "type")],
			"output": [("result", "type")],
			"constant": [("cluster", LineInput(numerical=True))],
		}
		return Node(w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = KMeans(n_clusters=int(const["cluster"]))  # it is assume the LineInput() takes care of integer
		mdl.fit(inp["x"])

		out["result"] = mdl.predict(inp["proto"])
		return out


class DecisionTreeCLF:
	title = "DecisionTree"
	name = "Std Decision Tree"

	@classmethod
	def create(cls, w, pos):
		cls.field = {
			"input": [("x", "type"), ("y", "type"), ("proto", "type")],
			"output": [("result", "type"), ("probability", "type")],
			"constant": [("max depth", LineInput(numerical=True)), ("min samples leaf", LineInput("1", numerical=True)),
			             ("min samples split", LineInput("2", numerical=True))],
		}
		return Node(w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = DecisionTreeClassifier(max_depth=int(const["max depth"]), min_samples_leaf=int(const["min samples leaf"]),
		                             min_samples_split=int(const["min samples split"]))
		mdl.fit(inp["x"], inp["y"])

		out["result"] = mdl.predict(inp["proto"])
		out["probability"] = mdl.predict_proba(inp["proto"])
		return out


class SupportVectorCLF:
	title = "SupportVector"
	name = "Support Vector Classifier"

	@classmethod
	def create(cls, w, pos):
		cls.field = {
			"input": [("x", "type"), ("y", "type"), ("proto", "type")],
			"output": [("result", "type"), ],
			"constant": [("kernel", Selector({"rbf (default)": "rbf", "linear": "linear",
			                                  "poly": "poly", "sigmoid": "sigmoid"}, default="rbf (default)"))],
		}
		return Node(w, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = SVC(kernel=const["kernel"])
		mdl.fit(inp["x"], inp["y"])

		out["result"] = mdl.predict(inp["proto"])
		return out
