#!/usr/bin/env python3

from setuptools import find_packages, setup

setup(
    name='frelia',
    version='0.1.0',
    packages=find_packages(exclude=['frelia_tests', 'frelia_tests.*']),
    install_requires=[
        'networkx',
        'PyYAML',
    ],
    entry_points={
    },

    author='Allen Li',
    author_email='darkfeline@felesatra.moe',
    description='Static website generator library',
    license='',
    url='',
)
