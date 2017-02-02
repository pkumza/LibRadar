import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="LibRadar",
    version="2.0.2.dev1",
    author="Zachary Marv",
    author_email="maziang@pku.edu.cn",
    description="LibRadar is an automatic tool for Android library detection.",
    license="BSD",
    keywords="Android Third-party Library",
    url="http://radar.pkuos.org/",
    packages=['LibRadar'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 2.7",
        "Topic :: Security",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
