# -*- coding: utf-8 -*-
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

import LibRadar


def read(f_name):
    return open(os.path.join(os.path.dirname(__file__), f_name)).read()

setup(
    name=LibRadar.__title__,
    version=LibRadar.__version__,
    author=LibRadar.__author__,
    author_email=LibRadar.__email__,
    description=LibRadar.__summary__,
    license=LibRadar.__license__,
    keywords="Android Third-party Library",
    url=LibRadar.__uri__,
    packages=['LibRadar'],
    long_description=read('docs/PyPI_Index.rst'),
    requires=['redis'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License"
    ],
)
