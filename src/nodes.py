from src.gfx.node import Node as Node  # type: ignore
from src.gfx.constant_models import *  # type: ignore

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression, LogisticRegression  # type: ignore
from sklearn.cluster import KMeans  # type: ignore
from sklearn.tree import DecisionTreeClassifier  # type: ignore
from sklearn.svm import SVC  # type: ignore

"""
class name suffix:

MDL - Generic Node (can be omitted)
REG - Regression (a continuum result)
CLF - Classifier (a discrete (labeled) result)
GRD - Gradient
NN - Neural Network

"""

class Nodes:
	title = "#[Abstract]"  # back-end oriented
	name = "#[Abstract]"  # user oriented

	@classmethod
	def create(cls, view, pos):
		""" Creates an instance of the node from this custom node class
		:param w:
		:param pos:
		:return:
		"""
		raise NotImplementedError

	@staticmethod
	def execute(inp, const, out, inst) -> dict:
		""" Execute function to execute this node
		:param inp: input dict
		:param const: constant input dict
		:param out: output dict (w/ side effects)
		:param inst: project instance/global variables
		:return: returns a dictionary type for output
		"""
		raise NotImplementedError

	@staticmethod
	def descriptor():
		""" Describes the model
		:return: the text of the description
		"""
		pass


Matrix = "mtx"
ScalarInt = "scl_int"
# class FutureNode:
# 	title = "#[Abstract]"  # back-end oriented
# 	name = "#[Abstract]"  # user oriented
#
# 	@__input__(name="input data", type=Matrix)
# 	def input(self, inp: list) -> Matrix:  # the list comes from all the connection line connecting to this connector
# 		#                          user define custom aggregator to aggregate the list of data or just the first element
# 		dat = sum(inp)
# 		return dat
#
# 	@__input__(name="bias", type=ScalarInt)
# 	def bias(self, inp: list) -> ScalarInt:
# 		dat = inp[0]
# 		return dat
#
# 	@__output__(name="result data", type=ScalarInt)  # can be a final modification for the output
# 	def result(self, out) -> ScalarInt:
# 		dat = int(out)
# 		return dat
#
# 	@__constant__  # define custom widgets for each constant. the returning class must have `value()` method
# 	def mode(self) -> QWidget:
# 		widget = QWidget()
# 		return widget
#
# 	@classmethod
# 	def create(cls, view, pos):
# 		raise NotImplementedError
#
# 	@staticmethod
# 	def execute(inp, const, out, inst) -> dict:
# 		return out
#
# 	@staticmethod
# 	def descriptor():
# 		pass


class CSVInput(Nodes):
	title = "CSVInput"
	name = "Read CSV"

	@classmethod
	def create(cls, view, pos):
		cls.field = {
			"input": [],
			"output": [("x", "type"), ("y", "type")],
			"constant": [("file input", FileDialog()), ("result column", LineInput()), ("transpose", CheckBox()),
			             ("result numerical", CheckBox()), ],
		}
		return Node(view, pos, cls)

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


class CSVOutput(Nodes):
	title = "CSVOutput"
	name = "Write CSV"

	@classmethod
	def create(cls, view, pos):
		cls.field = {
			"input": [("data", "type")],
			"output": [],
			"constant": [("file output", FileDialog()), ("transpose", CheckBox()), ("seperator", LineInput(","))],
		}
		return Node(view, pos, cls)

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


class LinearRegressionREG(Nodes):
	title = "LinearRegression"
	name = "Linear Regression"

	@classmethod
	def create(cls, view, pos):
		cls.field = {
			"input": [("x", "type"), ("y", "type"), ("test", "type")],
			"output": [("result", "type")],
			"constant": [],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = LinearRegression()
		mdl.fit(inp["x"], inp["y"])

		out["result"] = mdl.predict(inp["test"])
		return out


class LogisticRegressionREG(Nodes):
	title = "LogisticRegression"
	name = "Logistic Regression"

	@classmethod
	def create(cls, view, pos):
		cls.field = {
			"input": [("x", "type"), ("y", "type"), ("test", "type")],
			"output": [("result", "type")],
			"constant": [],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = LogisticRegression()
		mdl.fit(inp["x"], inp["y"])

		out["result"] = mdl.predict(inp["test"])
		return out


class KMeansCLF(Nodes):
	title = "KMeans"
	name = "K-Means Cluster"

	@classmethod
	def create(cls, view, pos):
		cls.field = {
			"input": [("x", "type"), ("test", "type")],
			"output": [("result", "type")],
			"constant": [("clusters", LineInput(numerical=True))],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = KMeans(n_clusters=int(const["cluster"]))  # it is assume the LineInput() takes care of integer
		mdl.fit(inp["x"])

		out["result"] = mdl.predict(inp["test"])
		return out


class DecisionTreeCLF(Nodes):
	title = "DecisionTree"
	name = "Std Decision Tree"

	@classmethod
	def create(cls, view, pos):
		cls.field = {
			"input": [("x", "type"), ("y", "type"), ("test", "type")],
			"output": [("result", "type"), ("probability", "type")],
			"constant": [("max depth", LineInput(numerical=True)), ("min samples leaf", LineInput("1", numerical=True)),
			             ("min samples split", LineInput("2", numerical=True))],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = DecisionTreeClassifier(max_depth=int(const["max depth"]), min_samples_leaf=int(const["min samples leaf"]),
		                             min_samples_split=int(const["min samples split"]))
		mdl.fit(inp["x"], inp["y"])

		out["result"] = mdl.predict(inp["test"])
		out["probability"] = mdl.predict_proba(inp["test"])
		return out


class SupportVectorCLF(Nodes):
	title = "SupportVector"
	name = "Support Vector Classifier"

	@classmethod
	def create(cls, view, pos):
		cls.field = {
			"input": [("x", "type"), ("y", "type"), ("test", "type")],
			"output": [("result", "type"), ],
			"constant": [("kernel", Selector({"rbf (default)": "rbf", "linear": "linear",
			                                  "poly": "poly", "sigmoid": "sigmoid"}, default="rbf (default)"))],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = SVC(kernel=const["kernel"])
		mdl.fit(inp["x"], inp["y"])

		out["result"] = mdl.predict(inp["test"])
		return out
