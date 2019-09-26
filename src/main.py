from pygame.locals import *
import ctypes; ctypes.windll.user32.SetProcessDPIAware(); del ctypes

from src.manager import Manager
from src.functions import *
from src.prologue import *

p.init()

fps = 60
clock = p.time.Clock()

width, height = 1920, 1080
# surface = p.display.set_mode( (width, height), p.FULLSCREEN )
surface = p.display.set_mode( (1000, 1000), )

APP_DIR = "C:/Users/Andrew Shen/Desktop/ProjectEmerald/src/test1"

def callCompiler(): pass


OBJ = Manager()
OBJ.create( {"file": {"input": "a.txt", "output": "b.txt"}}, )
OBJ.create( button( surface, [50, 10], [180, 60], "Save Project", callCompiler,), )
OBJ.create( button( surface, [250, 10], [180, 60], "Train Model", callCompiler,), )
OBJ.create( button( surface, [450, 10], [180, 60], "Execute Project", callCompiler,), )

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
			elif e.key == K_a: OBJ.create( node( surface, [10, 10], 0, ), )
			elif e.key == K_s: OBJ.create( node( surface, [10, 10], 0, ), )
			elif e.key == K_d: OBJ.create( node( surface, [10, 10], 0, ), )
			elif e.key == K_m: OBJ.create( node( surface, [10, 10], 0, ), )
			elif e.key == K_i: OBJ.create( node( surface, [10, 10], 0, mode=["FILE", "NODE", ], ), )
			elif e.key == K_o: OBJ.create( node( surface, [10, 10], 0, mode=["NODE", "FILE", ], ), )

	# print(OBJ.UPDATE_LIST)

	OBJ.execute( event )

	p.display.flip()
	clock.tick( fps )


