"""
issue stage 1 -> find possible bug outcomes
issue stage 2 -> standard debugger method: print, exec, assert ...
issue stage 3 -> quarantine the buggy code into a seperate file; stripping all unrelated to bug for further investigation
issue stage 4 -> use the debugger software; possible bug report for the respective language

issue stage 1

BASIC DEBUGGING PROCEDURE:
1. Assert if the type you expected and the outcome is expect
2. Print each variable of the `for` loop
3. Check the data or results upstream that is feeding downward to find the root problem
4. Try using shallow copy (.copy()) if you want separate the parameters or variables

===

github issue tracker:

"""


# ====== SUBROUTINE =====

# returns entity with the only requested components
def _entity_only(self, req): return self.entity_data(self.entity(req), _strict=req)


# boilerplate code
def _entity_req(self, req):
    ind = self.entity(req)
    dat = self.entity_data(ind)
    return dat, ind


# ======= SYSTEMS =======


def label(self, glbl):
    req = ["pos", "size", "text", "font", "font_size", "font_color", "font_align", "text_align"]
    e_main = self.entity_data(self.entity(req))
    for dt in e_main:
        font = p.font.SysFont(dt["font"], dt["font_size"])
        label = font.render(dt["text"], True, (0, 0, 0))
        dimn = font.size(dt["text"])
        pkx = {  # Position Key X
            "left": dt["pos"][0],
            "center": dt["pos"][0]+dt["size"][0]/2-(dimn[0]/2 if dt["text_align"] else 0),
            "right": dt["pos"][0]+dt["size"][0]-(dimn[0] if dt["text_align"] else 0),
        }
        pky = {  # Position Key Y
            "top": dt["pos"][1],
            "center": dt["pos"][1]+dt["size"][1]/2-(dimn[1]/2 if dt["text_align"] else 0),
            "bottom": dt["pos"][1]+dt["size"][1]-(dimn[1] if dt["text_align"] else 0),
        }
        glbl["surf"].blit(label, (pkx[dt["font_align"]["x"]], pky[dt["font_align"]["y"]]))


def rect(self, glbl):
    req = ["pos", "size", "color", ]
    e_main = self.entity_data(self.entity(req))
    for dt in e_main:
        p.draw.rect(glbl["surf"], dt["color"], [dt["pos"][0], dt["pos"][1], dt["size"][0], dt["size"][1]])


def click(self, glbl):
    req = ["pos", "size", "clicked", ]
    e_main = self.entity_data(self.entity(req))

    clicked = False
    e_click = self.entity_data(self.ENTITIES, ["clicked"])  # check if any other entity has clicked
    for c in e_click:
        if c:
            clicked = True

    for eid, dt in zip(reversed(self.entity(req)), reversed(e_main)):
        if dt["pos"][0] < glbl["event"]["mPos"][0] < dt["pos"][0]+dt["size"][0] and not clicked and \
                dt["pos"][1] < glbl["event"]["mPos"][1] < dt["pos"][1]+dt["size"][1] and glbl["event"][
            "mTrgOn"]:  # main
            dt["clicked"] = True
            clicked = True
        if glbl["event"]["mTrgOff"] and dt["clicked"]: dt["clicked"] = False
        self.entity_save(eid, dt)


def move(self, glbl):
    print("MOVE")
    req = ["pos", "clicked", "movable", "placement_ofs"]
    e_main = self.entity_data(self.entity(req))
    for eid, dt in zip(reversed(self.entity(req)), reversed(e_main)):
        if dt["movable"]:
            if dt["clicked"] and dt["placement_ofs"] == [None, None]:  # first clicked
                dt["placement_ofs"] = [dt["pos"][0]-glbl["event"]["mPos"][0], dt["pos"][1]-glbl["event"]["mPos"][1]]
            elif dt["clicked"]:  # next continues clicked
                dt["pos"] = [dt["placement_ofs"][0]+glbl["event"]["mPos"][0],
                             dt["placement_ofs"][1]+glbl["event"]["mPos"][1]]
            else:  # finish clicking
                dt["placement_ofs"] = [None, None]
        self.entity_save(eid, dt)


def move_child(self, glbl):
    print("CHILD")
    req = ["pos", "movable", "child", "placement_ofs"]
    e_main, e_ind = _entity_req(self, req)
    for eid, dt in zip(reversed(e_ind), reversed(e_main)):
        if dt["movable"] and dt["placement_ofs"] != [None, None]:
            e_child, e_indc = _entity_req(self, ["obj_id", "pos"])
            for eidc, dtc in zip(reversed(e_indc), reversed(e_child)):
                print(dtc["obj_id"], dt["child"])
                if dtc["obj_id"] == dt["child"]:  # this child entity is part of the master entity
                    vector = [(glbl["event"]["mPos"][0]+dt["placement_ofs"][0])-dt["pos"][0],
                              (glbl["event"]["mPos"][1]+dt["placement_ofs"][1])-dt["pos"][1]]
                    print(dt, dtc, )
                    print(f"({glbl['event']['mPos'][0]}+{dt['placement_ofs'][0]})-{dt['pos'][0]} = {vector[0]}")
                    print(f"({glbl['event']['mPos'][1]}+{dt['placement_ofs'][1]})-{dt['pos'][1]} = {vector[1]}")
                    dtc["pos"][0] += vector[0]
                    dtc["pos"][1] += vector[1]
                    self.entity_save(eidc, dtc)


def gen_fields(self, glbl):  # if missing
    req = ["obj_id", "pos", "field", ]
    e_main = self.entity_data(self.entity(req))
    for dt in e_main:
        e_child = _entity_only(self, ["fld_nm", ])
        e_missing = []  # fields that are missing

        for f in dt["field"]:
            if f not in e_child:
                e_missing.append(f)

        nd_pd = glbl["fld_sty"]["nd_pad"]
        nd_sz = glbl["fld_sty"]["nd_sz"]

        ind_i, ind_o = 0, 0
        for f in e_missing:  # creating a new entity

            if dt["field"][f] == glbl["node_typ"]["inp"]:
                preBoxInpField(self, dt["child"], dt["pos"], dt["size"], nd_pd, nd_sz, ind_i, dt["field"][f], f, )
                ind_i += 1
            elif dt["field"][f] == glbl["node_typ"]["out"]:
                preBoxOutField(self, dt["child"], dt["pos"], dt["size"], nd_pd, nd_sz, ind_i, dt["field"][f], f, )
                ind_o += 1
            elif dt["field"][f] == glbl["node_typ"]["user"]:  # user defined node, uses custom entities
                ind_u = max(ind_i, ind_o)+1
                self.create(obj_id=dt["child"],
                            pos=[dt["pos"][0], dt["pos"][1]+ind_u*(nd_sz+nd_pd)+nd_pd+dt["size"][1]/4+nd_pd],
                            size=[dt["size"][0], 25], color=(0, 0, 0), fld_nm=f, fld_typ=dt["field"][f], fld_dt=None)


def preBox(world, obj_id, master_id, pos, size, text, field):
    world.create(obj_id=obj_id, pos=pos, size=[size[0], size[1]], color=(150, 200, 255))  # output area
    world.create(obj_id=obj_id, pos=pos, size=[size[0]/2, size[1]], color=(170, 220, 255))  # input area
    world.create(obj_id=obj_id, pos=pos, size=[size[0], size[1]/4], color=(220, 220, 220))  # title area

    world.create(obj_id=obj_id, pos=pos, size=[size[0], size[1]/4], font="mono", font_size=15, font_color=(0, 0, 0),
                 font_align={"x": "center", "y": "center"}, text=text, text_align=True)  # title text

    # master controller entity for the box
    world.create(obj_id=master_id, child=obj_id, pos=pos, size=size, color=(255, 0, 0), clicked=False, movable=True,
                 placement_ofs=[None, None], field=field)


def preBoxField(world, obj_id, pos, size, ptxt, stxt, name, x_align, ):
    # field shape, data, and wires
    world.create(obj_id=obj_id, pos=pos, size=size, color=(0, 0, 0), clicked=False, )
    # field text
    world.create(obj_id=obj_id, pos=ptxt,
                 size=stxt, font="mono", font_size=12, font_color=(0, 0, 0), text_align=True,
                 font_align={"x": x_align, "y": "center"}, text=name)


def preBoxInpField(world, obj_id, pos, size, nd_pd, nd_sz, fld_ind, typ, name, ):
    preBoxField(world, obj_id, [pos[0]+nd_pd, pos[1]+fld_ind*(nd_sz+nd_pd)+nd_pd+size[1]/4+nd_pd], [nd_sz, nd_sz],
                [pos[0]+nd_sz+nd_pd*2, pos[1]+size[1]/4+nd_pd+nd_pd], [size[0]/2-nd_pd*2, nd_sz], name, "left", )


def preBoxOutField(world, obj_id, pos, size, nd_pd, nd_sz, fld_ind, typ, name, ):
    preBoxField(world, obj_id, [pos[0]+size[0]-nd_pd-nd_sz, pos[1]+fld_ind*(nd_sz+nd_pd)+nd_pd+size[1]/4+nd_pd],
                [nd_sz, nd_sz], [pos[0]+size[0]/2+nd_pd, pos[1]+size[1]/4+nd_pd+nd_pd],
                [size[0]/2-nd_sz-nd_pd*2-nd_pd*2, nd_sz], name, "right", )


from pygame.locals import *
import pygame as p
import ctypes;

ctypes.windll.user32.SetProcessDPIAware();
del ctypes

from src.debugger import *
from src.manager import World

info("Main Application Initialized")

p.init()

fps = 60
clock = p.time.Clock()

width, height = 1920, 1080
surface = p.display.set_mode((width, height), p.FULLSCREEN)
# surface = p.display.set_mode( (1000, 1000), )

info("Pygame and Standard Variables Initialized")


def callCompiler(): pass


def saveProject(obj):
    pass


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
        if e.type == QUIT:
            pass
        elif e.type == MOUSEBUTTONDOWN:
            dat["event"]["mTrgOn"] = True
        elif e.type == MOUSEBUTTONUP:
            dat["event"]["mTrgOff"] = True

    dat["fld_sty"] = {}
    dat["fld_sty"]["nd_pad"] = 2
    dat["fld_sty"]["nd_sz"] = 10

    return dat


components = ["obj_id", "pos", "size", "color", "font", "font_size", "font_color", "font_align", "text", "text_align",
              "clicked", "movable", "placement_ofs", "child", ]  # [..., "file_data", "vector"]

systems = [rect, move_child, move, click]  # 1st, ..., Nth
world = World(components, systems)


def preBox(world, obj_id, master_id, pos, size, text, ):
    world.create(obj_id=obj_id, pos=pos, size=[size[0], size[1]], color=(150, 200, 255))  # output area
    world.create(obj_id=obj_id, pos=pos, size=[size[0]/2, size[1]], color=(170, 220, 255))  # input area
    world.create(obj_id=obj_id, pos=pos, size=[size[0], size[1]/4], color=(220, 220, 220))  # title area

    world.create(obj_id=obj_id, pos=pos, size=[size[0], size[1]/4], font="mono", font_size=15, font_color=(0, 0, 0),
                 font_align={"x": "center", "y": "center"}, text=text, text_align=True)  # title text

    # master controller entity for the box
    world.create(obj_id=master_id, child=obj_id, pos=pos, size=size, color=(255, 0, 0), clicked=False, movable=True,
                 placement_ofs=[None, None], )


# test

# world.create( obj_id=obj_id, pos=pos, size=[size[0], size[1]], color=(0, 255, 0) )

preBox(world, 2, 3, [500, 500], [200, 100], "Hello World", )

# world.create( obj_id=2, pos=[500, 500], size=[200, 100], color=(150, 200, 255) )  # output area
# world.create( obj_id=2, pos=[500, 500], size=[200/2, 100], color=(170, 220, 255) )  # input area
# world.create( obj_id=2, pos=[500, 500], size=[200, 100/4], color=(220, 220, 220) )  # title area
#
# world.create( obj_id=2, pos=[500, 500], size=[200, 100/4], font="mono", font_size=15, font_color=(0, 0, 0),
#               font_align={"x":"center", "y":"center"}, text="Hello World", text_align=True )  # title text
#
# # master controller entity for the box
# world.create( obj_id=3, child=2, pos=[500, 500], size=[200, 100], color=(255, 0, 0), clicked=False, movable=True,
#               placement_ofs=[None, None],  field={"input":inPut, "output":outPut, "user defined":userDef} )

print(world.ENTITIES)
print(world.entity_data(world.ENTITIES))
#####

# MAIN:
MA = "__main__ [DEBUG] [[0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [2, 2, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [3, 3, 3, -1, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [4, 4, 4, 3, -1, -1, -1, -1, -1, -1, 0, 0, -1, 0, -1, -1, -1, 0, 0, -1, -1, -1]]"
MB = "__main__ [DEBUG] [{'obj_id': 2, 'pos': [500, 500], 'size': [200, 100], 'color': (150, 200, 255)}, {'obj_id': 2, 'pos': [500, 500], 'size': [100.0, 100], 'color': (170, 220, 255)}, {'obj_id': 2, 'pos': [500, 500], 'size': [200, 25.0], 'color': (220, 220, 220)}, {'obj_id': 2, 'pos': [500, 500], 'size': [200, 25.0], font': 'mono', 'font_size': 15, 'font_color': (0, 0, 0), 'font_align': {'x': 'center', 'y': 'center'}, 'text': 'Hello World', 'text_align': True}, {'obj_id': 3, 'pos': [500, 500], 'size': [200, 100], 'color': (255, 0, 0), 'clicked': False, 'movable': True, 'field': {'input': <function inPut at 0x03353C90>, 'output': <function outPut at 0x03353CD8>, 'user defined': <function userDef at 0x03353D20>}, 'placement_ofs': [None, None], 'child': 2}]"

# PREFAB:
PA = "__main__ [DEBUG] [[0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [2, 2, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [3, 3, 3, -1, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [4, 4, 4, 3, -1, -1, -1, -1, -1, -1, 0, 0, -1, 0, -1, -1, -1, 0, 0, -1, -1, -1]]"
PB = "__main__ [DEBUG] [{'obj_id': 2, 'pos': [500, 500], 'size': [200, 100], 'color': (150, 200, 255)}, {'obj_id': 2, 'pos': [500, 500], 'size': [100.0, 100], 'color': (170, 220, 255)}, {'obj_id': 2, 'pos': [500, 500], 'size': [200, 25.0], 'color': (220, 220, 220)}, {'obj_id': 2, 'pos': [500, 500], 'size': [200, 25.0], font': 'mono', 'font_size': 15, 'font_color': (0, 0, 0), 'font_align': {'x': 'center', 'y': 'center'}, 'text': 'Hello World', 'text_align': True}, {'obj_id': 3, 'pos': [500, 500], 'size': [200, 100], 'color': (255, 0, 0), 'clicked': False, 'movable': True, 'field': {'input': <function inPut at 0x03053C90>, 'output': <function outPut at 0x03053CD8>, 'user defined': <function userDef at 0x03053D20>}, 'placement_ofs': [None, None], 'child': 2}]"

c = 0
for i, j in zip(MA, PA):
    if i != j:
        print(c, i, j)
    c += 1

c = 0
for i, j in zip(MB, PB):
    if i != j:
        print(c, i, j)
    c += 1

#####

info("Software Graphic Object Initialized")

app_loop = True
while app_loop:
    surface.fill((255, 255, 255))

    event = p.event.get()
    mpx, mpy = p.mouse.get_pos()
    mps = p.mouse.get_pressed()

    for e in event:
        # print(e)
        if e.type == QUIT:
            app_loop = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE: app_loop = False

    world.execute(update_glbl)

    p.display.flip()
    clock.tick(fps)

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
