"""
The main process of execution in the program

Save Skeleton: Saves the empty models in place
Save Model: Saves all the parametized settings in each of model

Execute Skeleton: Executes all the user input and other input output
Execute ML: Automatically changes each settings of the model

"""

from src.model_config import node_types as ndtyp
import yaml

# this retrieves the user-defined class information from that file
get_class = lambda c: [i for i in c.__dict__ if i[0:2] != "__" and i[0] == i[0].upper()]

# number encode to different base
def enc(num, base=128):
    if num == 0: return [0]
    place = 1
    val = []
    after_zero = False
    while num%(base**place)//base**(place-1) != 0 or not after_zero or len(val) == 0:
        val.insert(0, num%(base**place)//base**(place-1))
        if val[0] != 0:
            after_zero = True
        place += 1
    return val

def dec(num, base=128):
    val = 0
    for digit, n in enumerate(reversed(num)):
        val += n*base**(digit)
    return val

# binary string format
def binf(*args):
    dat = b""
    for s in args:
        if type(s) == bytes or type(s) == bytearray:
            dat += s
        else:
            if type(s) != str: buf = str(s)
            else: buf = s
            try:
                dat += buf.encode("ascii")
            except UnicodeEncodeError:
                dat += buf.encode("utf-16")
    return dat

def bin_trans(s, trns):
    dt = s
    for k in trns:
        dt = dt.replace(k, trns[k])
    return dt

# saves the skeleton
def saveSkel(self, path):
    cfg = yaml.safe_load(open("config.yaml", "r").read())
    char = cfg["file_cfg"]["delimeter"]
    # initialize specific entities
    fld = self.entity(self.ENTITIES, ["obj_id","fld_dt"])
    mdl = self.entity(self.ENTITIES, ["obj_id","model"])

    # inject %short_id% into each entities for easier locating the entities
    inj = []
    for fdt, fid in zip(self.entity_data(fld), fld):
        fdt["%short_id%"] = bytearray([128+i for i in enc(self.short_id(fid))])
        inj.append(fdt)

    # modelization: grouping fields into models
    grp = []
    for m in self.entity_data(mdl):
        ent = []
        # get the model's fields
        for f in inj:
            if m["child"] == f["obj_id"]:
                if repr(f["fld_dt"][1]) == "c":
                    ent.append(self.entity_pp_cmpnt([f], ["obj_id", "fld_dt", "%short_id%"], strict=True)[0])
                else:
                    ent.append(self.entity_pp_cmpnt([f], ["obj_id", "fld_dt", "connectee", "%short_id%"], strict=True)[0])
                    ent[-1]["%fld_data_typ%"] = f["fld_dt"][1].typ.__name__

        # translate each mem addr into meaningful string data of the field
        field_data = [m["obj_id"], m["model"].mid]
        for ind, field in enumerate(m["model"].field):
            if type(field[1]) != ndtyp.Constant: val = repr(field[1].typ)
            else: val = repr(field[1].exe)
            field_data.append((field[0], val, str(field[1])))
        grp.append((field_data, ent))

    # print(grp)

    field_id_bind = {}

    # formatting into file data
    file_data = []
    for m, f in grp:
        s = binf(m[0],char["spc"],m[1],char["spc"])
        for intf in f:
            field_id_bind[bytes(intf['%short_id%'])] = binf(intf['fld_dt'][0])
            cid = intf['fld_dt'][1]
            if repr(intf['fld_dt'][1]) == "i":
                s += binf(char['inp'],intf["%short_id%"],":",intf['%fld_data_typ%'],intf['connectee'],char['inp'],char['spc'])
            elif repr(intf['fld_dt'][1]) == "o":
                s += binf(char['out'],intf["%short_id%"],":",intf['%fld_data_typ%'],intf['connectee'],char['out'],char['spc'])
            elif repr(intf['fld_dt'][1]) == "c":
                s += binf(char['cns'],intf["%short_id%"],":",cid.exe.go_id,char['spc'],repr(cid.exe),char['cns'],char['spc'])
        file_data.append(s+b"\n")

    file_data.append(b"~\n")
    for i in field_id_bind:
        file_data.append(binf(i,char['spc'],field_id_bind[i],"\n"))

    with open(path+"skeleton.dat.bin", "wb") as fbj:
        fbj.writelines(file_data)


def loadSkel(path):
    cfg = yaml.safe_load(open("config.yaml", "r").read())
    char = cfg["file_cfg"]["delimeter"]
    char["spc"] = binf(char["spc"])
    char["inp"] = binf(char["inp"])
    char["out"] = binf(char["out"])
    char["cns"] = binf(char["cns"])

    try:
        with open(path+"skeleton.dat.bin", "rb") as fbj:
            raw = fbj.readlines()
    except FileNotFoundError:
        print("ERROR: FILE NOT FOUND")
    fdt = raw[:raw.index(b"~\n")]
    tbl = raw[raw.index(b"~\n")+1:]

    short_id_bind = {}
    for l in tbl:
        byt = l.split(char["spc"])[0]
        short_id_bind[dec([int(i)-128 for i in byt])] = char["spc"].join(l.split(char["spc"])[1:]).strip(b"\n").decode("ASCII")

    frmt = []

    # format the file data
    for f in fdt:
        manp = []
        nested = False
        buf = b""
        for c in f:
            c = bytes(bytearray([c]))
            if (c == char["spc"] or c == b"\n") and not nested:
                manp.append(buf)
                buf = b""
            elif c in [char["inp"], char["out"], char["cns"]] and nested:
                nested = False
                buf += c
            elif c in [char["inp"], char["out"], char["cns"]]:
                nested = True
                buf += c
            else:
                buf += c
        frmt.append(manp)

    pyd = []
    # transfer data into python data
    for l in frmt:
        if b"" in l: l.remove(b"")
        obj = {}
        obj["model"] = int(l[1])
        obj["field"] = {}
        for fld in l[2:]:  # TODO: Problems when there is \n or not
            dat = bin_trans(fld, {char["inp"]: b"", char["out"]: b"", char["cns"]: b""}).split(b":")
            dat[0] = dec([int(i)-128 for i in dat[0]])

            obj["field"][dat[0]] = {}
            obj["field"][dat[0]]["value"] = None
            # print(fld[0:1], fld)
            if fld[0:1] == char["cns"]:
                obj["field"][dat[0]]["go"] = int(dat[1].split(char["spc"])[0])
                obj["field"][dat[0]]["data"] = dat[1].split(char["spc"])[1].decode("ASCII")
                obj["field"][dat[0]]["node"] = "c"
            elif fld[0:1] == char["inp"]:
                obj["field"][dat[0]]["type"] = dat[1][:dat[1].index(b"[")].decode("ASCII")
                cnc = dat[1][dat[1].index(b"["):]
                obj["field"][dat[0]]["connect"] = [int(i) for i in cnc[1:-1].split(b", ") if i != b""]
                obj["field"][dat[0]]["node"] = "i"
            elif fld[0:1] == char["out"]:
                obj["field"][dat[0]]["type"] = dat[1][:dat[1].index(b"[")].decode("ASCII")
                cnc = dat[1][dat[1].index(b"["):]
                obj["field"][dat[0]]["connect"] = [int(i) for i in cnc[1:-1].split(b", ") if i != b""]
                obj["field"][dat[0]]["node"] = "o"
        pyd.append(obj)

    return pyd, short_id_bind

def execSkel(dat, id_bind):

    # bind = lambda d, k, v : {k:v for o in d}

    import os

    inst = {
        "root dir": "C:/users/andrew shen/desktop/projectemerald/MySampleProject/"
    }

    del os

    from src.model_config import model
    from src.model_config import graphic_object

    cls = get_class(model)
    go = get_class(graphic_object)

    # binding model id to the model class itself
    bind_cls = {}  # TODO: Remove this
    for c in cls:
        bind_cls[eval(f"model.{c}.mid")] = eval(f"model.{c}")

    bind_go = {}  # TODO: Remove this
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

            out = bind_cls[mdl["model"]].execute(inp={}, const=cnst, inst=inst)
            try:
                out = {local_bind_go[i]: out[i] for i in out}
            except KeyError as e:
                print(f"ERROR: The model <{bind_cls[mdl['model']].__name__}> returned an invalid field, {e} ")
                return False
            except TypeError:
                print(f"ERROR: The model <{bind_cls[mdl['model']].__name__}> did not returned a dictionary")
                print(f"This is used for binding the executed value for the other models")
                return False

            # binding the output value to the output fields
            for f in out:
                # print("OUT", mdl["field"][f]["type"], type(out[f]).__name__)
                if mdl["field"][f]["type"] == type(out[f]).__name__:  # check if the types are same
                    mdl["field"][f]["value"] = out[f]
                else:
                    mdl["field"][f]["value"] = out[f]
                    print(f"Error: Expected Type: {mdl['field'][f]['type']}, Resulted Type: {type(out[f]).__name__}")
            # posting the output value
            for f in mdl["field"]:
                if mdl["field"][f]["node"] == "o":
                    for fid in mdl["field"][f]["connect"]:
                        # find the model
                        for m in dat:
                            if fid in list(m["field"]):
                                m["field"][fid]["value"] = mdl["field"][f]["value"]

    stack = []
    running = dat
    auto_terminate = False
    while True:
        for mdl in running:
            MODEL_SKIP = False
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
                            stack.append(mdl)
                    else:  # input has value
                        if mdl["field"][f]["connect"] != []: # has connectors
                            good = True
                        else:  # has no connectors
                            good = True  # a value can still be set by other fields even when it does not have connector
                    if good is False and id_in:
                        go_run = False
                else: # if the input type is not input
                    pass
            if go_run and any(l):  # And model must have input
                bind_fild_out = {id_bind[i]: i for i in list(mdl["field"]) if mdl["field"][i]["node"] == "o"}
                cnst = {i: mdl["field"][i]["data"]
                        for i in mdl["field"] if mdl["field"][i]["node"] == "c"}
                cnst = {id_bind[i]: cnst[i] for i in cnst}

                inp = {}
                for i in mdl["field"]:  # backflow input design
                    if mdl["field"][i]["node"] == "i":
                        if mdl["field"][i]["value"] is None and mdl["field"][i]["connect"] != []:
                            fid = mdl["field"][i]["connect"][0]  # TODO: Might want to merge multiple input
                            for m in dat:
                                for f in m["field"]:
                                    if f == fid:
                                        if m["field"][fid]["value"] is not None:  # check if that model has been ran
                                            # check if the both field had the same type
                                            if mdl["field"][i]["type"] == m["field"][fid]["type"]:
                                                mdl["field"][i]["value"] = m["field"][fid]["value"]
                                        else:  # input backflow failed; will be added to the stack fow later execution
                                            stack.append(mdl)
                                            MODEL_SKIP = True
                                            break
                        else:
                            inp[i] = mdl["field"][i]["value"]

                if MODEL_SKIP: break

                inp = {i: mdl["field"][i]["value"]
                        for i in mdl["field"] if mdl["field"][i]["node"] == "i"}
                inp = {id_bind[i]: inp[i] for i in inp}

                out = bind_cls[mdl["model"]].execute(inp=inp, const=cnst, inst=inst)
                try:
                    out = {bind_fild_out[i]: out[i] for i in out}
                except KeyError as e:
                    print(f"ERROR: The model <{bind_cls[mdl['model']].__name__}> returned an invalid field, {e} ")
                    return False
                except TypeError:
                    print(f"ERROR: The model <{bind_cls[mdl['model']].__name__}> did not returned a dictionary")
                    print(f"This is used for binding the executed value for the other models")
                    return False

                # binding the output value to the output fields
                for f in out:
                    if mdl["field"][f]["type"] == type(out[f]).__name__:  # check if the types are same
                        mdl["field"][f]["value"] = out[f]
                    else:
                        # TODO: This will be removed when the type system is mature
                        mdl["field"][f]["value"] = out[f]
                        print(f"Error: Expected Type: {mdl['field'][f]['type']}, Resulted Type: {type(out[f]).__name__}")

                # posting the output value
                for f in mdl["field"]:
                    if mdl["field"][f]["node"] == "o":
                        for fid in mdl["field"][f]["connect"]:
                            # find the model
                            for m in dat:
                                if fid in list(m["field"]):
                                    m["field"][fid]["value"] = mdl["field"][f]["value"]
            else:  # the node is not input
                pass

            if MODEL_SKIP: continue

        if stack == running and auto_terminate:
            break
        elif stack == running:
            auto_terminate = True
        elif stack != running:
            auto_terminate = False

        if stack == []:  # emulating do-while loop
            break
        running = stack
        stack = []
    return True

if __name__ == '__main__':
    dt, idb = loadSkel("C:/users/andrew shen/desktop/projectemerald/MySampleProject/")
    execSkel(dt, idb)
