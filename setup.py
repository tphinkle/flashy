#!/usr/bin/env python

from setuptools import setup

setup(
    name='flashcard',
    version='0.1',
    packages=['flashcard'],
    include_package_data=True,
    install_requires=[
        'flask',
    ]
)
