import pygame as p
from src.debugger import *
import src.prefab as prfb


# ====== SUBROUTINE =====

# returns entity data with the only requested components
def _entity_only(self, req):
    return self.entity_pp_cmpnt(self.entity_data(self.entity(self.ENTITIES, req), ), req, strict=True)


# boilerplate code
def _entity_req(self, req):
    ind = self.entity(self.ENTITIES, req)
    dat = self.entity_data(ind)
    return dat, ind


# ======= SYSTEMS =======


def label(self, glbl):
    req = ["pos", "rect", "text", "font", "font_size", "font_color", "font_align", "text_align"]
    e_main, e_ind = _entity_req(self, req)
    for dt in e_main:
        font = p.font.SysFont(dt["font"], dt["font_size"])
        label = font.render(dt["text"], True, (0, 0, 0))
        dimn = font.size(dt["text"])
        pkx = {  # Position Key X
            "left": dt["pos"][0],
            "center": dt["pos"][0]+dt["rect"][0]/2-(dimn[0]/2 if dt["text_align"] else 0),
            "right": dt["pos"][0]+dt["rect"][0]-(dimn[0] if dt["text_align"] else 0),
        }
        pky = {  # Position Key Y
            "top": dt["pos"][1],
            "center": dt["pos"][1]+dt["rect"][1]/2-(dimn[1]/2 if dt["text_align"] else 0),
            "bottom": dt["pos"][1]+dt["rect"][1]-(dimn[1] if dt["text_align"] else 0),
        }
        glbl["surf"].blit(label, (pkx[dt["font_align"]["x"]], pky[dt["font_align"]["y"]]))


def rect(self, glbl):
    req = ["pos", "rect", "color", ]
    e_main, e_ind = _entity_req(self, req)
    for dt in e_main:
        p.draw.rect(glbl["surf"], dt["color"], [dt["pos"][0], dt["pos"][1], dt["rect"][0], dt["rect"][1]])


def click(self, glbl):
    req = ["pos", "rect", "clicked", ]
    e_main, e_ind = _entity_req(self, req)

    clicked = False
    e_click = _entity_only(self, ["clicked"])  # check if any other entity has clicked
    for c in e_click:
        if c["clicked"]: clicked = True

    for eid, dt in zip(reversed(self.entity(self.ENTITIES, req)), reversed(e_main)):
        if dt["pos"][0] < glbl["event"]["mPos"][0] < dt["pos"][0]+dt["rect"][0] and not clicked and \
                dt["pos"][1] < glbl["event"]["mPos"][1] < dt["pos"][1]+dt["rect"][1] and glbl["event"]["mTrgOn"]:  # main
            dt["clicked"] = True
            clicked = True
        if glbl["event"]["mTrgOff"] and dt["clicked"]: dt["clicked"] = False
        self.entity_save(eid, dt)

def clickEvent(self, glbl):
    req = ["clicked", "function", "param"]
    e_main, e_ind = _entity_req(self, req)

    for dt in reversed(e_main):
        if dt["clicked"] and glbl["event"]["mTrgOn"]:
            dt["function"](*dt["param"])

def move(self, glbl):
    req = ["pos", "clicked", "movable", "placement_ofs"]
    e_main, e_ind = _entity_req(self, req)
    for eid, dt in zip(reversed(self.entity(self.ENTITIES, req)), reversed(e_main)):
        if dt["movable"]:
            if dt["clicked"] and dt["placement_ofs"] == [None, None]:  # first clicked
                dt["placement_ofs"] = [dt["pos"][0]-glbl["event"]["mPos"][0], dt["pos"][1]-glbl["event"]["mPos"][1]]
            elif dt["clicked"]:  # next continues clicked
                dt["pos"] = [dt["placement_ofs"][0]+glbl["event"]["mPos"][0],
                             dt["placement_ofs"][1]+glbl["event"]["mPos"][1]]
            else:  # finish clicking
                dt["placement_ofs"] = [None, None]
        self.entity_save(eid, dt)


def moveChild(self, glbl):
    req = ["pos", "movable", "child", "placement_ofs"]
    e_main, e_ind = _entity_req(self, req)
    for eid, dt in zip(reversed(e_ind), reversed(e_main)):
        if dt["movable"] and dt["placement_ofs"] != [None, None]:
            e_child, e_indc = _entity_req(self, ["obj_id", "pos"])
            for eidc, dtc in zip(reversed(e_indc), reversed(e_child)):
                if dtc["obj_id"] == dt["child"] and dt["clicked"]:  # this child entity is part of the master entity
                    vector = [(glbl["event"]["mPos"][0]+dt["placement_ofs"][0])-dt["pos"][0],
                              (glbl["event"]["mPos"][1]+dt["placement_ofs"][1])-dt["pos"][1]]
                    dtc["pos"][0] += vector[0]
                    dtc["pos"][1] += vector[1]
                    self.entity_save(eidc, dtc)


# render isolated wire (wire connected to the mouse)
def connectorWireIso(self, glbl):
    req = ["pos", "rect", "clicked", "connectee"]
    e_main, e_ind = _entity_req(self, req)
    for dt in e_main:
        if dt["clicked"]:
            p.draw.line(glbl["surf"], (255, 150, 0), dt["pos"], glbl["event"]["mPos"], 3)


# render connected wire (wire connected to the connected node)
def connectorWireMrg(self, glbl):
    req = ["pos", "rect", "connectee"]
    e_main, e_ind = _entity_req(self, req)
    for dt in e_main:
        for cncte in dt["connectee"]:
            edt = self.entity_data([self.ENTITIES[self.TAG.index(cncte)]])  # get entity data
            p.draw.line(glbl["surf"], (255, 0, 0), dt["pos"], edt[0]["pos"], 3)


# connects each nodes
def connectNode(self, glbl):
    req = ["obj_id", "pos", "rect", "clicked", "connectee", "connect_en", "connect_tg"]
    e_main, e_ind = _entity_req(self, req)

    connector, connectee, cmpct_id = None, None, None
    for eid, dt in zip(reversed(e_ind), reversed(e_main)):
        if dt["clicked"]:  # get the entity connector
            connector = (eid, dt)

        if dt["pos"][0] < glbl["event"]["mPos"][0] < dt["pos"][0]+dt["rect"][0] and \
                dt["pos"][1] < glbl["event"]["mPos"][1] < dt["pos"][1]+dt["rect"][1] and glbl["event"]["mTrgOff"]:
            connectee = (eid, dt)
            cmpct_id = self.TAG[self.ENTITIES.index(eid)]  # compact entity id for connector

    if None not in [connector, connectee,
                    cmpct_id]:  # check if all three variables are not none meaning there are datas
        if connectee[1]["connect_tg"] in connector[1]["connect_en"] and \
                connectee[1]["obj_id"] != connector[1][
            "obj_id"]:  # connect nodes together; check if they're not same obj_id
            connector[1]["connectee"].append(cmpct_id)
            self.entity_save(connector[0], connector[1])


# render editable input field
def shwCursor(self, glbl):  # TODO
    req = ["pos", "rect", "text", "font", "font_size", "at", "cursor", "font_align"]
    e_main, e_ind = _entity_req(self, req)

    for eid, dt in zip(reversed(e_ind), reversed(e_main)):
        if dt["at"]:
            font = p.font.SysFont(dt["font"], dt["font_size"])
            dimn = font.size(dt["text"])

            pkx = {  # Position Key X
                "left": dt["pos"][0],
                "center": dt["pos"][0]+dt["rect"][0]/2-(dimn[0]/2 if dt["text_align"] else 0),
                "right": dt["pos"][0]+dt["rect"][0]-(dimn[0] if dt["text_align"] else 0),
            }
            pky = {  # Position Key Y
                "top": dt["pos"][1],
                "center": dt["pos"][1]+dt["rect"][1]/2-(dimn[1]/2 if dt["text_align"] else 0),
                "bottom": dt["pos"][1]+dt["rect"][1]-(dimn[1] if dt["text_align"] else 0),
            }

            if glbl["chrc"]["raw"] == p.K_RIGHT and dt["cursor"] < len(dt["text"]):
                dt["cursor"] += 1
                glbl["cursor"]["blink"] = True
            elif glbl["chrc"]["raw"] == p.K_LEFT and dt["cursor"] > 0:
                dt["cursor"] -= 1
                glbl["cursor"]["blink"] = True

            gcur = glbl["cursor"]

            if glbl["cursor"]["blink"]:
                txt = font.render(dt["text"][0:dt["cursor"]], False, (0, 0, 0))
                textRect = txt.get_rect()
                locx = textRect[2]+gcur["ofsx"]+pkx[dt["font_align"]["x"]]
                p.draw.rect(glbl["surf"], (0, 0, 0), (locx, pky[dt["font_align"]["y"]], gcur["width"], dt["font_size"]))
            self.entity_save(eid, dt)


# edit the /text/ component
def editText(self, glbl):  # TODO
    req = ["text", "at", "cursor"]
    e_main, e_ind = _entity_req(self, req)

    for eid, dt in zip(reversed(e_ind), reversed(e_main)):
        if dt["at"]:
            if glbl["chrc"]["unicode"] in glbl["chrc"]["valid"] and glbl["chrc"]["unicode"] != "":
                l = list(dt["text"])
                l.insert(dt["cursor"], glbl["chrc"]["unicode"])
                dt["text"] = "".join(l)
                dt["cursor"] += 1
            if glbl["chrc"]["unicode"] == chr(p.K_BACKSPACE) and dt["cursor"] > 0:
                l = list(dt["text"])
                del l[dt["cursor"]-1]
                dt["text"] = "".join(l)
                dt["cursor"] -= 1
            self.entity_save(eid, dt)


# when user click ONCE on the object, this will always be true unless the user click away the object's dimension
def at(self, glbl):
    req = ["pos", "rect", "at", ]
    e_main, e_ind = _entity_req(self, req)

    for eid, dt in zip(reversed(self.entity(self.ENTITIES, req)), reversed(e_main)):
        at = False
        e_dt, e_id = _entity_req(self, ["at"])  # check if any other entity has clicked
        for edt, id in zip(e_dt, e_id):
            if edt["at"] and id != eid: at = True

        if dt["pos"][0] < glbl["event"]["mPos"][0] < dt["pos"][0]+dt["rect"][0] and not at and \
                dt["pos"][1] < glbl["event"]["mPos"][1] < dt["pos"][1]+dt["rect"][1]:  # if cursor is at the object
            if glbl["event"]["mTrgOn"]:  # cursor on clicked
                dt["at"] = True
                glbl["cursor"]["txt_inp"] = True
                glbl["cursor"]["blink"] = True
                self.entity_save(eid, dt)
                break

        # else: cursor hovering over the object or off clicked
        else:  # not at the object
            if glbl["event"]["mTrgOn"]:  # cursor on clicked
                dt["at"] = False
                glbl["cursor"]["txt_inp"] = False
                self.entity_save(eid, dt)


# special systems -- for specific purposes

def genFields(self, glbl):
    req = ["obj_id", "pos", "rect", "field", "child"]
    e_main, e_ind = _entity_req(self, req)
    for dt in e_main:
        e_missing = []  # field names that are missing

        entc_req = self.entity_pp_strip(self.entity_data(self.ENTITIES, req=["obj_id", "fld_nm", "fld_typ"]), strict=False,
                                        obj_id=dt["child"])
        entc_name = self.entity_pp_extc(entc_req, "fld_nm")
        entc_type = self.entity_pp_extc(entc_req, "fld_typ")

        for f in dt["field"]:
            if f[0] not in entc_name:
                e_missing.append(f)
            else:
                # if the field type does not match
                if f[1] != entc_type[entc_name.index(f[0])]:
                    e_missing.append(f)

        nd_pd = glbl["fld_sty"]["nd_pad"]
        nd_sz = glbl["fld_sty"]["nd_sz"]

        ind_i, ind_o = 0, 0
        for f in e_missing:  # creating a new entity
            if type(f[1]) == glbl["node_typ"]["inp"]:
                prfb.boxInpField(self, dt["child"], dt["pos"], dt["rect"], nd_pd, nd_sz, ind_i,
                                 f[1], f[0], [prfb.NdEn.BoxOut])  # going for reciprocal b/c inp cnnct to out
                ind_i += 1
            elif type(f[1]) == glbl["node_typ"]["out"]:
                prfb.boxOutField(self, dt["child"], dt["pos"], dt["rect"], nd_pd, nd_sz, ind_o,
                                 f[1], f[0], [prfb.NdEn.BoxInp])
                ind_o += 1
            elif type(f[1]) == glbl["node_typ"]["user"]:  # user defined node, uses custom entities
                ind_u = max(ind_i, ind_o)+1
                pos = dt["pos"]
                rect = dt["rect"]
                f[1].exe.create(self, dt["child"], [pos[0]+nd_pd, pos[1]+ind_u*(nd_sz+nd_pd)+nd_pd+rect[1]/4+nd_pd],
                                [rect[0], 20], f[0], f[1])
