"""
Project File Interface v1.0
	To interface the directory to the abstract file directory within the software. Loads models, training datasets, etc.
----------------------------

project root directory

deploy/  **NOTE: YET TO BE IMPLEMENTED**
test/  (final testing)
validator/  (parameterize the model)
train/  (fitting the model)
	*.csv - table datas
	*.png - picture formats
	... - video files, text files, etc.
model/
	M000.exec.dat (model executable data) - a executable ready data to be executed
	M000.proj.dat (model serialized data) - this shows the visualization of the model TODO: **UNSAFE: USES PICKLE**
	M000.grph.dat (model graph data) - this is to show the graphs of the result of the model
project.yaml
----------------------------
- project.yaml

-author: name
-created: mm/dd/yyyy hh:mm:ss
-updated: mm/dd/yyyy hh:mm:ss
-index: 0
-model
	-0
		-name:My Model
	-1
		-name:Another Model
	-2
		...
	...
----------------------------
~create_model()  # overwrites any previous save
~delete_model()  # just deletes the save
~obtain_model()  # reads the data of the save
 --- or ---
~save_model()
~read_model()
~delete(model_id, type)
"""
from __future__ import annotations

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

import yaml
import os

from src.debug import *
from src.gfx.connection import Connection
from src.gfx.connector import Connector
from src.gfx.node import Node
from src.constants import *

from typing import List, Optional, Union


def model_saver(items: List[Union[Node, Connector, Connection]]):  # TODO: Optimize and compact
	skl_tree = {}  # skeleton tree: pre-tree generation
	dat_tree = {}  # data tree: using skl_tree to generate data tree
	id_map = {}
	id_counter = 0

	# filling up nodes|connectors with allocated unique id (regardless of node type/field name)
	n: Node
	for n in [nd for nd in items if isinstance(nd, Node)]:
		skl_tree[id_counter] = {}
		id_map[id_counter] = n.central.nd_cls.title
		node_id = id_counter
		id_counter += 1

		connc: Connector  # only input|output connector
		for connc in n.central.connector:
			skl_tree[node_id][id_counter] = connc
			id_map[id_counter] = connc.field[Connector.FNAME]
			id_counter += 1

		for const in n.central.nd_cls.field["constant"]:  # only constant field
			skl_tree[node_id][id_counter] = const[1]
			id_map[id_counter] = const[0]
			id_counter += 1

	# filling up the tree with actual data
	n: Node
	for n in skl_tree:
		dat_tree[n] = {}
		for field in skl_tree[n]:
			connc = skl_tree[n][field]
			if isinstance(connc, Connector):  # input|output field
				cnc_typ = connc.tag
				fld_typ = connc.field[Connector.FTYPE]
				cnc_cnctn = []
				cnntn: Connection
				for cnntn in connc.connections:
					for int_n in skl_tree:
						for int_connc in skl_tree[int_n]:
							# uses each unique class reference instead of relying on unique field name
							#                                   (the name that users can see) -----^
							if cnntn.connector_b == skl_tree[int_n][int_connc]:
								cnc_cnctn.append(int_connc)
				dat_tree[n][field] = (cnc_typ, fld_typ, cnc_cnctn)
			else:  # constant field
				dat_tree[n][field] = (FLD_CONST, skl_tree[n][field].value())

	return _dat_file_saver(dat_tree, id_map)


def _dat_file_saver(model_tree, id_map):
	"""
	model_tree:
		node id:
			connector id: (connector type, data type, [connector id connections, ...]),
			connector id: (connector type = CONST, generic data),
	id_map:
		id: display name,
	"""

	ln = []
	tab = "    "

	for m in model_tree:  # each models
		ln.append(str(m))
		for f in model_tree[m]:  # each items (connectors)
			fld = model_tree[m][f]
			if fld[0] == TG_INPUT:
				ln.append(tab + str(f) + " << " + str(fld[1]) + "[" + ",".join([str(i) for i in fld[2]]) + "]")
			elif fld[0] == TG_OUTPUT:
				ln.append(tab + str(f) + " >> " + str(fld[1]) + "[" + ",".join([str(i) for i in fld[2]]) + "]")
			elif fld[0] == FLD_CONST:
				ln.append(tab + str(f) + " == " + str(fld[1]))

	ln.append("namespace")
	for o in id_map:  # each objects mapped to id
		ln.append(tab + str(o) + " " + str(id_map[o]))

	return ln

def dat_file_loader(fdt):
	fdt = [f.strip("\n") for f in fdt]
	model = fdt[:fdt.index("namespace")]
	raw_id_map = fdt[fdt.index("namespace")+1:]

	mdl_tree = {}
	last_mdl = None
	for m in model:
		if m[0:4] != "    ":
			mdl_tree[int(m)] = {}
			last_mdl = int(m)
		else:
			dat = m[4:]
			fld_id = dat[:dat.index(" ")]
			typ = dat[dat.index(" ")+1:dat.index(" ")+1+2]

			if typ == "==":
				val = dat[dat.index("==")+3:]  # get the value from the constant
				mdl_tree[last_mdl][int(fld_id)] = ["CNST", val]
			elif typ == "<<":
				fld_typ = dat[dat.index("<<")+3:dat.index("[")]  # field type
				connect = dat[dat.index("[")+1:-1].split(",")  # connections from the other field
				if connect == [""]:
					connect = []
				else:
					connect = [int(i) for i in connect]
				mdl_tree[last_mdl][int(fld_id)] = ["INP", fld_typ, connect, Null]
			elif typ == ">>":
				fld_typ = dat[dat.index(">>")+3:dat.index("[")]  # field type
				connect = dat[dat.index("[")+1:-1].split(",")  # connections from the other field
				if connect == [""]:
					connect = []
				else:
					connect = [int(i) for i in connect]
				mdl_tree[last_mdl][int(fld_id)] = ["OUT", fld_typ, connect, Null]

	id_map = {int(ln[4:ln.index(" ", 4)]): ln[ln.index(" ", 4)+1:] for ln in raw_id_map}

	return mdl_tree, id_map


class ProjectFI:
	""" Project File Interface
	"""

	dir_deploy = "deploy/"
	dir_validator = "validator/"
	dir_test = "test/"
	dir_train = "train/"
	dir_model = "model/"
	mdl_exec = ".exec.dat"
	mdl_proj = ".proj.dat"
	mdl_grph = ".grph.dat"

	prj_file = "project.yaml"

	def __init__(self, *, name: str, path: str):  # name: valid directory name
		if os.path.exists(path):
			self.path = os.path.join(path, name)
		else:
			print("Error: path name <", path, "> is not a valid pathname or non-existing directory")
			raise

		self.setup(name)

	def setup(self, name: str):
		""" sets-up the project directory
		"""
		existed = False

		if os.path.exists(self.path): existed = True
		else: os.mkdir(self.path)  # making root directory

		if os.path.exists(os.path.join(self.path, self.prj_file)):
			existed = True
			self.project = {}
			print("Warning: PROJECT FILE WAS ALREADY CREATED")
		else:
			# create project yaml file
			self.project = {
				"author": None,
				"created": None,
				"updated": None,
				"name": name,
				"model": {
					"index": 0,
					"tag": {},  # model name: {id_name:model_name}
				},
			}
			with open(os.path.join(self.path, self.prj_file), "w") as fbj:
				yaml.dump(self.project, fbj)

		for dir in [self.dir_deploy, self.dir_validator, self.dir_test, self.dir_train, self.dir_model]:
			if not os.path.exists(os.path.join(self.path, dir)): os.mkdir(os.path.join(self.path, dir))
			else: existed = True

		if existed: print("Some or all of the files/directories exists in the source path")

	def save(self):
		""" Loads project data to the memory except model files and related.
		"""
		with open(os.path.join(self.path, self.prj_file), "w") as fbj:
			yaml.dump(self.project, fbj)

	@staticmethod
	def load(dir: str) -> Optional[ProjectFI]:
		""" Loads project data to the memory except model files and related.
		"""
		if os.path.split(dir)[1] != ProjectFI.prj_file:
			print(f"Error: the directories '{dir}' project file was invalid!")
			return None

		if os.path.exists(dir):
			path, name = os.path.split(os.path.split(dir)[0])
			inst = ProjectFI(name=name,path=path)
			inst.loadfiles()

			return inst
		else:
			print(f"Error: the directory '{dir}' does not exist!")
			return None

	def loadfiles(self):
		self.project = {}

		with open(os.path.join(self.path, self.prj_file), "r") as fbj:
			dat = yaml.safe_load(fbj)
			if type(dat) is dict:
				self.project = dat
			else:
				print("Invalid project.yaml")

	def get_key(self, name: str) -> Optional[int]:
		if name not in self.project["model"]["tag"].values():
			_id = self.project["model"]["index"]
			self.project["model"]["tag"][_id] = name
			self.project["model"]["index"] += 1
			return _id
		print(f"Error: The model name <{name}> has already been defined")
		return None

	def valid_key(self, key: int) -> bool:
		if key in self.project["model"]["tag"].keys(): return True
		return False

	def change_name(self, key: int, name: str):
		if self.valid_key(key):
			print(f"Info: Name changed from <{self.project['model']['tag'][key]}> to <{name}>")
			self.project["model"]["tag"][key] = name
		else:
			print("Error: Invalid key")

	def save_mdl_exec(self, key: int, items: List[Union[Node, Connector, Connection]]):
		if self.valid_key(key):
			fdt = model_saver(items)
			with open(os.path.join(self.path, "MDL"+str(key)+self.mdl_exec), "w") as fbj:
				fbj.writelines([ln+"\n" for ln in fdt])
		else:
			print("Error: Invalid key")

	def read_mdl_exec(self, key: int) -> (dict, dict):
		if self.valid_key(key):
			fdt = []
			with open(os.path.join(self.path, "MDL"+str(key)+self.mdl_exec), "r") as fbj:
				fdt = fbj.readlines()
			return dat_file_loader(fdt)
		else:
			print("Error: Invalid key")

	def save_mdl_proj(self, key: int, items: List[Union[Node, Connector, Connection]]):
		if self.valid_key(key):
			fdt = {}
			for itm in items:
				if isinstance(itm, Node):
					print({c[0]:c[1] for c in itm.central.nd_cls.field["constant"]})
					fdt[items.index(itm)] = {
						"pos": itm.central.pos,
						"nd_cls": itm.central.nd_cls.__class__.__name__,
						"connector": [items.index(c) for c in itm.central.connector],
						"constants": {c[0]:c[1].save() for c in itm.central.nd_cls.field["constant"]},
					}
				elif isinstance(itm, Connector):
					fdt[items.index(itm)] = {
						"tag": itm.tag,
						"en": itm.en,
						"field": itm.field,
						"connections": [items.index(c) for c in itm.connections],
					}
				elif isinstance(itm, Connection):   # the connector auto adds "selector connection" adding redundancy
					if itm.connector_b is not None: fdt[items.index(itm)] = {
						"connector_a": items.index(itm.connector_a),
						"connector_b": items.index(itm.connector_b),
					}
			with open(os.path.join(self.path, "MDL"+str(key)+self.mdl_proj), "w") as fbj:
				yaml.safe_dump(fdt, fbj)
		else:
			print("Error: Invalid key")

	def read_mdl_proj(self, key: int) -> QGraphicsView:
		if self.valid_key(key):
			# iterate through the list and then find any graphical parts
			# that contains the current index of the current graphical parts
			# THAN instantiate the graphical parts
			# ALSO instantiate with the missing index which later will be replaced with

			fdt = {}
			with open(os.path.join(self.path, "MDL"+str(key)+self.mdl_proj), "r") as fbj:
				fdt = yaml.safe_load(fbj)

			scene = QGraphicsScene(0, 0, 1920, 1080)
			view = QGraphicsView(scene)

			# used in the eval()
			from src.components.workspace import nodes

			for i in fdt:  # TODO: A Cleaner way to deserialize constant fields
				if fdt[i].get("connector") is not None:  # Node
					o: Node = eval(f"nodes.{fdt[i]['nd_cls']}").create(view, fdt[i]['pos'])
					consts = []

					for ind, const in enumerate(o.central.nd_cls.field["constant"]):
						consts.append((const[0], const[1].load(fdt[i]["constants"][const[0]])))
					del o

					node: Node = eval(f"nodes.{fdt[i]['nd_cls']}").create(view, fdt[i]['pos'], const=consts)
					# also updates the connector, so this must be place after the update
					for ind, c in enumerate(node.central.connector):
						c.TEMP_ind = fdt[i]["connector"][ind]
					view.scene().addItem(node)

			for i in fdt:
				if fdt[i].get("connector_a") is not None:  # Connection
					item = view.items()
					cnc_a = None
					cnc_b = None
					if fdt[i]["connector_a"] != None:
						for ca in item:
							if isinstance(ca, Connector):
								if fdt[i]["connector_a"] == ca.TEMP_ind:
									cnc_a = ca
					if fdt[i]["connector_b"] != None:
						for cb in item:
							if isinstance(cb, Connector):
								if fdt[i]["connector_b"] == cb.TEMP_ind:
									cnc_b = cb
					if cnc_b is not None:  # connector connections
						S = cnc_a.mapToItem(cnc_a, cnc_a.spos)
						O = cnc_b.mapToItem(cnc_a, cnc_b.spos)
						view.scene().addItem(Connection(S, O, parent=cnc_a,external=cnc_b, color=Qt.green))
			for c in view.items():  # using the list `view` for the generated connectors from the Node class
				if isinstance(c, Connector):  # Connector
					del c.TEMP_ind
					for i in view.items():
						if isinstance(i, Connection):
							if i.connector_a == c and i.connector_b is not None:  # filter out selection connection
								print("PAIR", i, c, i.connector_a)
								c.connections.append(i)
			for node in view.items():
				if isinstance(node, Node):
					node.central.view = view  # updating the view attribute

			return view
		else:
			print("Error: Invalid key")

	def delete_mdl(self, key: int):
		if self.valid_key(key):  # deleting a file can be dangerous at times; only can remove the reference but to delete the actual file, users must delete it manually
			del self.project["model"]["tag"][key]
		else:
			print("Error: Invalid key")


	# ==== EXPERIMENTAL ====

	def save_mdl_grph(self, name: str): pass

	def read_mdl_grph(self, mid: int): pass


if __name__ == '__main__':
	# iterate through the list and then find any graphical parts
	# that contains the current index of the current graphical parts
	# THAN instantiate the graphical parts
	# ALSO instantiate with the missing index which later will be replaced with

	pass
