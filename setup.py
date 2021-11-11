#!/usr/bin/env python

from setuptools import setup
import os
import re

lib = os.path.dirname(os.path.realpath(__file__))
reqpath = os.path.join(lib, 'requirements.txt')

install_requires = [] 
with open(reqpath) as f:
    install_requires = f.read().splitlines()

description = 'Library for Parsing PDF/TXT and Python Objects with Text Using Regular Expressions'

with open(os.path.join(lib, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='prettyparser',
      version='1.0.15',
      description= description,
      author='Leandro Roser',
      author_email='learoser@gmail.com',
      url='https://github.com/leandroroser/prettyparser',
      install_requires=install_requires,
      license='ASL',
      python_requires='>=3.6',
      long_description=long_description,
      long_description_content_type = 'text/x-rst',
      py_modules=['prettyparser']
     )