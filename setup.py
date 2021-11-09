#!/usr/bin/env python

from distutils.core import setup
import os

lib = os.path.dirname(os.path.realpath("."))
reqpath = lib + '/requirements.txt'
install_requires = [] 
if os.path.isfile(reqpath):
    with open(reqpath) as f:
        install_requires = f.read().splitlines()

setup(name='prettyparser',
      version='1.0',
      description='Library for Parsing PDF/TXT and Python Objects with Text Using Regular Expressions',
      author='Leandro Roser',
      author_email='learoser@gmail.com',
      url='https://www.python.org/sigs/distutils-sig/',
      install_requires=install_requires,
      python_requires='>=3.6'
     )