from pygame.locals import *
import ctypes; ctypes.windll.user32.SetProcessDPIAware(); del ctypes
import yaml
import os, errno

from src.model_config import model as mdl
from src.model_config import node_types as typ
from src.debugger import *
from src.manager import World
from src.systems import *
from src.executor import *
import src.prefab as prfb
import src.model_config.graphic_object as go

info("Main Application Initialized")

p.init()

fps = 60
clock = p.time.Clock()

width, height = 1920, 1080
surface = p.display.set_mode((width, height), p.RESIZABLE)
# surface = p.display.set_mode( (1000, 1000), )

APP_DIR = "C:/Users/Andrew Shen/Desktop/ProjectEmerald/src/test1"

info("Pygame and Standard Variables Initialized")


def processConfig(path):
    cfg = yaml.safe_load(open(path, "r").read())
    dat = {}
    dat["surf"] = surface
    dat["event"] = {}
    dat["event"]["mPos"] = p.mouse.get_pos()
    dat["event"]["mBtn"] = p.mouse.get_pressed()
    dat["event"]["mTrgOn"] = False  # buttone pressed down
    dat["event"]["mTrgOff"] = False  # buttone pressed up
    dat["chrc"] = {}  # characters
    dat["chrc"]["valid"] = cfg["chrc"]["valid"]  # valid characters
    dat["chrc"]["moveR"] = False  # button move right
    dat["chrc"]["moveL"] = False  # button move right
    dat["chrc"]["on"] = ""  # characters on clicked
    dat["chrc"]["off"] = ""  # characters off clicked
    dat["chrc"]["raw"] = ""  # raw keyboard input
    dat["chrc"]["unicode"] = ""  # real-life keyboard emulator
    dat["fld_sty"] = {}  # field style
    dat["fld_sty"]["nd_pad"] = cfg["fld_sty"]["nd_pad"]
    dat["fld_sty"]["nd_sz"] = cfg["fld_sty"]["nd_sz"]
    dat["node_typ"] = {  # node type
        "inp": typ.Input,
        "out": typ.Output,
        "user": typ.Constant,
    }
    dat["cursor"] = {}
    dat["cursor"]["width"] = cfg["cursor"]["width"]  # the thickness of the cursor blinking
    dat["cursor"]["ofsx"] = cfg["cursor"]["ofsx"]  # offset-x of the cursor
    dat["cursor"]["ofsy"] = cfg["cursor"]["ofsy"]  # offset-y of the cursor
    dat["cursor"]["cnt_buf"] = 0  # cursor counter buffer
    dat["cursor"]["limit"] = cfg["cursor"]["limit"]  # cursor time limit; updates per frame
    dat["cursor"]["blink"] = False
    dat["cursor"]["txt_inp"] = False  # True if the cursor is inputting text
    dat["cursor"]["cld_buf"] = 0  # cursor cooldown buffer
    dat["cursor"]["cooldown"] = int(cfg["cursor"]["cooldown"])
    return dat

def autoCreate(filename, fdt, ):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:
        yaml.dump(fdt, f, default_flow_style=False)

def initProject(project_dir, project_name):
    cfg = yaml.safe_load(open("config.yaml", "r").read())
    root_dir = project_dir+project_name+"/"

    prj = {
        "workspace": [],
        "meta": "None",
    }

    sttng = {
        "root directory": root_dir
    }

    autoCreate(root_dir+cfg["file_cfg"]["project"], prj)
    autoCreate(root_dir+cfg["file_cfg"]["settings"], sttng)


def selectModel(oid_cc, ent_self, pos, rect, oid):
    get_class = lambda c: [i for i in c.__dict__ if i[0:2] != "__" and i[0] == i[0].upper()]
    class_nm = [eval(f"mdl.{c}.title") for c in get_class(mdl)]
    print(class_nm)
    txt = world.entity_data([ent_self])[0]["text"].lower()

    req = world.entity_pp_strip(world.entity_data( world.ENTITIES, req=["obj_id"] ), False, obj_id=oid)
    for edt in req:
        for edt_int, eid in zip(world.entity_data(world.ENTITIES), world.ENTITIES):
            if edt == edt_int:  # destroying entities from the previous selections
                world.destroy(eid)
    print(world.DESTROYING)
    world.flush()

    select_height = 20
    ind = 1
    for c in class_nm:
        print(txt, c, txt in c)

        if txt == c.lower():
            if txt == mdl.OperationModel.title.lower():
                mdl.OperationModel([500, 500],[200, 100],12).create(world,oid_cc,oid_cc+1)
            elif txt == mdl.FileSaver.title.lower():
                mdl.FileSaver([500, 500],[200, 100],12).create(world,oid_cc,oid_cc+1)
            elif txt == mdl.FileReceiver.title.lower():
                mdl.FileReceiver([500, 500],[200, 100],12).create(world,oid_cc,oid_cc+1)
            elif txt == mdl.ModelTrain.title.lower():
                mdl.ModelTrain([500, 500],[200, 100],12).create(world,oid_cc,oid_cc+1)
            elif txt == mdl.SVCModel.title.lower():
                mdl.SVCModel([500, 500],[200, 100],12).create(world,oid_cc,oid_cc+1)
            oid_cc += 2
        elif txt in c.lower():  # if True -> gets added to the list
            # the title of the text field
            world.create(obj_id=oid, pos=[pos[0], select_height*ind+pos[1]], rect=[rect[0], rect[1]+select_height], font="arial",
                         font_size=14, font_color=(0, 0, 0), font_align={"x": "center", "y": "center"},
                         text=c, text_align=True)
            ind += 1

    print("SELECT MODEL")
    return oid_cc

event = []
bufferRaw = ""
bufferUnic = ""
beginCounter = False  # begin counting the cooldown
model_chsn = ""  # model chosen by the user
txtfld_id = None  # text field id for the model_chsn
dat = processConfig("config.yaml")

components = ["obj_id", "pos", "rect", "color", "font", "font_size", "font_color", "font_align", "text", "text_align",
              "clicked", "movable", "function", "param", "fld_dt", "placement_ofs",
              "child", "connectee", "connect_en", "connect_tg", "length", "width", "cursor", "at", "trigger", "model",
              "listen"]  # [..., "file_data", "vector"]

systems = [rect, label, shwCursor, genFields, moveChild, move, connectorWireIso, connectorWireMrg, connectNode, click,
           at, editText, clickEvent, inputText]
world = World(components, systems)  # initialize world manager class

project = "MySampleProject"
# initialization
cfg = yaml.safe_load(open("config.yaml", "r").read())
root = cfg["file_index"][project]+"/"+project+"/"
print(cfg["file_index"])
for prj in cfg["file_index"]:
    initProject(cfg["file_index"][prj]+"/", prj)

oid_cc = 1

# pre-load objects
prfb.button(world, oid_cc, [220, 10], [200,50], "Save Project", saveSkel, [world, root], backg=(200, 200, 200))
prfb.button(world, oid_cc, [430, 10], [200,50], "Run Project", lambda x: execSkel(*loadSkel(x)), [root],
            backg=(200, 200, 200))
oid_cc += 1

world.create(obj_id=oid_cc, pos=[10, 5], rect=[200, 20], font="arial", font_size=20,  # the title of the text field
                 font_color=(0,0,0), font_align={"x": "center", "y": "center"}, text="Input Model", text_align=True)

prfb.triggerTextField(world, oid_cc, [10, 30], [200, 25], 18, "", K_RETURN, selectModel, backg=(230, 210, 200))  # text field
oid_cc += 2

# val = world.ENTITIES[world.TAG[txtfld_id]]


info("Software Graphic Object Initialized")

dat["oid-cc"] = oid_cc

fullscreen = False
app_loop = True
while app_loop:
    surface.fill((255, 255, 255))
    event = p.event.get()

    # resets counter (or timer) and negates the previous state of the /blink/
    if dat["cursor"]["cnt_buf"] > dat["cursor"]["limit"]:
        dat["cursor"]["cnt_buf"] = 0
        dat["cursor"]["blink"] = not dat["cursor"]["blink"]

    dat["event"]["mPos"] = p.mouse.get_pos()
    dat["event"]["mBtn"] = p.mouse.get_pressed()
    dat["event"]["mTrgOn"] = False  # buttone pressed down
    dat["event"]["mTrgOff"] = False  # buttone pressed up
    dat["chrc"]["moveR"] = False  # button move right
    dat["chrc"]["moveL"] = False  # button move right
    dat["chrc"]["on"] = ""  # characters on clicked
    dat["chrc"]["off"] = ""  # characters off clicked
    # dat["chrc"]["raw"] = ""  # raw keyboard input
    dat["cursor"]["cnt_buf"] += 1
    dat["chrc"]["raw"] = bufferRaw if dat["cursor"]["cld_buf"] > dat["cursor"]["cooldown"] else ""
    dat["chrc"]["unicode"] = bufferUnic if dat["cursor"]["cld_buf"] > dat["cursor"]["cooldown"] else ""

    dat["cursor"]["cld_buf"] = 0 if not beginCounter and dat["cursor"]["cld_buf"] != 0 else dat["cursor"]["cld_buf"]+1

    for e in event:
        if e.type == QUIT:
            app_loop = False
        elif e.type == KEYDOWN:
            dat["chrc"]["on"] = e.key
            dat["chrc"]["raw"] = e.key
            dat["chrc"]["unicode"] = e.unicode
            beginCounter = True

            bufferRaw = dat["chrc"]["raw"]
            bufferUnic = dat["chrc"]["unicode"]

            if e.key == K_RIGHT:
                dat["chrc"]["moveR"] = True
            elif e.key == K_LEFT:
                dat["chrc"]["moveL"] = True

            if e.key == K_ESCAPE:
                app_loop = False
            elif e.key == K_s and not dat["cursor"]["txt_inp"]:
                mdl.OperationModel([500, 500], [200, 100], 12).create( world, oid_cc, oid_cc+1)

                oid_cc += 2
            elif e.key == K_i and not dat["cursor"]["txt_inp"]:
                mdl.FileReceiver([500, 500], [200, 100], 12).create( world, oid_cc, oid_cc+1)

                oid_cc += 2
            elif e.key == K_o and not dat["cursor"]["txt_inp"]:
                mdl.FileSaver([500, 500], [200, 100], 12).create( world, oid_cc, oid_cc+1)

                oid_cc += 2
            elif e.key == K_F11:
                if fullscreen:
                    surface = p.display.set_mode((width, height), p.RESIZABLE)
                    fullscreen = False
                else:
                    surface = p.display.set_mode((width, height), p.FULLSCREEN)
                    fullscreen = True
                print(fullscreen)

        elif e.type == KEYUP:
            dat["chrc"]["off"] = e.key
            dat["chrc"]["raw"] = ""
            dat["chrc"]["unicode"] = ""
            beginCounter = False

            bufferRaw = ""
            bufferUnic = ""

            if e.key == K_RIGHT:
                dat["chrc"]["moveR"] = False
            elif e.key == K_LEFT:
                dat["chrc"]["moveL"] = False
        elif e.type == MOUSEBUTTONDOWN:
            dat["event"]["mTrgOn"] = True
        elif e.type == MOUSEBUTTONUP:
            dat["event"]["mTrgOff"] = True

    # print(world.entity_data([val])[0]["text"])
    world.execute(dat)

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
