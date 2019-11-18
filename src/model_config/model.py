"""

AI Model template data is stored in this file

"""
from .. import prefab as prfb
from . import graphic_object as go
from . import node_types as typ

import sklearn as skl


# example model
class OperationModel:
    """
    /input/ is to define the input fields {FIELD NAME : FIELD TYPE}
    /output/ is to define the output fields {FIELD NAME : FIELD TYPE}
    /const/ is to define the user-defined variables [FIELD CLASSTYPE(PARAM)]

    title: The title name to display for the model
    mid: an id to be easily identified by other files
    """

    title = "Operation"
    mid = 0x0000

    def __init__(self, pos, rect, font_size):
        """
        :param pos: Position of the model
        :param rect: Rect shape of the model
        :param font_size: Font size foe the model fields
        """
        self.field = [  # WARNING: CHANGING THE FIELD DATA WILL ASYNC THE FIELD FROM THE DATA FILE
            ("input", typ.Input(int)),
            ("output", typ.Output(int)),
            ("&OPERAND", typ.Constant(go.TextField("Operand:", font_size=font_size))),
        ]
        self.pos = pos
        self.rect = rect

    def create(self, world, master, child):
        """ Creates entities (back-end) for the model (front-end)
        :param world: The <World> class instance
        :param master: master object id
        :param child: child objects id
        :return:
        """
        prfb.modelBox(world, child, master, self.pos, self.rect, self)

    @staticmethod
    def execute(inp, const, inst,):
        """ Executes on behalf of the executor
        :param inp: Input values from the nodes the user selected
        :param const: Constant values (Users selected values)
        :return: returns the Output values and gets copied to other fields the user selected
        """
        ans = 0
        if const["&OPERAND"] == "+":
            ans = int(inp["input"])+5
        elif const["&OPERAND"] == "-":
            ans = int(inp["input"])-5
        elif const["&OPERAND"] == "*":
            ans = int(inp["input"])*5
        elif const["&OPERAND"] == "/":
            ans = int(inp["input"])/5
        else:
            print(f"Operand {const['&OPERAND']} is either unavaliable or invalid! (Supports basic 4 operation)")

        return {"output": ans}

# ========== REAL MODELS ==========


# retrieves the data from the file
class FileReceiver:
    title = "File Receiver"
    mid = 0x0001

    def __init__(self, pos, rect, font_size):
        self.field = [
            ("generic data", typ.Output(int)),
            ("&FNAME", typ.Constant(go.TextField("File Name:", font_size=font_size))),
        ]
        self.pos = pos
        self.rect = rect

    def create(self, world, master, child):
        prfb.modelBox(world, child, master, self.pos, self.rect, self)

    @staticmethod
    def execute(inp, const, inst,):
        with open(inst["root dir"]+"\\"+const["&FNAME"], "r") as fbj:
            fdt = fbj.readlines()
        return {"generic data": fdt[0]}


# saves the data into file
class FileSaver:
    title = "File Saver"
    mid = 0x0002

    def __init__(self, pos, rect, font_size):
        self.field = [
            ("generic data", typ.Input(int)),
            ("&FNAME", typ.Constant(go.TextField("File Name:", font_size=font_size))),
        ]
        self.pos = pos
        self.rect = rect

    def create(self, world, master, child):
        prfb.modelBox(world, child, master, self.pos, self.rect, self)

    @staticmethod
    def execute(inp, const, inst,):
        with open(inst["root dir"]+"\\"+const["&FNAME"], "w") as fbj:
            fbj.writelines([str(inp["generic data"])+"\n"])
        return {}


# Support Vector Machine - SVC Model
class SVCModel:  # TODO
    title = "SVM - SVC Model"
    mid = 0x0003

    def __init__(self, pos, rect, font_size):
        self.field = [
            ("numeric data", typ.Input(list)),
            ("classification", typ.Input(list)),
            ("model", typ.Output(int)),
        ]
        self.pos = pos
        self.rect = rect

    def create(self, world, master, child):
        prfb.modelBox(world, child, master, self.pos, self.rect, self)

    @staticmethod
    def execute(inp, const, inst,):  # TODO: Find a way to data serialize the model
        model = skl.svm.SVC()
        model.fit(inp["numeric data"], inp["classification"])
        return {"model": model}


# Support Vector Machine - SVC Model
class ModelTrain:  # TODO
    title = "Train Model (for SVC only)"
    mid = 0x0004

    def __init__(self, pos, rect, font_size):
        self.field = [
            ("model", typ.Input(list)),
            ("result", typ.Output(str)),
            ("&predict", typ.Constant(go.TextField("User Input:", font_size=font_size))),
        ]
        self.pos = pos
        self.rect = rect

    def create(self, world, master, child):
        prfb.modelBox(world, child, master, self.pos, self.rect, self)

    @staticmethod
    def execute(inp, const, inst,):
        prd = [int(i) for i in const["&predict"].split(" ")]
        r = " - ".join(inp["model"].predict([prd]))
        return {"result": r}