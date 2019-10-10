"""
issue stage 1 -> find possible bug outcomes
issue stage 2 -> standard debugger method: print, exec, assert ...
issue stage 3 -> quarantine the buggy code into a seperate file; stripping all unrelated to bug for further investigation
issue stage 4 -> use the debugger software; possible bug report for the respective language

===

github issue tracker:

"""



# Manages all components and system (and entities)
class World:
	ENTITIES = []  # [ENTITY, ENTITY, ENTITY, ...]
	COMPONENT = []  # components registered; for key and index for container
	CONTAINER = []  # [[data, data, ...], [data, ...], ...]; to store data; 2d data array
	SYSTEM = []  # registered systems (i.e. functions)
	GLOBAL = {}  # global variable

	def __init__( self, component, system ):
		self.COMPONENT = component
		self.SYSTEM = system
		for _ in component:  # initilize the data space in the container (data 2D array)
			self.CONTAINER.append( [] )

	# ==== basic function ====

	def create( self, **kwargs ):  # create anew entity
		ID = []  # [0, 3, 4, 5, 2, -1]; -1 means no value for each registered components
		dead = True  # if all the index in the entity is -1 (null pointer)
		for ind, cmpn in enumerate( self.COMPONENT ):
			if cmpn in kwargs:
				self.CONTAINER[ind].append( kwargs[cmpn] )  # appends the data to the container
				ID.append( len( self.CONTAINER[ind] )-1 )  # appends the index of that data
				dead = False
			else:
				ID.append( -1 )
		if dead:
			self.DESTROYING.append( ID )
		self.ENTITIES.append( ID )  # the index

	def execute( self, func, ):  # executes all the function; the function manages the entities
		self.GLOBAL = func()
		for s in self.SYSTEM:
			"""
			:param ent: entity list
			:param cmpnt: components type list
			:param glbl: world-global data list
			"""
			s( self, self.GLOBAL )

	# ==== feature function ====

	def entity( self, cmpn ):  # get entity by list of components

		# translates requested string components to translated required id
		ID_KEY = map( lambda c:0 if c not in cmpn else 1, self.COMPONENT )
		print( "main ky", [i for i in ID_KEY] )
		print( "main ky 2", [i for i in ID_KEY] )
		MATCHED = []  # entity passed the requirement
		for entity in self.ENTITIES:
			REQUESTED = True
			print( "ent:", entity )
			print( "key:", [i for i in ID_KEY] )
			print( "zip:", [i for i in zip( ID_KEY, entity )] )
			for id, c in zip( ID_KEY, entity ):
				print( "idc", id, c )
				if id == 1 and c == -1:
					REQUESTED = False
					print( "BREAK" )
					break
			if REQUESTED:
				MATCHED.append( entity )
		print( "ret ", MATCHED )
		return MATCHED

	def entity_data( self, entities ):
		COMBINED = []
		for eid in entities:
			DATA = {}
			for ind, c in enumerate( eid ):
				if c != -1: DATA[self.COMPONENT[ind]] = self.CONTAINER[ind][c]
			COMBINED.append( DATA )
		return COMBINED

def test( self, glbl ):
	a = self.entity( ["cmpn1"] )
	print("==result==", a)

w = World(["cmpn1", "cmpn2"], [test])

w.create(cmpn1=0, )
w.create(cmpn2=0, )
w.create(cmpn1=0, cmpn2=0)

def none(): pass
w.execute(none)