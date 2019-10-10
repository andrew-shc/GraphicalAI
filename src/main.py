from pygame.locals import *
import ctypes; ctypes.windll.user32.SetProcessDPIAware(); del ctypes

from src.manager import Manager
from src.functions import *
from src.prologue import *
from src.model_config.nodes import *

from src.debugger import *
from src.manager import World
from src.systems import *

info("Main Application Initialized")

p.init()

fps = 60
clock = p.time.Clock()

width, height = 1920, 1080
# surface = p.display.set_mode( (width, height), p.FULLSCREEN )
surface = p.display.set_mode( (1000, 1000), )

APP_DIR = "C:/Users/Andrew Shen/Desktop/ProjectEmerald/src/test1"

info("Pygame and Standard Variables Initialized")

def callCompiler(): pass
def saveProject(obj):
	pass


OBJ = Manager()
OBJ.create( {"file": {"input": "a.txt", "output": "b.txt"}}, )
OBJ.create( button( surface, [50, 10], [180, 60], "Save Project", callCompiler,), )
OBJ.create( button( surface, [250, 10], [180, 60], "Train Model", callCompiler,), )
OBJ.create( button( surface, [450, 10], [180, 60], "Execute Project", callCompiler,), )

event = []


def update_glbl():
	dat = {}
	dat["surf"] = surface
	dat["event"] = {}
	dat["event"]["mPos"] = p.mouse.get_pos()
	dat["event"]["mBtn"] = p.mouse.get_pressed()
	dat["event"]["mTrgOn"] = False  # buttone pressed down
	dat["event"]["mTrgOff"] = False  # buttone pressed up

	for e in event:
		if e.type == QUIT: pass
		elif e.type == MOUSEBUTTONDOWN: dat["event"]["mTrgOn"] = True
		elif e.type == MOUSEBUTTONUP: dat["event"]["mTrgOff"] = True


	dat["fld_sty"] = {}
	dat["fld_sty"]["nd_pad"] = 2
	dat["fld_sty"]["nd_sz"] = 10

	dat["node_typ"] = {
		"inp": inPut,
		"out": outPut,
		"user": userDef,
	}

	return dat

def fileInput(): pass
def selectionNode(): pass
def inPut(): pass  # input node
def outPut(): pass  # output node
def userDef(): pass  # user defined variable within software

""" 
NAME STYLE: ALL COMPONENTS/SYSTEM SHOULD ONLY HAVE (English Alphabets and underscore), [A-Z][a-z]_
field: ["FIELD NAME": [FIELD_TYPE]]
fld_dt: [ [eid, ... ], [eid, .... ] ]  # first list, input; second list, output
connectee: [ EID, EID, ... ]  # list of connected EID
"""
components = ["obj_id", "pos", "size", "color", "font", "font_size", "font_color", "font_align", "text", "text_align",
              "clicked", "movable", "function", "field", "fld_nm", "fld_typ", "fld_dt", "placement_ofs", "child",
              "connectee"]  # [..., "file_data", "vector"]

systems = [rect, label, gen_fields, click, move_child, move, render_iso_wire, match_node ]  # 1st, ..., Nth
world = World(components, systems)


world.create(obj_id=0, pos=[500, 500], size=[200, 100], color=(150, 200, 255))  # output area
world.create(obj_id=0, pos=[500, 500], size=[200/2, 100], color=(170, 220, 255))  # input area
world.create(obj_id=0, pos=[500, 500], size=[200, 100/4], color=(220, 220, 220))  # title area

world.create(obj_id=0, pos=[500, 500], size=[200, 100/4], font="mono", font_size=15, font_color=(0, 0, 0),
             font_align={"x": "center", "y": "center"}, text="Hello World", text_align=True )  # title text

# world.create(obj_id=0, pos=[500, 500], size=[200, 100], clicked=False, movable=True, placement_ofs=[None, None], child=0)

# world.create(obj_id=0, pos=[500+2, 500+100/4+2], size=[10, 10], color=(0, 0, 0),)
world.create(obj_id=1, child=0, pos=[500, 500], size=[200, 100], clicked=False, movable=True, placement_ofs=[None, None],
             field={"input":inPut, "output":outPut, "user defined":userDef})

# program input and output field
# world.create(obj_id=0, pos=[None, None], size=[None, None], color=(0, 0, 0), font="mono", font_size=10,
#             font_color=(0,0,0), font_align={"x": "center", "y": "center"}, text="Hello World", text_align=True,
#             fld_nm="FIELD NAME", fld_typ="input", fld_dt=[],)

# user input and output field
world.create(obj_id=5, fld_typ=fileInput, fld_dt=[])

# input/output field
# + fld_typ=input/output

# user input field
# + fld_typ=func type
# - fld_nm

world.create(obj_id=0, pos=[200, 200], size=[50, 50], color=(0, 0, 0), clicked=False, connectee=None )

info("Software Graphic Object Initialized")

app_loop = True
while app_loop:
	surface.fill( (255, 255, 255) )

	event = p.event.get()
	mpx, mpy = p.mouse.get_pos()
	mps = p.mouse.get_pressed()

	for e in event:
		#print(e)
		if e.type == QUIT:
			app_loop = False
		elif e.type == KEYDOWN:
			if e.key == K_ESCAPE: app_loop = False
			elif e.key == K_s: OBJ.create( node( surface, [10, 10], None, ), )
			elif e.key == K_i: OBJ.create( node( surface, [10, 10], None, ), )
			elif e.key == K_o: OBJ.create( node( surface, [10, 10], None, ), )

	# print(OBJ.UPDATE_LIST)

	OBJ.execute( event )

	world.execute( update_glbl )

	p.display.flip()
	clock.tick( fps )

DEAD_CMPNT = []
for ind, c in enumerate(world.CONTAINER):
	if c == []:
		DEAD_CMPNT.append(world.COMPONENT[ind])

info("Software Exit")

info("Software Result:")
info(f"\tErrors:   {getter()[2]-1}")
info(f"\tWarnings: {getter()[1]-1}")
info(f"\tDebugs:   {getter()[0]-1}")
info("Software Report:")
info(f"\tComponents Not Used: {DEAD_CMPNT}")

info("Debug Exit")
p.quit()
quit()