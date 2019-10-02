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


# Manages all components and system (and entities)
class World:
	ENTITIES = []   # [ENTITY, ENTITY, ENTITY, ...]
	COMPONENT = []  # components registered; for key and index for container
	CONTAINER = []  # [[data, data, ...], [data, ...], ...]; to store data; 2d data array
	SYSTEM = []  # registered systems (i.e. functions)
	GLOBAL = {}  # global variable

	DESTROYING = []  # entities to be destroyed

	"""
	Entities -> Refers to component for data and requirements
	Component -> All the registered components
	System -> All the registered system (or registered functions)
	
	COMPACT STORAGE -> HAS NO KEY, PURE DATA; ORDERED; MORE CPU
	NON-COMPACT STORAGE -> HAS KEYS; ORDERLESS; MORE DATA
	
	Compact storage is the default
	
	EID -> Entity Identification
	"""

	def __init__(self, component, system):
		self.COMPONENT = component
		self.SYSTEM = system
		for _ in component:  # initilize the data space in the container (data 2D array)
			self.CONTAINER.append([])

	# ==== basic function ====

	def create( self, **kwargs ):  # create anew entity
		ID = []  # [0, 3, 4, 5, 2, -1]; -1 means no value for each registered components
		dead = True  # if all the index in the entity is -1 (null pointer)
		for ind, cmpn in enumerate(self.COMPONENT):
			if cmpn in kwargs:
				self.CONTAINER[ind].append(kwargs[cmpn])  # appends the data to the container
				ID.append(len(self.CONTAINER[ind])-1)  # appends the index of that data
				dead = False
			else:
				ID.append(-1)
		if dead:
			self.DESTROYING.append(ID)
		self.ENTITIES.append(ID)  # the index

	def destroy( self, eid ):
		self.ENTITIES.remove(eid)
		self.DESTROYING.append(eid)

	def flush( self ):  # cleans all the dead data in the container
		pass

	def execute( self, func, ):  # executes all the function; the function manages the entities
		self.GLOBAL = func()
		for s in self.SYSTEM:
			s(self.ENTITIES, self.COMPONENT, self.CONTAINER, self.GLOBAL)

	# ==== feature function ====

	def organize( self ):  # organize by components
		pass