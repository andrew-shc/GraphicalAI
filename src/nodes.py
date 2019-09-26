class BaseNode():
	MODEL_ID = 0000
	INPUT = {}  # input field name and type
	OUTPUT = {}  # output field name and type

	# inp: [data, data], out: [data, data]; the parameters are not loc, it is real data
	def execute( self, inp, out ):  # the function gets executed by the project executor
		raise NotImplementedError()


class InputNode():
	pass