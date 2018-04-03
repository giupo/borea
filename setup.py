#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'tornado==5.0.1',
    'coloredlogs==9.0'
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-bdd',
    'pytest-xdist',
    'pytest-watch'
]

setup(
    name='borea',
    version='0.0.1',
    description='Python BOREA API services',
    long_description=readme + '\n\n' + history,
    author='Giuseppe Acito',
    author_email='giuseppe.acito@gmail.com',
    url='https://github.com/giupo/borea',
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='borea',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass={'test': PyTest},
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'borea=borea.app:main'
        ]
    }
)
