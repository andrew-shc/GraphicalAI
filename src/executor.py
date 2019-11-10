"""
The main process of execution in the program

Save Skeleton: Saves the empty models in place
Save Model: Saves all the parametized settings in each of model

Execute Skeleton: Executes all the user input and other input output
Execute ML: Automatically changes each settings of the model

"""

import re

from src.model_config import types as typ

APP_DIR = "C:/Users/Andrew Shen/Desktop/ProjectEmerald/src2/test1"
PROJECT_FILE = "/project_test_4.dat"

# saves the skeleton
def saveSkel(self):
    print("\n\n\n")
    # initialize specific entities
    fld = self.entity(self.ENTITIES, ["obj_id","fld_nm","fld_typ"])
    mdl = self.entity(self.ENTITIES, ["obj_id","field","mid"])

    # inject %short_id% into each entities for easier locating the entities
    inj = []
    for fdt, fid in zip(self.entity_data(fld), fld):
        fdt["%short_id%"] = self.short_id(fid)
        inj.append(fdt)

    # modelization: grouping fields into models
    grp = []
    for m in self.entity_data(mdl):
        ent = []
        # get the model's fields
        for f in inj:
            if m["child"] == f["obj_id"]:
                if repr(f["fld_typ"]) == "c":
                    ent.append(self.entity_pp_cmpnt([f], ["obj_id", "fld_nm", "fld_typ", "cid", "%short_id%"], strict=True)[0])
                else:
                    ent.append(self.entity_pp_cmpnt([f], ["obj_id", "fld_nm", "fld_typ", "connectee", "%short_id%"], strict=True)[0])
                ent[-1]["%fld_data_typ%"] = None

        # translate each mem addr into meaningful string data of the field
        field_data = [m["obj_id"], m["mid"]]
        for ind, field in enumerate(m["field"]):
            if type(field[1]) != typ.Constant:
                val = repr(field[1].typ)
            else:
                val = repr(field[1].exe)
            field_data.append((field[0], val, str(field[1])))
        grp.append((field_data, ent))

    field_id_bind = {}

    # formatting into file data
    file_data = []
    for m, f in grp:
        s = f"{m[0]} {m[1]} "
        for intf in f:
            field_id_bind[intf['%short_id%']] = intf['fld_nm']
            if repr(intf["fld_typ"]) == "i":
                s += f"${intf['%short_id%']}:{intf['%fld_data_typ%']}{intf['connectee']}$ "
            elif repr(intf["fld_typ"]) == "o":
                s += f"%{intf['%short_id%']}:{intf['%fld_data_typ%']}{intf['connectee']}% "
            elif repr(intf["fld_typ"]) == "c":
                s += f"@{intf['%short_id%']}:{intf['cid'].go_id} {repr(intf['cid'])}@ "
            # print(intf["fld_nm"], intf["fld_typ"])

        file_data.append(s+"\n")

    file_data.append("~\n")
    for i in field_id_bind:
        file_data.append(f"{i} {field_id_bind[i]}\n")

    with open("skeleton.dat.bin", "w") as fbj:
        fbj.writelines(file_data)


def loadSkel():
    fdt = []
    with open("skeleton.dat.bin", "r") as fbj:
        raw = fbj.readlines()

    fdt = raw[:raw.index("~\n")]
    tbl = raw[raw.index("~\n")+1:]

    short_id_bind = {}
    for l in tbl:
        short_id_bind[l.split(" ")[0]] = l.split(" ")[1].strip("\n")

    frmt = []

    # format the file data
    for f in fdt:
        manp = []
        nested = False
        buf = ""
        for c in f:
            if (c == " " or c == "\n") and not nested:
                manp.append(buf)
                buf = ""
            elif c in ["@", "$", "%"] and nested:
                nested = False
                buf += c
            elif c in ["@", "$", "%"]:
                nested = True
                buf += c
            else:
                buf += c
        frmt.append(manp)

    pyd = []
    # transfer data into python data
    for l in frmt:
        obj = {}
        obj["model"] = int(l[1])
        obj["field"] = {}

        for fld in l[2:]:  # TODO: Problems when there is \n or not
            dat = fld.translate({ord(i): None for i in '@$%'}).split(":")
            obj["field"][dat[0]] = {}
            obj["field"][dat[0]]["value"] = None

            if fld[0] == "@":
                obj["field"][dat[0]]["go"] = int(dat[1].split(" ")[0])
                obj["field"][dat[0]]["data"] = dat[1].split(" ")[1]
                obj["field"][dat[0]]["node"] = "c"
            elif fld[0] == "$":
                obj["field"][dat[0]]["type"] = dat[1][:dat[1].index("[")]
                cnc = dat[1][dat[1].index("["):]
                obj["field"][dat[0]]["connect"] = [int(i) for i in cnc[1:-1].split(", ") if i != ""]
                obj["field"][dat[0]]["node"] = "i"
            elif fld[0] == "%":
                obj["field"][dat[0]]["type"] = dat[1][:dat[1].index("[")]
                cnc = dat[1][dat[1].index("["):]
                obj["field"][dat[0]]["connect"] = [int(i) for i in cnc[1:-1].split(", ") if i != ""]
                obj["field"][dat[0]]["node"] = "o"
        pyd.append(obj)
    return pyd, short_id_bind

def execSkel(dat, id_bind):
    # this retrieves the user-defined class information from that file
    get_class = lambda c: [i for i in c.__dict__ if i[0:2] != "__" and i[0] == i[0].upper()]
    # bind = lambda d, k, v : {k:v for o in d}

    from src.model_config import model
    from src.model_config import graphic_object

    cls = get_class(model)
    go = get_class(graphic_object)

    # binding model id to the model class itself
    bind_cls = {}
    for c in cls:
        bind_cls[eval(f"model.{c}.mid")] = eval(f"model.{c}")

    bind_go = {}
    for o in go:
        bind_go[eval(f"graphic_object.{o}.go_id")] = eval(f"graphic_object.{o}")

    # execute <root> models first: the ones without input
    for mdl in dat:
        appnd = True
        for f in mdl["field"]:
            if mdl["field"][f]["node"] == "i":
                appnd = False
        if appnd:
            local_bind_go = {id_bind[i]:i for i in list(mdl["field"])}
            cnst = {i: mdl["field"][i]["data"]
                    for i in mdl["field"] if mdl["field"][i]["node"] == "c"}
            cnst = {id_bind[i]:cnst[i] for i in cnst}

            out = bind_cls[mdl["model"]].execute(inp={}, const=cnst)
            out = {local_bind_go[i]:out[i] for i in out}

            # binding the output value to the output fields
            for f in out:
                mdl["field"][f]["value"] = out[f]

            # posting the output value
            for f in mdl["field"]:
                if mdl["field"][f]["node"] == "o":
                    for fid in mdl["field"][f]["connect"]:
                        # find the model
                        for m in dat:
                            if fid in list(m["field"]):
                                m["field"][fid]["value"] = m["field"][f]["value"]

    stack = []
    while True:
        for mdl in dat:
            l = [True if mdl["field"][i]["node"] == "i" else False for i in mdl["field"]]
            go_run = True
            # retrieving the input value
            for f in mdl["field"]:
                if mdl["field"][f]["node"] == "i":
                    id_in = True
                    if mdl["field"][f]["value"] is None:  # input has no value
                        if mdl["field"][f]["connect"] != []: # has connectors
                            # putting the value from the external output into the internal input
                            good = True
                            id_in = False
                            for fid in mdl["field"][f]["connect"]:
                                fid = str(fid)
                                # find the model
                                for m in dat:
                                    if fid in list(m["field"]) and mdl != m:
                                        id_in = True
                                        mdl["field"][f]["value"] = m["field"][fid]["value"]
                                        if mdl["field"][f]["value"] == None:  # if the ext output still ='s None
                                            good = False
                        else:  # has no connectors
                            good = False
                            stack.append(f)
                    else:  # input has value
                        if mdl["field"][f]["connect"] != []: # has connectors
                            good = True
                        else:  # has no connectors (impossible)
                            good = False  # sets to False even if the input is set manually to prevent confusion
                    if good is False and id_in:
                        go_run = False
                else: # if the input type is not input
                    pass
            if go_run and any(l):  # And model must have input
                # TODO: input the code to execute the function
                local_bind_go = {id_bind[i]: i for i in list(mdl["field"])}
                cnst = {i: mdl["field"][i]["data"]
                        for i in mdl["field"] if mdl["field"][i]["node"] == "c"}
                cnst = {id_bind[i]: cnst[i] for i in cnst}

                inp = {i: mdl["field"][i]["value"]
                        for i in mdl["field"] if mdl["field"][i]["node"] == "i"}
                inp = {id_bind[i]: inp[i] for i in inp}

                out = bind_cls[mdl["model"]].execute(inp=inp, const=cnst)
                out = {local_bind_go[i]: out[i] for i in out}

                # binding the output value to the output fields
                for f in out:
                    mdl["field"][f]["value"] = out[f]

                # posting the output value
                for f in mdl["field"]:
                    if mdl["field"][f]["node"] == "o":
                        for fid in mdl["field"][f]["connect"]:
                            # find the model
                            for m in dat:
                                if fid in list(m["field"]):
                                    m["field"][fid]["value"] = m["field"][f]["value"]
        print(stack)
        if stack == []:  # emulating do-while loop
            break
        dat = stack
        stack = []


dt, idb = loadSkel()
execSkel(dt, idb)

"""
cool reference

to remove a set of character from a string
dat = fld.translate({ord(i): None for i in '@$%'})

"""