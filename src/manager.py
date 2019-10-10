import src.functions as func
from src.debugger import *

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
	"""
	Entities -> Refers to component for data and requirements
	Component -> All the registered components
	Container -> All the data organized by components
	System -> All the registered system (or registered functions)

	# TODO: [IF] Implement compact container and non-compact container if needed
	COMPACT STORAGE -> HAS NO KEY, PURE DATA; ORDERED; MORE CPU
	NON-COMPACT STORAGE -> HAS KEYS; ORDERLESS; MORE DATA

	Compact storage is the default

	EID ~ List of Entity ID
	ENTITIES ~ List of Entities Data
	"""

	ENTITIES = []   # [ENTITY, ENTITY, ENTITY, ...]
	COMPONENT = []  # components registered; for key and index for container
	CONTAINER = []  # [[data, data, ...], [data, ...], ...]; to store data; 2d data array
	SYSTEM = []  # registered systems (i.e. functions)
	GLOBAL = {}  # global variable

	DESTROYING = []  # entities to be destroyed

	def __init__(self, component, system):
		"""
		:param component: Components to be registered with the respective World()
		:param system: Systems to be registered for execution in the respective World()
		"""

		for c in component:
			if component.count(c) > 1:
				error(f"Duplicate component <{c}> when initializing")

		self.COMPONENT = component
		self.SYSTEM = system
		for _ in component:  # initilize the data space in the container (data 2D array)
			self.CONTAINER.append([])

	# ==== fundamental method ====

	def create( self, **kwargs ):
		""" creates anew entity from list of registered components
		:param **kwargs: Selected component (key) assigning a value (val) to the respective component
		"""

		for k in kwargs:
			if k not in self.COMPONENT:
				error(f"Entity creation passed in unregistered component <{k}>")

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

		info( "Entity Created", ID)

	def destroy( self, eid ):
		""" destroy the entity through ID
		:param eid: Destroys entity by ID
		"""
		self.ENTITIES.remove(eid)
		self.DESTROYING.append(eid)

		info( "Entity Destroyed", eid )

	def flush( self ):
		""" cleans all the dead data in the container """

		info( "Dead Entity Flushed" )

	def execute( self, func, ):
		""" executes all the function; the function manages the entities
		:param func: function to be executed for updating the self.GLOBAL variable
		"""

		self.GLOBAL = func()
		for s in self.SYSTEM:
			try:
				s(self, self.GLOBAL)
			except KeyError as e:
				if e not in self.COMPONENT:
					error( f"System <{s.__name__}> tried to access unregistered component <{e}>" )
				else:
					error(f"System <{s.__name__}> tried to access missing component <{e}>")

	# ==== feature methods ====

	def organize( self ):
		""" organize the container by components (hierachy) """
		pass

	def entity( self, cmpn ):
		""" get entity by list of required components
		:param cmpn: List of requested component
		:return: Returns list of matched entity
		"""

		for r in cmpn:
			if r not in self.COMPONENT:
				error( f"System <{caller_name()}> used unregistered component {r}" )

		# translates requested string components to translated required id
		ID_KEY = [d for d in map( lambda c: 0 if c not in cmpn else 1, self.COMPONENT)]
		MATCHED = []  # entity passed the requirement
		for entity in self.ENTITIES:
			REQUESTED = True
			for id, c in zip( ID_KEY, entity ):
				if id == 1 and c == -1:
					REQUESTED = False
					break
			if REQUESTED:
				MATCHED.append( entity )  # appends entity ID
		return MATCHED

	def entity_data( self, eid, _strict=() ):
		""" translates list of entity id into actual usable data
		:param eid: Entity ID to be processed into usable data for systems
		:param _strict =False: (), returns the matched entity data;
							   List<Components>, returns the matched entity data with the only required component
									**NOTE**: Single component inputted would yield single data/variable
		:return: Returns processed Entities
		"""

		combined = []
		if _strict is ():
			for id in eid:
				DATA = {}
				for ind, c in enumerate( id ):
					if c != -1: DATA[self.COMPONENT[ind]] = self.CONTAINER[ind][c]
				combined.append( DATA )
		elif _strict is not ():
			for s in _strict:
				if s not in self.COMPONENT:
					error( f"System <{caller_name()}> used unregistered component <{s}> that is invalid!" )
			if len(_strict) == 1:  # _strict has single component
				for e in eid:
					ind = self.COMPONENT.index(_strict[0])
					combined.append( self.CONTAINER[ind][e[ind]] )
			else:
				for id in eid:
					data = {}
					append = True
					for ind, c in enumerate( id ):
						if self.COMPONENT[ind] in _strict:  # the component that is active is strict in-bound
							if c != -1:  # not nullptr; there are data
								data[self.COMPONENT[ind]] = self.CONTAINER[ind][c]
							else:  # nullptr; missed the requirement
								append = False
								break
					if append: combined.append( data )
		else:
			error( "Method World.entity_data(self, _strict=False) received a wrong type for parameter _strict" )

		return combined

	def entity_equal( self, _strict=False, **kwargs, ):
		""" get entities with the same component and the same value of the respective component
		:param eid: Entities to be processed
		:param _strict =False: False, gets entities that has the component and the value of the respective component
									 equals to the listed component
								True, gets entities that ONLY has the component and the same exact value respectively
		:return: List of required entities that has the same exact value of the component's value
		"""

		for k in kwargs:
			if k not in self.COMPONENT:
				error(f"World.entity_equal accessing unregistered component <{k}>")

		ent_req = self.entity( kwargs.keys() )  # requested entity
		ent_eq = []  # entities matched
		for eid in ent_req:
			matched = True
			for ind, cid in enumerate(eid):
				for k in kwargs:
					if k == self.COMPONENT[ind]:  # if component <k> in kwargs == component <k> in entity
						if kwargs[k] != self.CONTAINER[ind][cid]:  # the value DOES NOT equals to each other
							matched = False
			if matched:
				ent_eq.append( eid )
		if _strict is False:  # not strict; returns the full entity id
			return self.entity_data( ent_eq )
		else:
			return self.entity_data( ent_eq, _strict=list(kwargs) )

	def entity_save( self, eid, ent_dt ):
		""" to save the data from entity dictionary into the container
		:param eid: Entity ID to find the reference to the container
		:param ent_dt: Data the Systems edited to be saved into the container
		"""

		for ind, c in enumerate(eid):
			if self.COMPONENT[ind] in ent_dt:  # components received from the eid is in the ent_data
				if c != -1:  # has pointer for that component to refer data, implying there is data
					self.CONTAINER[ind][c] = ent_dt[self.COMPONENT[ind]]
				else:  # nullptr component whilst still in-bound to ent_dt
					error(f"Entity ID, <{eid}>, does not align with the data (in order), <{list(ent_dt.keys())}>")
			else:
				if c == 1:  # has the pointer but not in ent_dt, definite no-no
					error(f"Entity ID, <{eid}>, does not align with the data (in order), <{list(ent_dt.keys())}>")

