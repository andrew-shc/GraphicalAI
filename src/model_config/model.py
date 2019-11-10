"""

AI Model template data is stored in this file

"""
from .. import prefab as prfb
from . import graphic_object as go
from . import types as typ


# example model
class OperationModel:
    """
    /input/ is to define the input fields {FIELD NAME : FIELD TYPE}
    /output/ is to define the output fields {FIELD NAME : FIELD TYPE}
    /const/ is to define the user-defined variables [FIELD CLASSTYPE(PARAM)]
    """

    title = "Operation"
    mid = 0x0000

    def __init__(self, pos, rect, font_size):
        self.field = [
            ("inp_val", typ.Input(int)),
            ("out_val", typ.Output(int)),
            ("&OPERAND", typ.Constant(go.TextField("Operand:", font_size=font_size))),
        ]
        self.pos = pos
        self.rect = rect

    def create(self, world, master, child):
        """ Creates entities (back-end) for the model (front-end)
        :param world:
        :param master:
        :param child:
        :return:
        """
        prfb.box(world, child, master, self.mid, self.pos, self.rect, self.title, self.field)

    @staticmethod
    def execute(inp, const):
        print("MODEL OPERATION")
        print(inp)
        print(const)
        return {"out_val": "MODEL OP?"}

# retrieves the data from the file
class FileReceiver:
    title = "File Receiver"
    mid = 0x0001

    def __init__(self, pos, rect, font_size):
        self.field = [
            ("out_val", typ.Output(int)),
            ("&OPERAND", typ.Constant(go.TextField("File Name:", font_size=font_size))),
        ]
        self.pos = pos
        self.rect = rect

    def create(self, world, master, child):
        prfb.box(world, master, child, self.mid, self.pos, self.rect, self.title, self.field)

    @staticmethod
    def execute(inp, const):
        print("MODEL FILE RECEIVER")
        print(inp)
        print(const)
        return {"out_val": "FILE RCV?"}

# saves the data into file
class FileSaver:
    title = "File Saver"
    mid = 0x0002

    def __init__(self, pos, rect, font_size):
        self.field = [
            ("inp_val", typ.Input(int)),
            ("&OPERAND", typ.Constant(go.TextField("File Name:", font_size=font_size))),
        ]
        self.pos = pos
        self.rect = rect

    def create(self, world, master, child):
        prfb.box(world, master, child, self.mid, self.pos, self.rect, self.title, self.field)

    @staticmethod
    def execute(inp, const):
        print("MODEL FILE OUTPUTTER")
        print(inp)
        return {}
