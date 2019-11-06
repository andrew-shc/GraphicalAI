"""
The main process of execution in the program

Save Skeleton: Saves the empty models in place
Save Model: Saves all the parametized settings in each of model

Execute Skeleton: Executes all the user input and other input output
Execute ML: Automatically changes each settings of the model

"""

from src. model_config import types as typ

APP_DIR = "C:/Users/Andrew Shen/Desktop/ProjectEmerald/src2/test1"
PROJECT_FILE = "/project_test_4.dat"

# saves the skeleton
def saveSkel(self):
    print("\n\n\n")
    # initialize specific entities
    fld = self.entity(self.ENTITIES, ["obj_id","fld_nm","fld_typ"])
    mdl = self.entity(self.ENTITIES, ["obj_id","field"])

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
                if f["fld_typ"] == typ.Constant:
                    ent.append(self.entity_pp_cmpnt([f], ["obj_id", "fld_nm", "fld_typ"], strict=True))
                else:
                    ent.append(self.entity_pp_cmpnt([f], ["obj_id", "fld_nm", "fld_typ", "connectee"], strict=True))

        # translate each mem addr into meaningful string data of the field
        field_data = []
        for ind, field in enumerate(m["field"]):
            field_data.append((field[0], field[1].typ if type(field[1]) != typ.Constant else field[1].exe, str(field[1])))
        grp.append((field_data, ent))


    for i in grp:
        print(i)

