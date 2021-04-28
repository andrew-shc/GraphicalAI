"""
Windows Compiler
"""

import os
import subprocess

PYTHON_DIR= "C:\\Users\\Andrew Shen\\AppData\\Local\\Programs\\Python\\Python37"
ROOT = "C:\\Users\\Andrew Shen\\Desktop\\GraphicalAI-II"
SRC = ROOT+"\\graphical_ai"
BIN = ROOT+"\\bin"
SRC_PYD_EXT = ".cp37-win_amd64.pyd"

MAIN = "main"
MAIN_EXEC = "main.exe"
MODL = ["libs"]

# === start of the actual execution of the compilation process ===

PYX_MAIN = "\\"+MAIN
PYX_MODL = ["\\"+i for i in MODL]
PYX_MODL.append(PYX_MAIN)

items = [os.path.join(BIN, i) for i in os.listdir(BIN)]
while len(items) > 0:
	item = items[0]
	del items[0]

	if item.endswith(SRC_PYD_EXT) or item.endswith(".c"):
		fname = os.path.basename(item).split(".")[0]
		if "\\"+fname in PYX_MODL or "\\"+fname == PYX_MAIN:
			os.remove(item)
	elif os.path.isdir(item):
		items += [os.path.join(item, i) for i in os.listdir(item)]

try:
	# compiling all the dependent modules into *.pyd
	for modl in PYX_MODL:
		subprocess.run(["cythonize", "-3", SRC+modl+".pyx", "-i"], shell=True, capture_output=True, check=True)
		os.rename(SRC+modl+".c", BIN+modl+".c")
		os.rename(SRC+modl+SRC_PYD_EXT, BIN+modl+SRC_PYD_EXT)
	print("[COMPILATION]", "# Internal module dependencies finished compiling")

	# compiling the main *.pyx file into an embedded executable to be runned alongside with the loaded pyd files
	subprocess.run(["cython", "-3", "-I "+SRC, SRC+PYX_MAIN+".pyx", "-o", BIN+PYX_MAIN+".c", "--embed"], shell=True, capture_output=True, check=True)
	print("[COMPILATION]", "Finished compiling Python main to .c: ", BIN+PYX_MAIN+".c")
	subprocess.run(["gcc", BIN+PYX_MAIN+".c", "-Os", "-DSIZEOF_VOID_P=8", "-DMS_WIN64", "-I", PYTHON_DIR+r"\include", "-o", BIN+PYX_MAIN+".exe", "-lpython37", "-lm", "-L", PYTHON_DIR+r"\libs", "-municode"], shell=True, capture_output=True, check=True)
	print("[COMPILATION]", "Finished compiling main .c file to binaries: ", BIN+PYX_MAIN+".exe")

	with open(BIN+"\\pymain.py", "w") as fbo:
		fbo.writelines(["import main"])
	print("[COMPILATION]", "Finished generating pymain.py file: ", BIN+PYX_MAIN+".exe")

	os.chdir(BIN)
	res = subprocess.run([BIN+PYX_MAIN+".exe"], shell=True, capture_output=True, check=True)
	print("[COMPILATION]", "EXIT CODE:", res.stdout.decode("ASCII"))
	print("[COMPILATION]", "ERROR:", "\n"+res.stderr.decode("ASCII"))
except subprocess.CalledProcessError as e:
	print("[COMPILATION]", "ERROR:", e.stderr.decode("ASCII"))
