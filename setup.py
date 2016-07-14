# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os.path import join, dirname
version = {}
with open(join(dirname(__file__), "lightmanager", "localclient", "version.py")) as fp:
    exec (fp.read(), version)
with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='lm-lightmanager',
    version=version['__version__'],
    packages=find_packages(exclude=('tests', 'docs')),
    url='https://github.com/leonarddevries/lm-server',
    license='MIT',
    author='Leonard de Vries',
    author_email='leonard@ldvengineering.nl',
    description='Light manager controlling several distributed light modules',
    install_requires=required,
)
