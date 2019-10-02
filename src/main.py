from pygame.locals import *
import ctypes; ctypes.windll.user32.SetProcessDPIAware(); del ctypes

from src.manager import Manager
from src.functions import *
from src.prologue import *
from src.model_config.nodes import *

from src.manager import World
from src.systems import *

p.init()

fps = 60
clock = p.time.Clock()

width, height = 1920, 1080
# surface = p.display.set_mode( (width, height), p.FULLSCREEN )
surface = p.display.set_mode( (1000, 1000), )

APP_DIR = "C:/Users/Andrew Shen/Desktop/ProjectEmerald/src/test1"

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
	dat["surface"] = surface
	dat["event"] = {}
	dat["event"]["mPos"] = p.mouse.get_pos()
	dat["event"]["mBtn"] = p.mouse.get_pressed()
	dat["event"]["mTrgOn"] = False  # buttone pressed down
	dat["event"]["mTrgOff"] = False  # buttone pressed up

	for e in event:
		if e.type == QUIT: pass
		elif e.type == MOUSEBUTTONDOWN: dat["event"]["mTrgOn"] = True
		elif e.type == MOUSEBUTTONUP: dat["event"]["mTrgOff"] = True

	return dat

components = ["obj_id", "color", "font", "text"]
systems = [label]
world = World(components, systems)
world.create(obj_id=0, color=(0, 0, 0), text="no")
world.create(obj_id=1, color=(0, 0, 0), text="no")
world.create(obj_id=2, color=(0, 0, 0), text="no")
world.create(obj_id=3, color=(0, 0, 0),)

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


