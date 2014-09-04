#!/usr/bin/env python
# coding: utf8

import sys

from super_state_machine import __version__ as version

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Hacking unittest.
try:
    import tests
    if 'test' in sys.argv and '--quick' in sys.argv:
        tests.QUICK_TESTS = True
        del sys.argv[sys.argv.index('--quick')]
except ImportError:
    pass

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='super_state_machine',
    version=version,
    description='Super State Machine gives you utilities to build finite state machines.',
    long_description=readme + '\n\n' + history,
    author='Szczepan Cieślik',
    author_email='szczepan.cieslik@gmail.com',
    url='https://github.com/beregond/super_state_machine',
    packages=[
        'super_state_machine',
    ],
    package_dir={'super_state_machine':
                 'super_state_machine'},
    include_package_data=True,
    install_requires=[
        'enum34',
        'six',
    ],
    license="BSD",
    zip_safe=False,
    keywords='super_state_machine',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
)
