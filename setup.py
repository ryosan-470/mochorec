#!/usr/bin/env python3
from setuptools import setup
import mochorec


def _load_requires_from_file(filepath):
    return [pkg_name.rstrip('\r\n') for pkg_name in open(filepath).readlines()]


def _install_requires():
    return _load_requires_from_file('requirements.txt')


setup_options = dict(
    name='mochorec',
    packages=["mochorec"],
    version=mochorec.__version__,
    description='A CLI for nicovideo live',
    long_description=open('README.md').read(),
    author='Ryosuke SATO @jtwp470',
    author_email='rskjtwp@gmail.com',
    url='https://github.com/jtwp470/mochorec',
    entry_points={
        "console_scripts": ['mochorec = mochorec.__main__']
    },
    install_requires=_install_requires(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Natural Language :: Japanese',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3 :: Only',
    ),
)

setup(**setup_options)
