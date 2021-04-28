from os import path
import builtins
import inspect


def print(*args, **kwargs):
    # builtins.print(__file__, path.abspath(__file__), inspect.stack()[1].filename)
    builtins.print(
        f"{path.relpath(inspect.stack()[1].filename, path.dirname(path.abspath(__file__)))}:{inspect.stack()[1].lineno-1}:{inspect.stack()[1].function}",
        " ¶ ", *args, **kwargs)
