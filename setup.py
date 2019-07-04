#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup, find_packages


MODULE_NAME = 'sentry_wrapper'

DEPENDENCIES = [
    'sentry-sdk',
]

TEST_DEPENDENCIES = [
]


def get_version():
    """ Reads package version number from package's __init__.py. """
    with open(os.path.join(
        os.path.dirname(__file__), MODULE_NAME, '__init__.py'
    )) as init:
        for line in init.readlines():
            res = re.match(r'^__version__ = [\'"](.*)[\'"]$', line)
            if res:
                return res.group(1)


def get_long_description():
    """ Read description from README and CHANGES. """
    with open(
        os.path.join(os.path.dirname(__file__), 'README.rst')
    ) as readme, open(
        os.path.join(os.path.dirname(__file__), 'CHANGES.rst')
    ) as changes:
        return readme.read() + '\n' + changes.read()


setup(
    name=MODULE_NAME.replace('_', '-'),
    version=get_version(),
    description='Forward exceptions raised by a setuptools entrypoint to sentry',
    long_description=get_long_description(),
    author='Julien Castets',
    author_email='castets.j@gmail.com',
    url='http://scaleway.com/',
    packages=find_packages(),
    install_requires=DEPENDENCIES,
    tests_require=DEPENDENCIES + TEST_DEPENDENCIES,
    dependency_links=[
    ],
    test_suite=MODULE_NAME + '.tests',
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Topic :: System :: Distributed Computing',
    ],
    license='WTFPL',
    entry_points={
        'console_scripts': [
            'sentry-wrapper = sentry_wrapper:execute',
            'sentry-msg     = sentry_msg:execute',
        ],
    },
)
