from PySide6.QtWidgets import QGraphicsScene
from enum import Enum

from model_view.node import *
from model_view.components import *


class NodeState(Enum):
    INPUT = 1
    OUTPUT = 2
    MEDIUM = 3


class NodeExec:
    ndtg = None  # node tag for internal representation; must have 5 characters in length
    name = None  # node name
    state = None  # node state {INPUT, OUTPUT, MEDIUM}

    def __init__(self):
        # values for each field at runtime
        # these intermediate variables are so it is easier to analyze errors and visualization
        self.inp = {}
        self.out = {}
        self.const = {}
        self.field_data = self._field_data()

    def interface(self, scene: QGraphicsScene, pos: tuple) -> FasterNode:
        """
        the GUI frontend code of the nodes
        """
        raise NotImplementedError()

    @staticmethod
    def _field_data():
        """
        returns pure field data for the nodes (must be at runtime since the QtWidget obj reqr a Qt Parent at runtime)
        """
        raise NotImplementedError()

    def execute(self, inst):
        """
        the node's execution supplied with necessary inputs, outputs, constants, and project instance state.
        """
        raise NotImplementedError()

    def descriptor(self):
        raise NotImplementedError()


class InputDataND(NodeExec):
    ndtg = "InpDT"
    name = "Input Data"
    state = NodeState.INPUT
    # field_data_n = {
    #         "input": {"inp field A": CT.T_ANY},
    #         "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
    #         "constant": {"const field A": ComboBox(["a", "b"])},
    #     }

    def interface(self, scene: QGraphicsScene, pos: tuple) -> FasterNode:
        return FasterNode(scene, self, self.field_data, pos=pos)

    @staticmethod
    def _field_data():
        return {
            "input": {"inp field A": CT.T_ANY},
            "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
            "constant": {"const field A": ComboBox(["F", "Xssss"])},
        }
    # @staticmethod
    # def field_data():
    #     return {
    #         "input": {"inp field A": CT.T_ANY},
    #         "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
    #         "constant": {"const field A": ComboBox(["F", "Xssss"])},
    #     }

    def execute(self, inst):
        print("EXECUTE!!!", self.inp, self.out, self.const, inst)


class OutputDataND(NodeExec):
    ndtg = "OutDT"
    name = "Output Data"
    state = NodeState.OUTPUT
    # field_data_n = {
    #         "input": {"inp field A": CT.T_ANY},
    #         "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
    #         "constant": {"const field A": ComboBox(["Vrrr", "X"])},
    #     }

    def interface(self, scene: QGraphicsScene, pos: tuple) -> FasterNode:
        return FasterNode(scene, self, self.field_data, pos=pos)

    @staticmethod
    def _field_data():
        return {
            "input": {"inp field A": CT.T_ANY},
            "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
            "constant": {"const field A": ComboBox(["Vrrr", "X"])},
        }
    # @staticmethod
    # def field_data():
    #     return {
    #         "input": {"inp field A": CT.T_ANY},
    #         "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
    #         "constant": {"const field A": ComboBox},
    #     }

    def execute(self, inst):
        print("EXECUTE!!!", self.inp, self.out, self.const, inst)


class _TESTND_LongConst(NodeExec):
    ndtg = "XXXX0"
    name = "Testing Long Const"
    state = NodeState.MEDIUM
    # field_data_n = {
    #         "input": {"inp field A": CT.T_ANY, "inp field B": CT.T_ANY, "inp field C": CT.T_ANY},
    #         "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
    #         "constant": {"const field A": ComboBox(["None"]), "const field B": LineInput("default?"),
    #                      "const field C": ComboBox(["None"]), "const field D": LineInput("")},
    #     }

    def interface(self, scene: QGraphicsScene, pos: tuple) -> FasterNode:
        return FasterNode(scene, self, self.field_data, pos=pos)

    @staticmethod
    def _field_data():
        return {
            "input": {"inp field A": CT.T_ANY, "inp field B": CT.T_ANY, "inp field C": CT.T_ANY},
            "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
            "constant": {"const field A": ComboBox(["None"]), "const field B": LineInput("default?"),
                         "const field C": ComboBox(["None"]), "const field D": LineInput("")},
        }
    # @staticmethod
    # def field_data():
    #     return {
    #         "input": {"inp field A": CT.T_ANY, "inp field B": CT.T_ANY, "inp field C": CT.T_ANY},
    #         "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
    #         "constant": {"const field A": ComboBox, "const field B": LineInput,
    #                      "const field C": ComboBox, "const field D": LineInput},
    #     }

    def execute(self, inst):
        print("EXECUTE!!!", self.inp, self.out, self.const, inst)


class _TESTND_AllConst(NodeExec):
    ndtg = "XXXX1"
    name = "Testing All Const"
    state = NodeState.MEDIUM
    # field_data_n = {
    #         "input": {"inp field A": CT.T_ANY, "inp field B": CT.T_ANY, "inp field C": CT.T_ANY},
    #         "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
    #         "constant": {"const field A": IntLineInput(40), "const field B": LineInput("texxt"),
    #                      "const field C": ComboBox(["a", "b", "c"]), "CHECKKKK BOX----": CheckBox(),
    #                      "var selc": VariableSelector(), "multibox": MultiComboBox},
    # }

    def interface(self, scene: QGraphicsScene, pos: tuple) -> FasterNode:
        return FasterNode(scene, self, self.field_data, pos=pos)

    @staticmethod
    def _field_data():
        return {
            "input": {"inp field A": CT.T_ANY, "inp field B": CT.T_ANY, "inp field C": CT.T_ANY},
            "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
            "constant": {"const field A": IntLineInput(40), "const field B": LineInput("texxt"),
                         "const field C": ComboBox(["a", "b", "c"]), "CHECKKKK BOX----": CheckBox(),
                         "var selc": VariableSelector(), "multibox": MultiComboBox()},
    }
    # @staticmethod
    # def field_data():
    #     return {
    #         "input": {"inp field A": CT.T_ANY, "inp field B": CT.T_ANY, "inp field C": CT.T_ANY},
    #         "output": {"out field A": CT.T_ANY, "out field B": CT.T_ANY},
    #         "constant": {"const field A": IntLineInput, "const field B": LineInput,
    #                      "const field C": ComboBox, "CHECKKKK BOX----": CheckBox,
    #                      "var selc": VariableSelector, "multibox": MultiComboBox},
    #     }

    def execute(self, inst):
        print("EXECUTE!!!", self.inp, self.out, self.const, inst)



export = {
    "_test": {
        "long const": _TESTND_LongConst,
        "all const": _TESTND_AllConst,
    },
    "core": {
        "input data": InputDataND,
        "output data": OutputDataND,
    },
    "single": {
    },
    "neural network": {
    },
}

__nd_cls = {i: export[s][i] for s in export for i in export[s]}
node_class_ref = {__nd_cls[c].ndtg: __nd_cls[c] for c in __nd_cls}
