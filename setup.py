# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='le-lightmanager',
    version='0.0.1',
    packages=find_packages(exclude=('tests', 'docs')),
    url='https://github.com/ <not yet>',
    license='',
    author='Leonard de Vries',
    author_email='leonard@ldvengineering.nl',
    description='Light manager controlling several distributed light modules'
)
