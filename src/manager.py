import src.functions as func

class Manager:
	UNIQ_ID = 0

	OBJECTS = {}  # {id:state, id:state, id:state}
	FUNCTION = 0

	def __init__(self):
		self.UNIQ_ID = 0
		self.FUNCTION = func.REG_FUNCTIONS

	def create( self, state, ):  # (initial state w/ dictionary or map)
		if type(state) == dict:
			self.OBJECTS[self.UNIQ_ID] = state
			self.UNIQ_ID += 1
			print( "\033[1;31m DEBUG: ID <\033[0m", id, "\033[1;31m> has been created \033[0m", )
		else:
			print( "\033[1;31m ERROR: <\033[0m", state, "\033[1;31m> has to be dictionary! \033[0m", )
			return 1
		return 0

	def remove( self, id ):  # (id: remove state by id)
		print( "\033[1;31m DEBUG: ID <\033[0m", id, "\033[1;31m> is deleted \033[0m", )
		del self.OBJECTS[ id ]

	def execute( self, event ):  # executes function
		#for key in self.OBJECTS:
		#	print("\033[1;31m#\033[0m", key, "", self.OBJECTS[key],"", end="")
		#print()
		for f in self.FUNCTION:
			f( event=event, obj=self.OBJECTS )
