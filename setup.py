from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("system_stats.pyx", language_level=3),
)
