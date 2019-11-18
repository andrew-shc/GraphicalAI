import inspect

ERRORS = 0
WARNING = 0
DEBUG = 0


# https://stackoverflow.com/questions/2654113/how-to-get-the-callers-method-name-in-the-called-method
def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method

       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0+skip
    if len(stack) < start+1:
        return ''
    parentframe = stack[start][0]

    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append(codename)  # function or a method

    ## Avoid circular refs and frame leaks
    #  https://docs.python.org/2.7/library/inspect.html#the-interpreter-stack
    del parentframe, stack

    return ".".join(name)

esc = "\033[0m "


def txtcl(frgd, bkgd, style):
    """ text colour """
    color = {
        "none": 0,
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
    }

    sty = {
        "normal": 0,
        "bright": 1,
        "underline": 2,
        "negative-f": 3,
        "negative-b": 5,
    }
    return f"\033[{sty[style]};{color[frgd]};{color[bkgd]+10}m"


import builtins as __builtin__


def info(*kwargs):
    __builtin__.print(esc+txtcl("cyan", "none", "normal"), "[INFO]", *kwargs, esc)


def error(*kwargs):
    global ERRORS
    ERRORS += 1
    __builtin__.print(esc+txtcl("magenta", "blue", "bright"), "[ERROR]", *kwargs, esc)


def warning(*kwargs):
    global WARNING
    WARNING += 1
    __builtin__.print(esc+txtcl("red", "none", "bright"), "[WARNING]", *kwargs, esc)


def print(*kwargs):
    global DEBUG
    DEBUG += 1
    __builtin__.print(esc+txtcl("yellow", "none", "normal"), caller_name(), "[DEBUG]", *kwargs, esc, )


def normal(*kwargs):
    __builtin__.print(*kwargs)


def getter():
    return (DEBUG, WARNING, ERRORS)

def A(): print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
def B(): print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
