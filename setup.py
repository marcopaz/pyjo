#!/usr/bin/env python
from setuptools import setup, find_packages
import re

with open('pyjo/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)
if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='pyjo',
    version=version,
    description='Python JSON Objects',
    url='https://github.com/marcopaz/pyjo',
    download_url='https://github.com/marcopaz/pyjo/archive/{}.tar.gz'.format(version),
    long_description=open('README.md').read(),
    author='Marco Pazzaglia',
    author_email='marco@pazzaglia.me',
    packages=find_packages(),
    package_data={'': ['LICENSE']},
    test_suite="tests",
    install_requires=[
        'six',
        'future',
        'enum34',
    ],
)
