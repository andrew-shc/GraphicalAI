from setuptools import setup
from Cython.Build import cythonize

setup(
    name="Application",
    ext_modules=cythonize(["main.py","libs.pyx"]),
    zip_safe=False,
)
