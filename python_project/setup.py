#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='whatever',
    entry_points={
        'console_scripts': [
            'whatever_ok = whatever:ok',
            'whatever_exception = whatever:exception',
        ],
    },
)
