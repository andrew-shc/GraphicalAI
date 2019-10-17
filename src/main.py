from pygame.locals import *
import ctypes; ctypes.windll.user32.SetProcessDPIAware(); del ctypes

from src.debugger import *
from src.manager import World
from src.systems import *
import src.prefab as prfb

info("Main Application Initialized")

p.init()

fps = 60
clock = p.time.Clock()

width, height = 1920, 1080
surface = p.display.set_mode( (width, height), p.FULLSCREEN )
# surface = p.display.set_mode( (1000, 1000), )

APP_DIR = "C:/Users/Andrew Shen/Desktop/ProjectEmerald/src/test1"

info("Pygame and Standard Variables Initialized")

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
		"inp": prfb.inPut,
		"out": prfb.outPut,
		"user": prfb.userDef,
	}

	return dat

# run doc build:  sphinx-build ./source ../ref
""" 
NAME STYLE: ALL COMPONENTS/SYSTEM SHOULD ONLY HAVE (English Alphabets and underscore), [A-Z][a-z]_
field: ["FIELD NAME": [FIELD_TYPE]]
fld_dt: [ [eid, ... ], [eid, .... ] ]  # first list, input; second list, output
connectee: [ EID, EID, ... ]  # list of connected EID
connect_en: [ tag ]  # connection to enable
connect_tg: tag  # connector's tag to identify
"""
components = ["obj_id", "pos", "size", "color", "font", "font_size", "font_color", "font_align", "text", "text_align",
              "clicked", "movable", "function", "field", "fld_nm", "fld_typ", "fld_dt", "placement_ofs", "child",
              "connectee", "connect_en", "connect_tg"]  # [..., "file_data", "vector"]

systems = [rect, label, gen_fields, move_child, move, connectorWireIso, connectorWireMrg, connectNode, click ]
world = World(components, systems)  # initialize world manager class

oid_cc = 1
prfb.Box(world, oid_cc, oid_cc+1, [500, 500], [200, 100], "Hello World", {"input":prfb.inPut, "output":prfb.outPut, "user defined":prfb.userDef})
oid_cc += 2

world.create(obj_id=0, pos=[200, 200], size=[50, 50], color=(0, 0, 0), clicked=False, connectee=[], connect_en=["nodeA"], connect_tg="nodeA" )
world.create(obj_id=0, pos=[500, 200], size=[50, 50], color=(0, 0, 0), clicked=False, connectee=[], connect_en=["nodeA"], connect_tg="nodeA" )

info("Software Graphic Object Initialized")

app_loop = True
while app_loop:
	surface.fill( (255, 255, 255) )
	event = p.event.get()

	for e in event:
		if e.type == QUIT:
			app_loop = False
		elif e.type == KEYDOWN:
			if e.key == K_ESCAPE: app_loop = False
			elif e.key == K_s:
				prfb.Box(world, oid_cc, oid_cc+1, [500, 500], [200, 100], "S",
				         {"input":prfb.inPut, "output":prfb.outPut, "user defined":prfb.userDef})
			elif e.key == K_i:
				prfb.Box(world, oid_cc, oid_cc+1, [500, 500], [200, 100], "I",
				         {"input":prfb.inPut, "output":prfb.outPut, "user defined":prfb.userDef})
			elif e.key == K_o:
				prfb.Box(world, oid_cc, oid_cc+1, [500, 500], [200, 100], "O",
				         {"input":prfb.inPut, "output":prfb.outPut, "user defined":prfb.userDef})
			oid_cc += 2

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