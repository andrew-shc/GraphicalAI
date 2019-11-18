"""
The 3 basic node type's class definition.


class Input and Output are semi-dummy class to differntiate between the nodes and types.
"""



class Input:
    def __init__(self, typ):
        """
        :param typ: Inherited from <Any> class
        """
        self.typ = typ

    # to read by the people
    def __str__(self):
        return "input type"

    # to be read by the executor
    def __repr__(self):
        return "i"

class Output:
    def __init__(self, typ):
        """
        :param typ: Inherited from <Any> class
        """
        self.typ = typ

    # to read by the people
    def __str__(self):
        return "output type"

    # to be read by the executor
    def __repr__(self):
        return "o"

class Constant:
    def __init__(self, exe):
        """
        :param exe: A class that executes the custom fields, aka constants
        """
        self.exe = exe

    # to read by the people
    def __str__(self):
        return "constant type"

    # to be read by the executor
    def __repr__(self):
        return "c"