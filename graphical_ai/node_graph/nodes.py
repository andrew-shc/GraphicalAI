from __base__ import *  # ~~~ automatically generated by __autoinject__.py ~~~

from io import StringIO

from model_view.node import *
from model_view.components import *
from node_graph.backend_test import *
from node_graph.training_weights import WeightRef, NodeWeights
from node_state import NodeState


class NodeExec:
    ndtg: str = None  # node tag for internal representation; must have 5 characters in length
    name: str = None  # node name
    state: NodeState = None  # node state {INPUT, OUTPUT, MEDIUM}
    weights: NodeWeights = None  # collection of weights nodes contains

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
        return FasterNode(scene, self.ndtg, self.name, self.state, len(self.weights) > 0, self.field_data, pos=pos)

    @staticmethod
    def _field_data():
        """
        returns pure field data for the nodes (must be at runtime since the QtWidget obj require a parent at runtime)
        """
        raise NotImplementedError()

    def execute(self, cycle):
        """
        the node's execution supplied with necessary inputs, outputs, constants, and project instance state.
        the project instance state can change between each execution cycles.
        """
        raise NotImplementedError()

    def descriptor(self):
        raise NotImplementedError()


class InputCSV(NodeExec):
    ndtg = "InpCV"
    name = "Input CSV"
    state = NodeState.INPUT
    weights = NodeWeights()

    @staticmethod
    def _field_data(): return {
            "input": {},
            "output": {"x": CT.T_ANY, "y": CT.T_ANY},
            "constant": {"fname": AttributeSelector(NodeState.INPUT), "has depn. var": CheckBox(default=True), "dependent var": LineInput("")}
        }

    def execute(self, cycle):
        if cycle["inp"][self.const["fname"]][0] == "file" or cycle["inp"][self.const["fname"]][0] == "file-content":
            if cycle["inp"][self.const["fname"]][0] == "file":  # type=file
                df = pd.read_csv(cycle["inp"][self.const["fname"]][1])  # data are the local path to the file
            else:  # type=file-content
                df = pd.read_csv(StringIO(cycle["inp"][self.const["fname"]][1]))  # data are the content of the 'file'

            # TODO: a better mechanism to differentiate a csv file for predicting (without targ out) and for training
            #   (with output). Currently, in predicting, an input file must not have dependent col. (the ans key)
            if self.const["has depn. var"] and not cycle["predicting?"]:
                y = df[self.const["dependent var"]]  # TODO: SEPARATE THIS FUNCTIONALITY (EACH COL. DONT HAVE TO BE #)
                ydt = y.map(
                    {k: v for (v, k) in enumerate(y.unique().tolist())}
                ).to_numpy()

                x = df.drop(self.const["dependent var"], axis=1)
                xdt = x.to_numpy()

                self.out["x"] = xdt
                self.out["y"] = ydt
            else:
                xdt = df.to_numpy()
                self.out["x"] = xdt
                self.out["y"] = None
        else:
            raise Exception()


class OutputCSV(NodeExec):
    ndtg = "OutCV"
    name = "Output CSV"
    state = NodeState.OUTPUT
    weights = NodeWeights()

    @staticmethod
    def _field_data(): return {
            "input": {"data": CT.T_ANY},
            "output": {},
            "constant": {"fname": AttributeSelector(NodeState.OUTPUT)}
        }

    def execute(self, cycle):
        # TODO: we should really leave the file op outside of the nodes inside the attributes
        #   this also makes it easier to intercept the output in training
        if not cycle["first"]:
            if cycle["out"][self.const["fname"]][0] == "file":
                pd.DataFrame(self.inp["data"].numpy()).to_csv(cycle["out"][self.const["fname"]][1])
            elif cycle["out"][self.const["fname"]][0] == "file-content":
                cycle["out"][self.const["fname"]] = (
                    cycle["out"][self.const["fname"]][0],
                    pd.DataFrame(self.inp["data"].numpy()).to_csv(),
                    ".csv"
                )
            else:
                raise Exception()


class LinearRegressionMDL(NodeExec):
    ndtg = "LRMDL"
    name = "Linear Regression"
    state = NodeState.MEDIUM
    weights = NodeWeights(WeightRef("coef"), WeightRef("bias"))

    @staticmethod
    def _field_data(): return {
            "input": {"x": CT.T_ANY},
            "output": {"result": CT.T_ANY},
            "constant": {}
        }

    def execute(self, cycle):
        if not cycle["first"]:
            # execute this for every other cycle other than the first cycle
            self.out["result"] = tf.math.reduce_sum(self.inp["x"] * self.weights["coef"].value, axis=1) + self.weights["bias"].value
        else:
            self.weights["coef"].format_value((4,))
            self.weights["bias"].format_value(None)


class LogisticRegressionMDL(NodeExec):
    ndtg = "LGMDL"
    name = "Logistic Regression"
    state = NodeState.MEDIUM
    weights = NodeWeights(WeightRef("unknown"))

    @staticmethod
    def _field_data(): return {
            "input": {"data": CT.T_ANY},
            "output": {"result": CT.T_ANY},
            "constant": {}
        }

    def execute(self, cycle):
        dprint("linear regression execution")
        linreg = ModelLogisticReg()  # TODO: add multiple independent variables

        # linreg.train(self.inp["data"][0], self.inp["data"][1], 50)
        # self.out["result"] = (linreg.bias, linreg.coef)


class AttributeSelectorTesting(NodeExec):
    ndtg = "ATTRS"
    name = "Logistic Regression"
    state = NodeState.MEDIUM
    weights = NodeWeights()

    @staticmethod
    def _field_data(): return {
            "input": {"INP": CT.T_ANY},
            "output": {"OUT": CT.T_ANY},
            "constant": {"test_var_selc": AttributeSelector(NodeState.INPUT), "output_test": AttributeSelector(NodeState.OUTPUT)}
        }

    def execute(self, cycle):
        dprint("linear regression execution")
        linreg = ModelLogisticReg()  # TODO: add multiple independent variables

        cycle["io-inp"]["constant"]

        # linreg.train(self.inp["data"][0], self.inp["data"][1], 50)
        # self.out["result"] = (linreg.bias, linreg.coef)


export = {
    "core": {
        "Input CSV": InputCSV,
        "Output CSV": OutputCSV,
        "Linear Regression": LinearRegressionMDL,
        "T variable selectors": AttributeSelectorTesting,
    },
    "single": {
    },
    "neural network": {
    },
}

__nd_cls = {i: export[s][i] for s in export for i in export[s]}
node_class_ref = {__nd_cls[c].ndtg: __nd_cls[c] for c in __nd_cls}
