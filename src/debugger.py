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
    # TODO(techtonik): consider using __main__
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


print("\033[0;37;40m Normal       Text")
print("\033[2;37;40m Underlined   Text\033[0;37;40m")
print("\033[1;37;40m Bright       Colour\033[0;37;40m")
print("\033[3;37;40m Negative     Colour Background\033[0;37;40m")
print("\033[5;37;40m Negative     Colour Foreground\033[0;37;40m")

print(
    "\033[1;37;40m \033[2;37:40m TextColour (Bright)          TextColour                BackgroundColour \033[0;37;40m\n")
print(
    "\033[1;30;47m Dark Gray                    \033[0;30;47m Black                   \033[0;31;40m Background                       \033[0m")
print(
    "\033[1;31;40m Bright Red                   \033[0;31;40m Red                     \033[0;32;41m Background                       \033[0m")
print(
    "\033[1;32;40m Bright Green                 \033[0;32;40m Green                   \033[0;33;42m Background                       \033[0m")
print(
    "\033[1;33;40m Yellow                       \033[0;33;40m Brown                   \033[0;34;43m Background                       \033[0m")
print(
    "\033[1;34;40m Bright Blue                  \033[0;34;40m Blue                    \033[0;35;44m Background                       \033[0m")
print(
    "\033[1;35;40m Bright Magenta               \033[0;35;40m Magenta                 \033[0;36;45m Background                       \033[0m")
print(
    "\033[1;36;40m Bright Cyan                  \033[0;36;40m Cyan                    \033[0;37;46m Background                       \033[0m")
print(
    "\033[1;37;40m White                        \033[0;37;40m Light Grey              \033[0;30;47m Background                       \033[0m")

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

info("Information")
error("Error")
warning("Warning")
print("Debug")
normal("Normal")
normal("\n===\n")

normal("DEBUG TEST")

A()
B()

info("Finished Color Testing and Pre-Initializing")


