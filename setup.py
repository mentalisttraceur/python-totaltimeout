#!/usr/bin/env python

from os import path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from totaltimeout import __doc__, __version__

project_directory = path.abspath(path.dirname(__file__))
readme_path = path.join(project_directory, 'README.rst')

readme_file = open(readme_path)
try:
    long_description = readme_file.read()
finally:
    readme_file.close()

setup(
    name='totaltimeout',
    version=__version__,
    description=__doc__.split('\n')[0],
    long_description=long_description,
    license='0BSD',
    url='https://github.com/mentalisttraceur/python-totaltimeout',
    author='Alexander Kozhevnikov',
    author_email='mentalisttraceur@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ],
    py_modules=['totaltimeout'],
)
