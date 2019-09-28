"""
Node Notes
==========

When configuring the node
INPUT = {"field name": type}     # input field name and type; "fieldname": type
OUTPUT = {"field name": type}    # output field name and type; "fieldname": type
CONSTANT = {"field name": method}  # user selected data; "fieldname": method (i.e. textInput, dropDown)

When rendering, respectively
_INP = {"field name": []}
_OUT = {"field name": []}
_CNT = {"field name": []}

When executing
INPUT = {"field name": merged data}
OUTPUT = {"field name": merged data}
CONSTANT = {"field name": merged data}
"""


class BaseNode():
	# config
	MODEL_ID = -1  # NO ID
	TITLE = ""
	MULT_INP = True   # there should only be one wire retrieving data from the input
	MULT_OUT = False  # there should only be one wire providing data from the output


	# data
	INPUT = {}
	OUTPUT = {}
	CONSTANT = {}
	_INP = {}
	_OUT = {}
	_CNT = {}

	# place private variables below here for storing data for execution

	# inp: [data, data], out: [data, data]; the parameters are not loc, it is real data
	def execute( self, inp, out ):  # the function gets executed by the project executor
		raise NotImplementedError()

	# custom choice of how to merge multiple inputs
	def mergeInput( self, data: list ):
		return data

# TODO: Do the inp/out type and the constant method
class InputNode(BaseNode):
	MODEL_ID = 0000
	TITLE = "Input"
	INPUT = {}
	OUTPUT = {"data": type}
	CONSTANT = {"filename": "textinput"}

	DATASET = []  # dataset

	def execute( self, inp, out ):
		with open(self.CONSTANT["filename"], "r") as fbj:
			pass

class OutputNode( BaseNode ):
	MODEL_ID = 0000
	TITLE = "Output"
	INPUT = {"data":type}
	CONSTANT = {"filename":"textinput"}

	DATASET = []  # dataset

	def execute( self, inp, out ):
		with open( self.CONSTANT["filename"], "r" ) as fbj:
			pass

class SVCNode( BaseNode ):
	MODEL_ID = 0000
	TITLE = "SVC"
	INPUT = {"label":type, "dataset":type}
	OUTPUT = {"classification":type}
	CONSTANT = {"filename":"textinput"}

	DATASET = []  # dataset

	def execute( self, inp, out ):
		with open( self.CONSTANT["filename"], "r" ) as fbj:
			pass
