###############################################
# All Python file, whom part of this project, must import this file
###############################################

def print(*args,**kwargs):
	__import__('builtins').print(f"{__import__('os').path.relpath(__import__('inspect').stack()[1].filename,__import__('os').path.dirname(__import__('os').path.abspath(__file__)))}:{__import__('inspect').stack()[1].lineno}:{__import__('inspect').stack()[1].function}", " ### ",*args,**kwargs)
