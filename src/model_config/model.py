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

    def __init__(self, pos, rect, font_size):
        self.field = [
            ("inp_val", typ.Input(int)),
            ("out_val", typ.Output(int)),
            ("%OPERAND", typ.Constant(go.TextField("Operand:", font_size=font_size))),
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
        prfb.box(world, child, master, self.pos, self.rect, self.title, self.field)

    def execute(self, inp, const, out):
        print("MODEL OPERATION")
        return out

# retrieves the data from the file
class FileReceiver:
    title = "File Receiver"

    def __init__(self, pos, rect, font_size):
        self.field = [
            ("out_val", typ.Output(int)),
            ("%OPERAND", typ.Constant(go.TextField("File:", font_size=font_size))),
        ]
        self.pos = pos
        self.rect = rect

    def create(self, world, master, child):
        prfb.box(world, master, child, self.pos, self.rect, self.title, self.field)

    def execute(self, inp, const, out):
        print("MODEL FILE RECEIVER")
        return out

# saves the data into file
class FileSaver:
    title = "File Receiver"

    def __init__(self, pos, rect, font_size):
        self.field = [
            ("out_val", typ.Output(int)),
            ("%OPERAND", typ.Constant(go.TextField("File:", font_size=font_size))),
        ]
        self.pos = pos
        self.rect = rect

    def create(self, world, master, child):
        prfb.box(world, master, child, self.pos, self.rect, self.title, self.field)

    def execute(self, inp, const, out):
        print("MODEL FILE OUTPUTTER")
        return out
