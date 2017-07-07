# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='disktypes',
    version='0.1.0',
    description='Disk backed datatypes for reduced memory usage',
    long_description=readme,
    author='Philip Poten',
    author_email='philip.poten@gmail.com',
    url='https://github.com/elpollodiablo/python-disktypes',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

