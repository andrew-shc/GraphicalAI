### === DUMMY CODE ===

def funA(): pass
def funB(): pass
def funX(): pass
def merge(**kwargs): pass
def comb(*args): pass
def required(state): pass
class functype: pass

### ==================

state_data = {
	"keyA": "value",
	"keyB": {
		"keyA":"value",
		"keyC":"value",
	},
}

function_root = {
	funA: "/keyB",
	funB: "/",
}

# FINAL ANSWER: THE GOLDEN KEY TO MY PROBLEM OF INREUSABLITIY

stata = merge( src=[funB],
	keyA="value",
	keyB=merge( src=[funA, funX],
		keyA="value",
		keyC="value",
	),
)

# RETHINKG 1

class Curtain:
	state = {
		"color": "white",
		"length": "50m",
		"hanged": True,
		"pos": [0, 0],
		"wind_velocity": 0,
		"model": None,
		"pattern": {  # problem here <---
			"pattern0": None,  # needs seperate function for each nested same object: inreusability
			"pattern1": None,
			"pattern2": None,
		}
	}
	def __init__(self, description):
		self.description = description


def wind_movement(state):
	if required(state):
		state.wind_velocity = 5


# RETHINK 2

class Curtain:
	# the name of state will be called by the function
	# each state can hold multiple type of its same parent type
	# define maximum object for each state, -1: indefinite; [N]: must contains at most [N] object(s)
	max = {"pattern": -1, "pos": 1, "rect": 1}
	pattern = [
		None,
		None,
		None,
	]
	pos = [None]
	rect = [None]


# RETHINK 3

class Curtain:
	entity = [
		"uniq_id(0,1,NULL)",  # pattern 1
		"uniq_id(None,0,0)",  # the main rectangle
	]

	container = {
		"pattern": [None, None, None],
		"pos": [None, None],
		"rect": [None],
	}

class Node:
	entity = [
		"id",  # field1?
		"id",  # main rectangle?
		"id"   # field2?
	]

	container = {
		"pos": [[0,0], [0,2], [40, 50]],
		"rect": [[0, 10], [0, 20], [0, 30]],
		"clicked": [False, False, False, False, True],
		"selected_region": [False, True]
	}

# RETHINK 4
# I call this the GECS- Grouped ECS

entity = {
	"object-uniq_id": [  # object's unique id are based of id incrementation; more of a grouped entity
		"entity-uniq_id",  # entitiy's unique id are based of which component it has
		"entity-uniq_id",
		"entity-uniq_id",
	]
}

component = ["pos", "rect", "clicked", "selected_region"]  # list upto 255 max; the component's index are used for as component-id
container = [
	[[0,0], [0,2], [40, 50]],
	[[0, 10], [0, 20], [0, 30]],
	[False, False, False, False, True],
	[False, True],
]

# CID - Component ID; EID - Entity ID; OID: - Object ID; FNM - Function Name
# entity's unique id: 8-bit:"[CID 8b][INDEX 16b]"
# e.g. \x02\x01\xF5
# max of 255 types of components; max of 65536 component data per component container