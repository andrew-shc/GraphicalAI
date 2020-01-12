from src.connector import Connector
from src.model import Model
import src.ai_models as aim
import src.ml_models as mlm

from src.project_file_interface import ProjectFI

class Null:
	__slots__ = ()

AI = 0x1000
ML = 0x1001

import builtins


def print(*args):
	builtins.print("[EXECUTOR]: ", *args)


def model_saver(model_dt: list, items: list, prj_root: str, fname: str):
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
				if i.parent.nmspc_id == m.nmspc_id:
					id_map[obj_map[m]] = m.nmspc_id
					id_map[obj_map[i]] = i.field[0]
					dat[obj_map[m]][obj_map[i]] = (i.tag, i.field[1], [obj_map[c] for c in i.connectees])
		for c in m.field["constant"]:  # constants
			id_map[obj_map[m]] = m.nmspc_id
			id_map[obj_map[c[1]]] = c[0]
			dat[obj_map[m]][obj_map[c[1]]] = ("const", c[1].value())
	dat_file_saver(dat, id_map, prj_root, fname)

	return dat


def dat_file_saver(model_tree, id_map, prj_root: str, fname: str):
	"""
	model_tree:
	{
		model title: {
			connector id: (type, [connector id connections, ...]),
			...
		},
		...
	}

	id_map:
		id: display name,
		...
	"""

	ln = []
	tab = "    "

	for m in model_tree:  # each models
		ln.append(str(m))
		for f in model_tree[m]:  # each items (connectors)
			fld = model_tree[m][f]
			if fld[0] == Model.TG_INPUT:
				ln.append(tab+str(f)+" << "+fld[1]+"["+",".join([str(i) for i in fld[2]])+"]")
			elif fld[0] == Model.TG_OUTPUT:
				ln.append(tab+str(f)+" >> "+fld[1]+"["+",".join([str(i) for i in fld[2]])+"]")
			elif fld[0] == "const":
				ln.append(tab+str(f)+" == "+str(fld[1]))

	ln.append("namespace")
	for o in id_map:  # each objects mapped to id
		ln.append(tab+str(o)+" "+str(id_map[o]))

	with open(prj_root+fname, "w") as fbj:
		fbj.writelines([l+"\n" for l in ln])


def dat_file_loader(prj_root, fname):
	fdt = []
	with open(prj_root+fname, "r") as fbj:
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


def modelFieldArgs(model, id_map, const="CNST", out="OUT", inp="INP"):
	"""
		This passes in the keywords arguments into the model executor function
	model: the actual variable values and names
	"""
	dtinp = {}  # input fields attributes
	dtout = {}  # output fields attributes; this will leave all the attribute set to "None" and wait for the model \
	# to change the value to be later returned
	dtconst = {}  # constant fields attributes

	for field in model:
		if model[field][0] == const:
			dtconst[id_map[field]] = model[field][1]
		elif model[field][0] == out:
			dtout[id_map[field]] = Null
		elif model[field][0] == inp:
			if model[field][3] is Null:  # an input field is None; aborts of creating the args
				return False
			else:
				dtinp[id_map[field]] = model[field][3]
	return dtinp, dtconst, dtout


def modelFieldReturn(tree, model, id_map, output, const="CNST", inp="INP", out="OUT"):
	"""
		This saves the output of the internal field to the connected fields known by the internal output
	tree: Model Tree
	model: Selected model
	id_map: An id map for it to transfer from names to values
	output: Output value from the model's executor function
	"""

	# field_map = {id_map[f]:f for f in model}
	print(tree)
	for mdl in tree:
		if tree[mdl] == model:
			for field in tree[mdl]:
				if tree[mdl][field][0] == out:
					for int_mdl in tree:
						for int_field in tree[int_mdl]:
							if int_field in tree[mdl][field][2]:
								print("### RETURN", int_field, field)
								tree[int_mdl][int_field][3] = output[id_map[field]]
	print(">>>", tree)
	# for field in model:
	# 	if model[field][0] == out:
	# 		print("###", model, field, model, output, field, output[id_map[field]])
	# 		tree[model][field][3] = output[id_map[field]]  # saving the value to the internal output field
	# 		for m in tree:
	# 			for f in tree[m]:
	# 				if f in tree[model][field][2]:
	# 					tree[m][f][3] = output[id_map[field]]  # saving the value to the external input field
	return tree


def checkBackflow(tree, selected, id_map, inst, field_map, title_map, typ):
	"""
		This checks any external output fields with a value connecting to any of the internal input field
		and copies the value from the output to the input.
	"""

	for m in tree:
		if m == selected:
			for field in tree[m]:
				if tree[m][field][0] == "INP":
					no_field = True  # are fields connected and not null

					for ext_m in tree:
						for ext_field in tree[ext_m]:
							# print("@@@", ext_field, tree[ext_m][ext_field])
							if tree[ext_m][ext_field][0] == "OUT":
								if ext_field in tree[m][field][2]:

									if tree[ext_m][ext_field][3] != Null:  # the field
										no_field = False
										tree[m][field][3] = tree[ext_m][ext_field][3]  # copy the data from  \
									# the external output -> internal input
					if not no_field:
						print("BACK FLOW - HAS FIELDS")
						args = modelFieldArgs(tree[m], id_map)
						if args != False:
							print("BACK FLOW - MODEL ARGUMENT", args)
							out = eval(f"{'aim' if typ == AI else 'mlm'}.{title_map[id_map[m]]}.execute(args[0], args[1], args[2], inst)")
							tree = modelFieldReturn(tree, tree[m], id_map, out)
						else:
							print("BACK FLOW FAILED - MODEL NOT CONNECTED")
							return tree, False
					else:
						print("BACK FLOW - HAS NO FIELDS")
						return tree, False
	return tree, True


def callFrontflow(tree, selected, id_map, inst, title_map, typ):
	"""
		This calls any model that is connected to the internal output fields when the model itself has value
	model_tree: Model tree
	selected: The selected model to be called on
	"""

	for m in tree:
		if m == selected:
			for field in tree[m]:
				if tree[m][field][0] == "OUT" or tree[m][field][0] == "INP":
					args = modelFieldArgs(tree[m], id_map)
					if args != False:
						print("FRONT FLOW SUCCESS ARGS:", args)
						out = eval(f"{'aim' if typ == AI else 'mlm'}.{title_map[id_map[m]]}.execute(args[0], args[1], args[2], inst)")
						tree = modelFieldReturn(tree, tree[m], id_map, out)
						return tree, True
					else:
						print("FRONT FLOW FAILED")
						tree, success = checkBackflow(tree, selected, id_map, inst, {}, title_map, typ)
						if not success: return tree, False
	return tree, True


def executor(model_tree, id_map, prj, typ):
	"""
	model_tree: NOTE: each fields should be (Field Type, Field Name, Connections, Value=Null())
	"""
	print(model_tree)
	print(id_map)
	print("=====")

	inst = {
		"project": prj,
	}

	mdl = __import__("ai_models" if typ == AI else "ml_models")
	mdl_map = [mdl.__dict__[c] for c in mdl.__dir__()
		                if type(mdl.__dict__[c]) == type
		                if mdl.__dict__[c].__module__ == mdl.__name__
		                ]
	title_map = {o.title:o.__name__ for o in mdl_map}

	active_model = [i for i in model_tree]

	for m in model_tree:  # execute root models (the ones without input)
		onlyOutput = False
		for f in model_tree[m]:
			if model_tree[m][f][0] == "OUT":
				onlyOutput = True
			elif model_tree[m][f][0] == "INP":
				onlyOutput = False; break

		if onlyOutput:
			print("<><><>", m, model_tree)
			model_tree, success = callFrontflow(model_tree, m, id_map, inst, title_map, typ)
			if success: active_model.remove(m)
			print("-+-+-+", model_tree)
		# print(model_tree[m][f][0])
	# print(model_tree[m], onlyOutput)
	print("~~~", active_model)

	loop = True
	while loop:
		print("=EPOCH=", active_model, model_tree)
		for m in active_model:  # execute active models meaning models that haven't gotten an value
			print("><><><", m, model_tree[m])
			model_tree, success = callFrontflow(model_tree, m, id_map, inst, title_map, typ)
			if success: active_model.remove(m)

		if len(active_model) == 0: loop = False
	print("END EXECUTION")

	inst["project"].save_project()


if __name__ == '__main__':
	prj = ProjectFI("../MyTestProj/")
	prj.load_project()
	executor(*dat_file_loader("../MyTestProj/", "ml_skl.dat"), prj, ML)
