#!/usr/bin/env python

from distutils.core import setup
import os
import re


lib = os.path.dirname(os.path.realpath("./prettyparser"))
reqpath = os.path.join(lib, 'requirements.txt')
install_requires = [] 
if os.path.isfile(reqpath):
    with open(reqpath) as f:
        install_requires = f.read().splitlines()

long_desc_path = os.path.join(lib, 'README.md')

try:
    import pypandoc
    if os.path.isfile(long_desc_path):
        long_description = pypandoc.convert_file(long_desc_path, 'rst')
        long_description = re.sub("icon", "", long_description)
    else:
        long_description = ''
except:
    pass



setup(name='prettyparser',
      version='1.0.4',
      description='Library for Parsing PDF/TXT and Python Objects with Text Using Regular Expressions',
      author='Leandro Roser',
      author_email='learoser@gmail.com',
      url='https://github.com/leandroroser/prettyparser',
      install_requires=install_requires,
      license='ASL',
      python_requires='>=3.6',
      long_description=long_description,
      long_description_content_type='text/x-rst'
     )