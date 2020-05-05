from src.gfx.node import Node as Node
from src.gfx.constant_models import *
from src.components.workspace.connector_type import ConnectorType as CT

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

from tensorflow.keras import models, layers, losses

"""
class name suffix:

MDL - Generic Node (can be omitted)
REG - Regression (a continuum result)
CLF - Classifier (a discrete (labeled) result)
GRD - Gradient
MTX - Matrix manipulator
NN - Neural Network

error types:
Internal Error: Errors that is related to invalid Nodes (this error should be fixed as soon as possible)
External Error: When a user executes an invalid input

"""

class Nodes:
	title = "#[Abstract]"  # back-end oriented
	name = "#[Abstract]"  # user oriented

	@staticmethod
	def create(view, pos, const=None):
		""" Creates an instance of the node from this custom node class
		** NOTE **: Removed this as statimethod from classmethod because the .field attr was storing to the class itself
		            (which had an unintended effect on serialization of node)
		:param view: the graphical object list of the Model Workspace Scene
		:param pos: position of each node
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


class NodeRev2(Nodes):
	title = "#[Abstract]"
	name = "#[Abstract]"

	def inp(self, **kwargs): pass

	def out(self, **kwargs): pass

	def const(self, **kwargs): pass

	@classmethod
	def create(cls, view, pos, **load_const):
		node = cls()

		# replace the underscore with space when users sees it
		node.inp( x=CT.Any, x2=CT.Any, )
		node.out( y=CT.Any, other=CT.Any, file_output=CT.Any, )
		if load_const == {}: node.const( file_input=FileDialog() )
		else: node.const( **load_const )

		return node

	@staticmethod
	def execute(inp, const, out, inst) -> dict:
		out.x = const.file_input()
		return out


# TODO: executor does not read from export, still reads from the usual names here
# class Binding:
# 	Null = None
# 	Constant = None
#
#
# def inp(**kwargs): pass
# def out(**kwargs): pass
# def cns(**kwargs): pass
#
# def node(*args, **kwargs): return node
# class NodeRev3(Nodes):
# 	title = "#[Abstract]"
# 	name = "#[Abstract]"
#
# 	def __getitem__(self, item, **kwargs):
# 		pass
#
# 	def __init__(self, view, pos, **load_const):
# 		self.fieldname = self[inp, CT.Matrix | CT.Int, Binding.Null]
# 		self.fieldname = self[out, CT.Matrix | CT.Any, Binding.Null]
# 		self.constants = self[cns, CT.Any, Binding.Constant]
#
# 	@staticmethod
# 	def execute(inp, const, out, inst) -> dict:
# 		out.x = const.file_input()
# 		return out


class CSVInput(Nodes):
	title = "CSVInput"
	name = "Read CSV"

	@staticmethod
	def create(view, pos, const=None):
		cls = CSVInput()
		cls.field = {
			"input": [],
			"output": [("x", CT.Matrix | CT.Any), ("y", CT.Matrix | CT.Any)],
			"constant": const if const is not None else
				[("file input", FileDialog()), ("result column", LineInput()), ("transpose", CheckBox()),
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

	@staticmethod
	def create(view, pos, const=None):
		cls = CSVOutput()
		cls.field = {
			"input": [("data", CT.Matrix | CT.Any)],
			"output": [],
			"constant": const if const is not None else
			[("file output", FileDialog()), ("transpose", CheckBox()), ("separator", LineInput(","))],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		if isinstance(inp["data"], pd.DataFrame):
			if const["transpose"]: dat = inp["data"].T
			else: dat = inp["data"]
			dat.values.tofile(const["file output"], sep=const["separator"])
		elif isinstance(inp["data"], np.ndarray):
			if const["transpose"]: dat = inp["data"].T
			else: dat = inp["data"]
			dat.tofile(const["file output"], sep=const["separator"])
		else:
			print("[Error]: The type is not supported. Only supports Numpy Arrays and Pandas Dataframe/Series")

		return out


class LinearRegressionREG(Nodes):
	title = "LinearRegression"
	name = "Linear Regression"

	@staticmethod
	def create(view, pos, const=None):
		cls = LinearRegressionREG()
		cls.field = {
			"input": [("x", CT.Matrix | CT.Any), ("y", CT.Matrix | CT.Any), ("test", CT.Matrix | CT.Any)],
			"output": [("result", CT.Matrix | CT.Any)],
			"constant": const if const is not None else [],
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

	@staticmethod
	def create(view, pos, const=None):
		cls = LogisticRegressionREG()
		cls.field = {
			"input": [("x", CT.Matrix | CT.Any), ("y", CT.Matrix | CT.Any), ("test", CT.Matrix | CT.Any)],
			"output": [("result", CT.Matrix | CT.Any)],
			"constant": const if const is not None else [],
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

	@staticmethod
	def create(view, pos, const=None):
		cls = KMeansCLF()
		cls.field = {
			"input": [("x", CT.Matrix | CT.Any), ("test", CT.Matrix | CT.Any)],
			"output": [("result", CT.Matrix | CT.Any)],
			"constant": const if const is not None else [("clusters", LineInput(numerical=True))],
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

	@staticmethod
	def create(view, pos, const=None):
		cls = DecisionTreeCLF()
		cls.field = {
			"input": [("x", CT.Matrix | CT.Any), ("y", CT.Matrix | CT.Any), ("test", CT.Matrix | CT.Any)],
			"output": [("result", CT.Matrix | CT.Any), ("probability", CT.Matrix | CT.Any)],
			"constant": const if const is not None else
			[("max depth", LineInput(numerical=True)), ("min samples leaf", LineInput("1", numerical=True)),
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

	@staticmethod
	def create(view, pos, const=None):
		cls = SupportVectorCLF()
		cls.field = {
			"input": [("x", CT.Matrix | CT.Any), ("y", CT.Matrix | CT.Any), ("test", CT.Matrix | CT.Any)],
			"output": [("result", CT.Matrix | CT.Any), ],
			"constant": const if const is not None else
			[("kernel", Selector({"rbf (default)": "rbf", "linear": "linear", "poly": "poly", "sigmoid": "sigmoid"}, default="rbf (default)"))],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		mdl = SVC(kernel=const["kernel"])
		mdl.fit(inp["x"], inp["y"])

		out["result"] = mdl.predict(inp["test"])
		return out


class InputLayerNN(Nodes):
	title = "InputLayerNN"
	name = "Input Layer NN"

	@staticmethod
	def create(view, pos, const=None):
		cls = InputLayerNN()
		cls.field = {
			"input": [("x", CT.Matrix | CT.Any)],
			"output": [("model", CT.Matrix | CT.Any), ],
			"constant": const if const is not None else
			[("nodes", LineInput(numerical=True)),
			 ("activation", Selector({"Linear": "linear", "Sigmoid": "sigmoid", "ReLU": "relu", "Softmax": "softmax"}))],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		model = models.Sequential()
		model.add(layers.Dense(const["nodes"], input_dim=len(inp["x"].columns), activation=const["activation"]))

		out["model"] = model
		return out


class OutputLayerNN(Nodes):
	title = "OutputLayerNN"
	name = "Output Layer NN"

	@staticmethod
	def create(view, pos, const=None):
		cls = OutputLayerNN()
		cls.field = {
			"input": [("model", CT.Matrix | CT.Any), ],
			"output": [("model", CT.Matrix | CT.Any),],
			"constant": const if const is not None else
			[("loss", Selector({"MSE": "MSE", "MAE": "MAE", "Bin Cross Entropy": "BCE"})),
			 ("optimizer", Selector({"SGD": "sgd", "Adam": "adam"})),
			 ("metrics", Selector({"Accuracy": ["accuracy"]})),
			 ],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		loss = {
			"MSE": losses.mean_squared_error,
			"MAE": losses.mean_absolute_error,
			"BCE": losses.binary_crossentropy,
		}[const["loss"]]

		model = inp["model"]
		model.compile(loss=loss, optimizer=const["optimizer"], metrics=const["metrics"])
		out["model"] = model
		return out


class HiddenLayerNN(Nodes):
	title = "HiddenLayerNN"
	name = "Hidden Layer NN"

	@staticmethod
	def create(view, pos, const=None):
		cls = HiddenLayerNN()
		cls.field = {
			"input": [("model", CT.Matrix | CT.Any), ],
			"output": [("model", CT.Matrix | CT.Any), ],
			"constant": const if const is not None else
			[("nodes", LineInput(numerical=True)),
			 ("activation", Selector({"Linear": "linear", "Sigmoid": "sigmoid", "ReLU": "relu", "Softmax": "softmax"}))],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		model = inp["model"]
		model.add(layers.Dense(const["nodes"], activation=const["activation"]))
		out["model"] = model
		return out


class TrainNN(Nodes):
	title = "TrainNN"
	name = "Training NN"

	@staticmethod
	def create(view, pos, const=None):
		cls = TrainNN()
		cls.field = {
			"input": [("model", CT.Matrix | CT.Any), ("x", CT.Matrix | CT.Any), ("y", CT.Matrix | CT.Any), ("test x", CT.Matrix | CT.Any)],
			"output": [("result", CT.Matrix | CT.Any), ],
			"constant": const if const is not None else
			[("epochs", LineInput(numerical=True)),
			 ("batch size", LineInput(numerical=True)),
			 ("classify", CheckBox())],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		model: models.Sequential = inp["model"]

		print(inp["x"], inp["y"], inp["test x"])
		# casting pandas types to numpy types
		x: np.ndarray = inp["x"].values if isinstance(inp["x"], pd.DataFrame) else inp["x"]
		y: np.ndarray = inp["y"].values if isinstance(inp["y"], pd.Series) else inp["y"]
		test_x: np.ndarray = inp["test x"].values if isinstance(inp["test x"], pd.DataFrame) else inp["test x"]
		print(x.reshape((-1, 150)), y, test_x)

		# when the output variable between the nodes and the dataset is incompatible
		# print(model.layers[-1].output_shape[1], y.shape)
		# if model.layers[-1].output_shape[1] != y.shape[1]:
		# 	return "Error"

		model.fit(x=x, y=y, epochs=const["epochs"], batch_size=const["batch size"])
		# to evaluate the result
		# mdl.evaluate()
		if const["classify"]: res = model.predict_classes(test_x)
		else: res = model.predict(test_x)

		out["result"] = res
		return out


class ConvolutionalLayerMTX(Nodes):
	title = "ConvolutionalLayerMTX"
	name = "Convolutional Layer"

	@staticmethod
	def create(view, pos, const=None):
		cls = ConvolutionalLayerMTX()
		cls.field = {
			"input": [],
			"output": [("input nodes", CT.Matrix | CT.Any), ],
			"constant": const if const is not None else
			[("file name", FileDialog()), ("input", Selector({"row": "row", "column": "column"}))],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		return out


class PoolingMTX(Nodes):
	title = "PoolingMTX"
	name = "Pooling Layer"

	@staticmethod
	def create(view, pos, const=None):
		cls = PoolingMTX()
		cls.field = {
			"input": [],
			"output": [("input nodes", CT.Matrix | CT.Any), ],
			"constant": const if const is not None else
			[("file name", FileDialog()), ("input", Selector({"row": "row", "column": "column"}))],
		}
		return Node(view, pos, cls)

	@staticmethod
	def execute(inp, const, out, inst):
		return out


export = {
	"File": [
		CSVInput,
		CSVOutput
	],
	"Generic": [
		LinearRegressionREG,
		LogisticRegressionREG,
		KMeansCLF,
		DecisionTreeCLF,
		SupportVectorCLF,
	],
	"Neural Network": [
		InputLayerNN,
		OutputLayerNN,
		HiddenLayerNN,
		TrainNN,
		ConvolutionalLayerMTX,
		PoolingMTX,
	],
	"Pre-Processing": [

	]
}
