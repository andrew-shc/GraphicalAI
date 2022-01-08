from __base__ import *  # ~~~ automatically generated by __autoinject__.py ~~~

from typing import List, Dict

import copy
import tensorflow as tf

from node_graph.nodes import node_class_ref
from node_graph.loss_funcs import LOSS_FUNCTIONS
from node_graph.training_weights import WeightRef
from node_state import NodeState
from errors import ModelExecutionRuntimeError, ModelExecutionError


class ModelPredictor:
    """
    Merely executes the `execute()` function for each node and handles the movement of input and output
    between nodes. The ModelPredictor assumes all weights have been properly trained.
    """
    # TODO: executor will need info about variable selection, variable specifier, etc.

    def __init__(self, model_exec_data, weights: List[tf.Variable]):
        # each individual nodes are labelled with an id based on its index in the model exec data list
        self.mdl_ref_dt = copy.deepcopy(model_exec_data)  # mapper between node-exec id and the actual node data
        self.inp_ref_nd = {}  # mapper between input id to its respective node (through node id) and its name
        self.node_anchors = []
        self.global_weights_vec: List[tf.Variable] = weights

        self.node_adj_list = {nid:[] for nid in range(0, len(self.mdl_ref_dt))}
        for (nid, nd) in enumerate(self.mdl_ref_dt):
            nd["%%class"] = node_class_ref[nd["ndtg"]]()
            # dprint(nd, nd["%%class"].state)
            # dprint(nid, nd["inp"])
            # dprint("zip?", nd["inp"], nd["%%class"].field_data()["input"])
            for (inp_id, inp_nm) in zip(nd["inp"], nd["%%class"].field_data["input"]):
                self.inp_ref_nd[inp_id] = (nid, inp_nm)
            for (out_nid, out_nd) in enumerate(self.mdl_ref_dt):
                out_fld = [j for i in out_nd["out"] for j in i]
                if len(nd["inp"]+out_fld) > len(set(nd["inp"]) | set(out_fld)):
                    self.node_adj_list[out_nid].append(nid)
            for const_nm in nd["const"]:
                nd["const"][const_nm] = nd["%%class"].field_data["constant"][const_nm].bin_deserialize(nd["const"][const_nm])
            if nd["%%class"].state == NodeState.INPUT:
                self.node_anchors.append(nid)
            # dprint("FIELD APPENDING", nd["inp"], nd["out"])
        # dprint(self.node_adj_list)

    def execute(self, inst_state) -> Dict[str, tuple]:
        dprint("Model Prediction Begin")

        # resets the weights to immediately prepare for the next round of execution
        for nd in self.mdl_ref_dt:
            nd["%%class"].weights.reset()

        self.cycle_exec(inst_state, init_setup=True)
        self.cycle_exec(inst_state)

        dprint("Model Prediction Finished")

        return inst_state["out"]

    def cycle_exec(self, cycle_state, init_setup=False):
        """
        executes the model node graph
        """
        dprint("Model Prediction Cycle Begin")

        cycle_state["first"] = init_setup

        # dprint("MAPPER", self.mdl_ref_dt)
        # dprint("INPREF", self.inp_ref_nd)
        # dprint("ANCHOR", self.node_anchors)
        # dprint("ADJLST", self.node_adj_list)

        # this is a modified breadth-first search where there are no visited queue, because first time you visit
        # Node A, it might not be ready till all the other connected nodes assigns the values to Node A's input.
        # In other words, calling the already visited Node A is OK, and once the last connected node refers to Node A,
        # then it will allow Node A to execute (because then all the Node A's inputs are assigned with values).

        weights_activated = 0
        queue = self.node_anchors.copy()
        while len(queue) != 0:
            first = queue[0]
            del queue[0]
            nd_dt = self.mdl_ref_dt[first]  # note: reference (not copy)
            fld_meta = nd_dt["%%class"].field_data

            for nd_ref in self.node_adj_list[first]:
                queue.append(nd_ref)

            # dprint("STATE:", nd_dt["%%class"].state)
            # dprint("FIELD:", fld_meta)
            # dprint("ND DT:", nd_dt)

            # per each node executed
            # ----------------------
            # 1. check all input field data is filled
            # 2. retrieve all the constant's value
            # 3. execute the node
            # 4. check output field data is valid
            #   ~ Are all necessary fields filled (else return a warning and fill that field with None)
            #   ~ Additional unknown fields will be sent out as a warning and break
            #   ~ [Tentative:TypeChecking] If that output field does not have a correct type (else return a warning)
            # 5. Find each output field's reference input field ID through the mapper to find the node
            # 6. Fill the referenced input field with the data from output
            # --- done ---

            if nd_dt["%%class"].state != NodeState.INPUT:
                # dprint("INP", nd_dt["%%class"].inp)
                valid_inp = True
                for ifld_nm in fld_meta["input"]:
                    if ifld_nm not in nd_dt["%%class"].inp:
                        valid_inp = False
                        break
                if valid_inp is False:
                    dprint("warning: incomplete input")
                    continue

            # NOTE: retrieving value directly from the constant widget object itself rather than deserializing
            #   binary data is not garunteed to have the same value as the user specified, as this class strives
            #   to be independent from node data. Only from the read binary data.
            nd_dt["%%class"].const = nd_dt["const"]  # {k:fld_meta["constant"][k].value() for k in fld_meta["constant"]}
            try:
                nd_dt["%%class"].execute(cycle_state)
                if init_setup and len(nd_dt["%%class"].weights) != 0:
                    # activates the weight
                    w: WeightRef
                    for w in nd_dt["%%class"].weights.collection:
                        # fyi, activation happens after the node has set the weight's shape
                        w.activate_set(self.global_weights_vec, weights_activated)
                        weights_activated += 1
            except ModelExecutionRuntimeError as e:
                raise e
            except BaseException as e:
                raise ModelExecutionError(msg=e, code=ModelExecutionError.DEBUG_ERROR)

            if nd_dt["%%class"].state != NodeState.OUTPUT:
                # dprint("OUT", nd_dt["%%class"].out)
                for (ind, ofld_nm) in enumerate(fld_meta["output"]):
                    # each output field in this node
                    if ofld_nm not in nd_dt["%%class"].out:
                        dprint(f"warning: output field <{ofld_nm}> is missing; will be replaced with None")
                        nd_dt["%%class"].out[ofld_nm] = None
                    for inp_ref in nd_dt["out"][ind]:
                        # each referenced input of ext node of the individual output field in the current master node
                        ext_node = self.mdl_ref_dt[self.inp_ref_nd[inp_ref][0]]
                        ext_node["%%class"].inp[self.inp_ref_nd[inp_ref][1]] = nd_dt["%%class"].out[ofld_nm]
                # dprint(nd_dt["%%class"].out)

            # TODO: create a diagram why we do this instead of using visited list
            # this is it removes any additional occurrences of the current <first> node presently from the queue, as to
            # not repeat, while also allow loops with at least 2 different node instance it has to loop through
            # (or else it just directly refers back to the queue and get removed instantly and its unreadable
            # w/ a single node instance loop)
            queue = [n for n in queue if n != first]

        dprint("Model Prediction Cycle Finished")


# TODO: add an option to automatically initialize the global weights vec like to random, linear steps, init value, etc.
class ModelTrainer:
    """
    Similar to the purpose of ModelPredictor, but this time, its like the "debug" version of the ModelPredictor, with
    more things to keep track of the weights and recurring-ly update the model.

    MODEL ASSUMPTION (PROGRAMMED WITHIN, NO WORRIES): THERE WILL BE ONLY ONE INPUT & OUTPUT NODE
    """

    def __init__(self, model_exec_data):
        self.global_weights_vec: List[tf.Variable] = []
        self.interim_pred = None

        self.mdl_ref_dt = copy.deepcopy(model_exec_data)
        self.inp_ref_nd = {}
        self.node_anchors = []

        self.expc_out = None  # the expected output/prediction (i.e. the answer key)

        """
        Model Reference Data
        --------------------
        [
            Node {
                node tag "ndtg": str,
                input numerical ids for each input fields "inp": [int],
                output per index is another list of input numerical ids connecting with the output "out": [[int]],
                constant fields "const": ConstantFields {
                    constant field name: its binary data
                }
            },
               .
               .
               .
        ]
        """

        self.node_adj_list = {nid: [] for nid in range(0, len(self.mdl_ref_dt))}
        for (nid, nd) in enumerate(self.mdl_ref_dt):
            nd["%%class"] = node_class_ref[nd["ndtg"]]()
            for (inp_id, inp_nm) in zip(nd["inp"], nd["%%class"].field_data["input"]):
                self.inp_ref_nd[inp_id] = (nid, inp_nm)
            for (out_nid, out_nd) in enumerate(self.mdl_ref_dt):
                out_fld = [j for i in out_nd["out"] for j in i]
                if len(nd["inp"]+out_fld) > len(set(nd["inp"]) | set(out_fld)):
                    self.node_adj_list[out_nid].append(nid)
            for const_nm in nd["const"]:  # convert constant field binary data into usable data by custom deserialization
                nd["const"][const_nm] = nd["%%class"].field_data["constant"][const_nm].bin_deserialize(
                    nd["const"][const_nm])
            if nd["%%class"].state == NodeState.INPUT:
                self.node_anchors.append(nid)

    def execute(self, iterations: int, loss_name: str, rate: float, inst_state):
        """
        1. find the anchor nodes
        2. execute the first cycle tracking down all the weights
        3. re-execute again and again
        """
        dprint("Model Training Begin")
        dprint(f"Iterations {iterations} - Loss {loss_name} - Rate {rate}")

        loss_func = LOSS_FUNCTIONS[loss_name]

        self.cycle_exec(inst_state, init_setup=True)
        dprint("GLOBAL WEIGHTS VEC", self.global_weights_vec)

        for _ in range(iterations-1):
            # ndtg, inp = self.cycle_exec(inst_state, intercept_out=True)
            # if ndtg == "OutCV":
            #     pred = inp["data"]

                with tf.GradientTape(persistent=True) as g:
                    ndtg, inp = self.cycle_exec(inst_state, intercept_out=True)
                    if ndtg == "OutCV":
                        loss: tf.Tensor = loss_func(inp["data"], self.expc_out)

                dl_dw = g.gradient(loss, self.global_weights_vec)
                dprint("LOSS", loss.numpy())
                dprint("GRADIENT", dl_dw)

                for i, w in enumerate(self.global_weights_vec):
                    w.assign_sub(rate * dl_dw[i])

                #     linreg.coef.assign_sub(learning_rate * dl_dw2)
                #     linreg.bias.assign_sub(learning_rate * dl_db2)

        self.cycle_exec(inst_state)  # so the final output without interception can be fully executed

        # resets the weights in-preparation for the next execution
        for nd in self.mdl_ref_dt:
            nd["%%class"].weights.reset()

        dprint("Model Training Finished")

    def cycle_exec(self, cycle_state, init_setup=False, intercept_out=False):
        """
        first defines whether the cycle is first or not. It is to determine whether this cycle should do weight
        initialization and other prep work.
        """

        dprint("Model Training Cycle Begin")

        cycle_state["first"] = init_setup

        # dprint("MAPPER", self.mdl_ref_dt)
        # dprint("INPREF", self.inp_ref_nd)
        # dprint("ANCHOR", self.node_anchors)
        # dprint("ADJLST", self.node_adj_list)

        queue = self.node_anchors.copy()
        while len(queue) != 0:
            first = queue[0]
            del queue[0]

            nd_dt = self.mdl_ref_dt[first]  # note: reference (not copy)
            fld_meta = nd_dt["%%class"].field_data

            for nd_ref in self.node_adj_list[first]:
                queue.append(nd_ref)

            # dprint("STATE:", nd_dt["%%class"].state)
            # dprint("FIELD:", fld_meta)
            # dprint("ND DT:", nd_dt)

            if nd_dt["%%class"].state != NodeState.INPUT:
                valid_inp = True
                for ifld_nm in fld_meta["input"]:
                    if ifld_nm not in nd_dt["%%class"].inp:
                        valid_inp = False
                        break
                if valid_inp is False:
                    dprint("warning: incomplete input")
                    continue

            nd_dt["%%class"].const = nd_dt["const"]  # {k:fld_meta["constant"][k].value() for k in fld_meta["constant"]}
            try:
                if nd_dt["%%class"].state == NodeState.OUTPUT and intercept_out:
                    return (nd_dt["%%class"].ndtg, nd_dt["%%class"].inp)
                nd_dt["%%class"].execute(cycle_state)
                if init_setup and len(nd_dt["%%class"].weights) != 0:
                    # activates the weight
                    w: WeightRef
                    for w in nd_dt["%%class"].weights.collection:
                        # fyi, activation happens after the node has set the weight's shape
                        w.activate(self.global_weights_vec)
            except ModelExecutionRuntimeError as e:
                raise e
            except BaseException as e:
                raise ModelExecutionError(msg=e, code=ModelExecutionError.DEBUG_ERROR)

            if nd_dt["%%class"].state != NodeState.OUTPUT:
                # dprint("OUT", nd_dt["%%class"].out)
                for (ind, ofld_nm) in enumerate(fld_meta["output"]):
                    # each output field in this node
                    if ofld_nm not in nd_dt["%%class"].out:
                        dprint(f"warning: output field <{ofld_nm}> is missing; will be replaced with None")
                        nd_dt["%%class"].out[ofld_nm] = None
                    for inp_ref in nd_dt["out"][ind]:
                        # each referenced input of ext node of the individual output field in the current master node
                        ext_node = self.mdl_ref_dt[self.inp_ref_nd[inp_ref][0]]
                        ext_node["%%class"].inp[self.inp_ref_nd[inp_ref][1]] = nd_dt["%%class"].out[ofld_nm]
                # dprint(nd_dt["%%class"].out)

                if init_setup and nd_dt["%%class"].ndtg == "InpCV":
                    self.expc_out = nd_dt["%%class"].out["y"]

            # TODO: create a diagram why we do this instead of using visited list
            # this is it removes any additional occurrences of the current <first> node presently from the queue, as to
            # not repeat, while also allow loops with at least 2 different node instance it has to loop through
            # (or else it just directly refers back to the queue and get removed instantly and its unreadable
            # w/ a single node instance loop)

            # dprint("removes add. occur. eh?", queue, first)
            queue = [n for n in queue if n != first]

        dprint("Model Training Cycle Finished")

        return (None, None)

