import sys
from cx_Freeze import setup, Executable


# 1: add __init__.py to imported packages (when runtime error shown as ModuleNotFoundError/compiling shows ImportError)
# 2: add the missing module to the packages
# 3: recaptilize the filename (e.g. Pool.py -> pool.py)
# 4: Exclude the file (may be name collision)

source_dir = "src/"

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

options = {
    'build_exe': {
        'path': sys.path + [
            '',
            source_dir,
            source_dir+'components',
            source_dir+'components/workspace',
            source_dir+'gfx',
            source_dir+'interface'
        ],
        'includes': [
            'atexit',
            # 'scipy._lib'
            # 'scipy'
        ],
        'packages': [
            'scipy',
            'tensorflow',
            'termcolor',
            # 'tensorflow_core',
            'google',
        ],
        'excludes': {
            'pytest',
            'tkinter',
            'scipy.spatial.cKDTree'
        }
    },
}

executables = [
    Executable('src/main.py', base=base)
]

setup(  name="Hexacone",
        version="0.0.0",
        description="AI GUI Application",
        options=options,
        executables=executables
        )
