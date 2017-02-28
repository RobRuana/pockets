# -*- coding: utf-8 -*-
# Copyright (c) 2016 the Pockets team, see AUTHORS.
# Licensed under the BSD License, see LICENSE for details.

"""A collection of helpful Python tools!"""

import os
from setuptools import setup, find_packages


# Package versioning solution originally found here:
# http://stackoverflow.com/q/458550
exec(open(os.path.join('pockets', '_version.py')).read())

reqs = open('requirements.txt', 'r').read().strip().splitlines()
test_reqs = open('requirements_test.txt', 'r').read().strip().splitlines()

setup(
    name='pockets',
    version=__version__,
    url='http://pockets.readthedocs.org',
    download_url='http://pypi.python.org/pypi/pockets',
    license='BSD',
    author='Rob Ruana',
    author_email='rob@robruana.com',
    description=__doc__,
    long_description=open('README.rst', 'r').read(),
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(exclude=['tests*']),
    install_requires=reqs,
    tests_require=test_reqs
)
