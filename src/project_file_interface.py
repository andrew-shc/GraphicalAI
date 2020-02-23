"""
Project File Interface v1.0
	To interface the directory to the abstract file directory within the software. Loads models, training datasets, etc.
---------------------------

project root directory
	project.yaml
	MODEL_0.dat (Model Data)
	training data
		misc.files
		group1
			...
		group2
			...
	testing data
		...

"""

import yaml
import os

from src.debug import *
from src.gfx.connector import Connector
from src.constants import *


class ProjectFI:
	""" Project File Interface
	"""
	MODEL_EXT = ".dat"

	def __init__(self, path: str, project_file="project.yaml", model_dir="", training_dir="training/",
	             testing_dir="testing/"):
		# loads the models and files references/names/directories from the project directory to the interface

		self.path = path  # absolute project path location

		self.project_file = project_file  # project file directory (project.yaml)
		self.model_dir = model_dir  # model directory (*.dat); usually in the main directory
		self.training_dir = training_dir  # training directory
		self.testing_dir = testing_dir  # testing directory

		self.MODELS = {}  # a buffer of all the model files in the project
		self.project_dat = {}

	def create_project(self):
		""" Creates a new project data and saves it """
		FILE_CREATED_ERROR = False

		self.project_dat = {
			"author": None,
			"date": None,
			"model": {
				"index": 0,
				"tag": {},
			}
		}

		if not os.path.isfile(self.path+self.project_file):  # creating a new project file
			with open(self.path+self.project_file, "w") as fbj:
				yaml.dump(self.project_dat, fbj, default_flow_style=False)
		else:
			print(f"{self.path+self.project_file} for project file is already existed!", l=ERR)
			FILE_CREATED_ERROR = True

		if not os.path.exists(self.path+self.training_dir):  # creating a new training files directory
			os.makedirs(self.path+self.training_dir)
		else:
			print(f"{self.path+self.training_dir} for training directory is already existed!", l=ERR)
			FILE_CREATED_ERROR = True

		if not os.path.exists(self.path+self.testing_dir):  # creating a new testings files directory
			os.makedirs(self.path+self.testing_dir)
		else:
			print(f"{self.path+self.testing_dir} for testing directory is already existed!", l=ERR)
			FILE_CREATED_ERROR = True
		return FILE_CREATED_ERROR

	def load_project(self):
		""" Loads the models and files data to the interface for quick access and buffering """
		with open(self.path+self.project_file, "r") as fbj:
			self.project_dat = yaml.safe_load(fbj)

		for f in os.listdir(self.path+self.model_dir):
			if os.path.splitext(f)[1] == self.MODEL_EXT:
				with open(self.path+self.model_dir+f, "r") as fbj:
					self.MODELS[os.path.splitext(f)[0]] = fbj.readlines()

	def save_project(self):
		""" saves all data to the files """
		with open(self.path+self.project_file, "w") as fbj:
			yaml.dump(self.project_dat, fbj, default_flow_style=False)

		for mdl in self.MODELS:
			with open(self.path+self.model_dir+mdl+self.MODEL_EXT, "w") as fbj:
				fbj.writelines(self.MODELS[mdl])
		print("[INFO]: Project Saved")

	def read_models(self, tag: str):
		""" reads the models from the buffer """
		mdl_k = {self.project_dat["model"]["tag"][k]: k for k in self.project_dat["model"]["tag"]}
		return self.MODELS[mdl_k[tag]], self.project_dat["model"]["tag"][mdl_k[tag]]

	def write_model(self, tag: str, fdt: list):
		""" writes the AI model to the buffer or creates a new model """
		print(self.project_dat)
		mdl_k = {self.project_dat["model"]["tag"][k]:k for k in self.project_dat["model"]["tag"]}
		if tag not in mdl_k.keys():
			print(f"[INFO]: Automatically added the model <{tag}>.")
			self.MODELS["MODEL_"+str(self.project_dat["model"]["index"])] = fdt
			self.project_dat["model"]["tag"]["MODEL_"+str(self.project_dat["model"]["index"])] = tag
			self.project_dat["model"]["index"] += 1
		else:
			self.MODELS[mdl_k[tag]] = fdt
			if tag != "": self.project_dat["model"]["tag"][mdl_k[tag]] = tag

	def model_saver(self, model_dt: list, items: list, name: str):
		"""
			Saves the model data to a file.
		items: a list of items in a graphics view
		"""
		dat = {}

		dt_obj = [i for i in items if isinstance(i, Connector)]
		for m in model_dt:
			dt_obj.append(m)
			for fld in m.field["constant"]:
				dt_obj.append(fld[1])

		obj_id = 0
		obj_map = {}
		for i in dt_obj:
			obj_map[i] = obj_id
			obj_id += 1

		model_id = 0
		model = {}
		for m in model_dt:
			model[m] = model_id
			model_id += 1

		id_map = {}  # ID # mapping to name
		for m in model_dt:
			dat[obj_map[m]] = {}
			for i in items:
				if isinstance(i, Connector):  # connectors
					if i.parent == m:
						id_map[obj_map[m]] = m.nmspc_id
						id_map[obj_map[i]] = i.field[0]
						dat[obj_map[m]][obj_map[i]] = (i.tag, i.field[1], [obj_map[c] for c in i.connectees])
			for c in m.field["constant"]:  # constants
				id_map[obj_map[m]] = m.nmspc_id
				id_map[obj_map[c[1]]] = c[0]
				dat[obj_map[m]][obj_map[c[1]]] = ("const", c[1].value())
		self._dat_file_saver(dat, id_map, name)

		return dat

	def _dat_file_saver(self, model_tree, id_map, name: str):
		"""
		model_tree:
			model title:
				connector id: (type, [connector id connections, ...]),

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
					ln.append(tab+str(f)+" << "+fld[1]+"["+",".join([str(i) for i in fld[2]])+"]")
				elif fld[0] == TG_OUTPUT:
					ln.append(tab+str(f)+" >> "+fld[1]+"["+",".join([str(i) for i in fld[2]])+"]")
				elif fld[0] == "const":
					ln.append(tab+str(f)+" == "+str(fld[1]))

		ln.append("namespace")
		for o in id_map:  # each objects mapped to id
			ln.append(tab+str(o)+" "+str(id_map[o]))

		self.write_model(name, [l+"\n" for l in ln])
		self.save_project()

	def dat_file_loader(self, fname):
		fdt = []
		with open(self.path+fname, "r") as fbj:
			fdt = fbj.readlines()
			fdt = [l.strip("\n") for l in fdt]

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


if __name__ == '__main__':
	f = ProjectFI("C:/Users/Andrew Shen/Desktop/ProjectEmerald/FileInterfaceTest/")
	f.create_project()
	f.write_model("MyModel1", [b"model data"])
	f.write_model("MyModel2", [b"damn it"])
	f.write_model("TrainingModel1", [b"another data"])
	f.write_model("TrainingModel2", [b"another model object data"])
	f.write_model("MyModel1", [b"model 1 changed from model data -> none"])
	# f.load_project()
	print(f.MODELS)
	print(f.project_dat)
	print(f.read_models("TrainingModel2"))
	print(f.read_models("MyModel2"))
	print(f.save_project())


"""
		cnc = [i for i in items if isinstance(i, Connector)]

		oid = 0
		oid_map = {}  # object id map
		dat_tree = {}

		for m in model_dt:
			mid = oid
			oid += 1
			oid_map[mid] = m.nmspc_id
			dat_tree[mid] = {}

			for c in cnc:
				if c.parent == m:  # under the same parent
					fid = oid
					oid += 1
					oid_map[fid] = c.field[0]
					dat_tree[mid][fid] = (c.tag, c.field[1], c.connectees)
			for const in m.field["constant"]:
				fid = oid
				oid += 1
				oid_map[fid] = const[0]
				dat_tree[mid][fid] = ("const", const[1].value())

		print("@@@", oid_map)
		print("@@@", dat_tree)
"""