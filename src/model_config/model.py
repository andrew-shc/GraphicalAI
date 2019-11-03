"""

AI Model template data is stored in this file

"""

# example model: f(x)=x+1
class AddModel:
	"""
	/input/ is to define the input fields {FIELD NAME : FIELD TYPE}
	/output/ is to define the output fields {FIELD NAME : FIELD TYPE}
	/const/ is to define the user-defined variables [FIELD CLASSTYPE(PARAM)]
	"""

	inp = {  # input field
		"start_val": None
	}
	out = {  # output field

	}
	const = {  # user defined

	}

	def execute( self, f ):
		pass
