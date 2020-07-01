#!/usr/bin/env python

import re
import os
from os.path import abspath, dirname, join
from setuptools import setup

CURDIR = dirname(abspath(__file__))
REQUIREMENTS = ['robotframework >= 3.0']
with open(join(CURDIR, 'src', 'formulated_automation', 'version.py')) as f:
    VERSION = re.search("^VERSION = '(.*)'", f.read()).group(1)
with open(join(CURDIR, 'README.rst'), encoding='utf-8') as f:
    DESCRIPTION = f.read()
print(dir(os.listdir(CURDIR)))
CLASSIFIERS = '''
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.8
Topic :: Software Development :: Testing
Framework :: Robot Framework
Framework :: Robot Framework :: Library
'''.strip().splitlines()

setup(
    name='robotframework-profiler',
    version=VERSION,
    description='Robot Framework System Profiler',
    long_description=DESCRIPTION,
    author='Formulated Automation',
    author_email='hello@formulatedautomation.com',
    url='https://github.com/itsautomic/robotframework-otp',
    license='Apache License 2.0',
    keywords='robotframework testing testautomation profiler',
    platforms='any',
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    package_dir={'': 'src'},
    packages=['formulated_automation']
)
