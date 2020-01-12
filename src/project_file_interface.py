"""
Project File Interface v1.0
	To interface the directory to the abstract file directory within the software. Loads models, training datasets, etc.
---------------------------

project root directory
	project.yaml
	skeleton.dat (a pure data from project)
	0AI.dat (AI model)
	0ML.dat (ML model)
	0PM.dat (Parameterized/Trained/Tested Model)
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

		self.MODELS = {}  # a buffer of all the AI (Artificial Intelligence) and ML (Machine Learning) model files in the project
		self.project_dat = {}

	def create_project(self):
		""" Creates a new project data and saves it """
		FILE_CREATED_ERROR = False

		self.project_dat = {
			"author": None,
			"date": None,
			"model": {
				"ai_index": 0,
				"ml_index": 0,
				"tag": {},
			}
		}

		if not os.path.isfile(self.path+self.project_file):  # creating a new project file
			with open(self.path+self.project_file, "w") as fbj:
				yaml.dump(self.project_dat, fbj, default_flow_style=False)
		else:
			print(f"[ERROR]: {self.path+self.project_file} for project file is already existed!")
			FILE_CREATED_ERROR = True

		if not os.path.exists(self.path+self.training_dir):  # creating a new training files directory
			os.makedirs(self.path+self.training_dir)
		else:
			print(f"[ERROR]: {self.path+self.training_dir} for training directory is already existed!")
			FILE_CREATED_ERROR = True

		if not os.path.exists(self.path+self.testing_dir):  # creating a new testings files directory
			os.makedirs(self.path+self.testing_dir)
		else:
			print(f"[ERROR]: {self.path+self.testing_dir} for testing directory is already existed!")
			FILE_CREATED_ERROR = True
		return FILE_CREATED_ERROR

	def load_project(self):
		""" Loads the models and files data to the interface for quick access and buffering """
		with open(self.path+self.project_file, "r") as fbj:
			self.project_dat = yaml.safe_load(fbj)

		for f in os.listdir(self.path+self.model_dir):
			if os.path.splitext(f)[1] == self.MODEL_EXT:
				with open(self.path+self.model_dir+f, "rb") as fbj:
					self.MODELS[os.path.splitext(f)[0]] = fbj.readlines()

	def save_project(self):
		""" saves all data to the files """
		with open(self.path+self.project_file, "w") as fbj:
			yaml.dump(self.project_dat, fbj, default_flow_style=False)

		for mdl in self.MODELS:
			with open(self.path+self.model_dir+mdl+self.MODEL_EXT, "wb") as fbj:
				fbj.writelines(self.MODELS[mdl])
		print("[INFO]: Project Saved")

	def read_models(self, tag: str):
		""" reads the models from the buffer """
		mdl_k = {self.project_dat["model"]["tag"][k]: k for k in self.project_dat["model"]["tag"]}
		return self.MODELS[mdl_k[tag]], self.project_dat["model"]["tag"][mdl_k[tag]]

	def write_ai_model(self, tag: str, fdt: list):
		""" writes the AI model to the buffer or creates a new model """
		print(self.project_dat)
		mdl_k = {self.project_dat["model"]["tag"][k]:k for k in self.project_dat["model"]["tag"]}
		if tag not in mdl_k.keys():
			print(f"[INFO]: Automatically added AI model <{tag}>.")
			self.MODELS[str(self.project_dat["model"]["ai_index"])+"AI"] = fdt
			self.project_dat["model"]["tag"][str(self.project_dat["model"]["ai_index"])+"AI"] = tag
			self.project_dat["model"]["ai_index"] += 1
		else:
			self.MODELS[mdl_k[tag]] = fdt
			if tag != "": self.project_dat["model"]["tag"][mdl_k[tag]] = tag

	def write_ml_model(self, tag: str, fdt: list):
		""" writes the ML model to the buffer or creates a new model """
		mdl_k = {self.project_dat["model"]["tag"][k]: k for k in self.project_dat["model"]["tag"]}
		if tag not in mdl_k.keys():
			print(f"[INFO]: Automatically added ML model <{tag}>.")
			self.MODELS[str(self.project_dat["model"]["ml_index"])+"ML"] = fdt
			self.project_dat["model"]["tag"][str(self.project_dat["model"]["ml_index"])+"ML"] = tag
			self.project_dat["model"]["ml_index"] += 1
		else:
			self.MODELS[mdl_k[tag]] = fdt
			if tag != "": self.project_dat["model"]["tag"][mdl_k[tag]] = tag


if __name__ == '__main__':
	f = ProjectFI("C:/Users/Andrew Shen/Desktop/ProjectEmerald/FileInterfaceTest/")
	f.create_project()
	f.write_ai_model("MyModel1", [b"model data"])
	f.write_ai_model("MyModel2", [b"damn it"])
	f.write_ml_model("TrainingModel1", [b"another data"])
	f.write_ml_model("TrainingModel2", [b"another model object data"])
	f.write_ai_model("MyModel1", [b"model 1 changed from model data -> none"])
	# f.load_project()
	print(f.MODELS)
	print(f.project_dat)
	print(f.read_models("TrainingModel2"))
	print(f.read_models("MyModel2"))
	print(f.save_project())
