###############################################
# All Python file, whom part of this project, must import this file
###############################################
INF, WRN, ERR = 0xF001, 0xF002, 0xF003
# def print(*args,l=WRN):
# 	with open("debug.log","a")as fbj:__import__('builtins').print(__import__("datetime").datetime.now(),f"{__import__('os').path.relpath(__import__('inspect').stack()[1].filename,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))}:{__import__('inspect').stack()[1].lineno}:{__import__('inspect').stack()[1].function}",f"\r\t\t{({WRN:'[WARN ]',INF:'[INFO ]',ERR:'[ERROR]'}[l])}",*args,file=fbj,end="\r")

def print(*args,l=WRN):
	__import__('builtins').print(*args)