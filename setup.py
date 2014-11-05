#!/usr/bin/env python

import os.path
import sys

from setuptools import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'testproject'))

setup(
    version='0.1.1',
    url='https://github.com/nathforge/django-wiretap',
    name='django-wiretap',
    description='https://github.com/nathforge/django-wiretap',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='Nathan Reynolds',
    author_email='email@nreynolds.co.uk',
    packages=['wiretap'],
    package_dir={'': 'src'},
    install_requires=[
        'django-roma'
    ]
)
