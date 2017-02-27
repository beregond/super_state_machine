#!/usr/bin/env python
# coding: utf-8

import sys
from setuptools.command.test import test as TestCommand

from super_state_machine import __version__ as version

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


PROJECT_NAME = 'super_state_machine'


class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['--cov', PROJECT_NAME]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

if sys.version_info < (3, 4):
    compat_req = ['six', 'enum34']
else:
    compat_req = ['six']


setup(
    name='super_state_machine',
    version=version,
    description=(
        'Super State Machine gives you utilities '
        'to build finite state machines.'
    ),
    long_description=readme + '\n\n' + history,
    author='Szczepan Cieślik',
    author_email='szczepan.cieslik@gmail.com',
    url='https://github.com/beregond/super_state_machine',
    packages=[
        'super_state_machine',
    ],
    package_dir={'super_state_machine': 'super_state_machine'},
    include_package_data=True,
    install_requires=compat_req,
    license="BSD",
    zip_safe=False,
    keywords='super_state_machine',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass={
        'test': PyTest,
    },
)
