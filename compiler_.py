"""
Windows Compiler
"""

import os
import subprocess
import shutil

ROOT = "C:\\Users\\Andrew Shen\\Desktop\\GraphicalAI-II"
SRC = ROOT+"\\graphical_ai"
BIN = ROOT+"\\pyd_bin"
SRC_PYD_EXT = ".cp37-win_amd64.pyd"

INPLACE = ["pymain.py", "proj_ref.yaml"]
MODL = ["main"]

# === start of the actual execution of the compilation process ===

PYX_MODL = ["\\"+i for i in MODL]

items = [os.path.join(BIN, i) for i in os.listdir(BIN)]
while len(items) > 0:
	item = items[0]
	del items[0]

	if os.path.isdir(item):
		items += [os.path.join(item, i) for i in os.listdir(item)]
	elif os.path.basename(item) not in INPLACE:
		try:
			os.remove(item)
			print("removed: ", item)
		except PermissionError:
			print("tried removed: ", item)


items = [os.path.join(SRC, i) for i in os.listdir(SRC)]
while len(items) > 0:
	item = items[0]
	itemr = os.path.relpath(item, SRC)
	del items[0]

	if os.path.basename(item) != "__pycache__":
		if os.path.isdir(item):
			items += [os.path.join(item, i) for i in os.listdir(item)]
		elif os.path.basename(item).split(".")[-1] == "py":  # pyx and pxd will be auto-compiled to pyd
			print("copying:", SRC+"\\"+itemr, "to", BIN+"\\"+itemr)
			try:
				# shutil.copyfile(SRC+"\\"+itemr, BIN+"\\"+itemr)
				with open(SRC+"\\"+itemr, "r") as fbo:
					fdt = fbo.readlines()
				with open(BIN+"\\"+itemr, "w") as fbo:
					fdt.insert(0, "from __base__ import *\n")
					fbo.writelines(fdt)

			except FileNotFoundError as e:
				print(e)
				print(itemr, os.path.dirname(itemr), BIN+"\\"+os.path.dirname(itemr))
				os.mkdir(BIN+"\\"+os.path.dirname(itemr))
				shutil.copyfile(SRC+"\\"+itemr, BIN+"\\"+itemr)
				# raise e
		elif os.path.basename(item).split(".")[-1] == "pyx":
			print(os.path.basename(item))
			# subprocess.run(["cythonize", "-3", SRC+modl+".pyx", "-i"], shell=True, capture_output=True, check=True)
			# os.rename(SRC+modl+".c", BIN+modl+".c")
			# os.rename(SRC+modl+SRC_PYD_EXT, BIN+modl+SRC_PYD_EXT)
			# print("compiled", modl)

try:
	# compiling all the dependent modules into *.pyd
	for modl in PYX_MODL:
		subprocess.run(["cythonize", "-3", SRC+modl+".pyx", "-i"], shell=True, capture_output=True, check=True)
		os.rename(SRC+modl+".c", BIN+modl+".c")
		os.rename(SRC+modl+SRC_PYD_EXT, BIN+modl+SRC_PYD_EXT)
		print("compiled", modl)

except subprocess.CalledProcessError as e:
	print("error - compiling:", e.stderr.decode("ASCII"))
