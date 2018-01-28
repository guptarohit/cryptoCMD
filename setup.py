#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from codecs import open
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

NAME = 'cryptocmd'
VERSION = '0.1.2'

with open('requirements.txt') as f:
    required = f.readlines()

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()

setup(
    name=NAME,
    version=VERSION,
    description='Cryptocurrency historical market price data scrapper.',
    long_description=long_description,
    packages=[NAME],
    url='https://github.com/guptarohit/cryptocmd',
    author='Rohit Gupta',
    author_email='rohitg.tech@gmail.com',
    install_requires=required,
    include_package_data=True,
    extras_require={
        'pandas': ['pandas'],
    },
    license='BSD',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: BSD License",
    ],
)
