#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""Setup script for TEN.

Distributed under the terms of the MIT License.
"""

#-----------------------------------------------------------------------------
# Instalation script bases on IPython setup.py (under BSD Licence)
# and from Python packaging user guide
# https://python-packaging-user-guide.readthedocs.org
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
from __future__ import print_function
import sys
import os

from setuptools import setup, find_packages

# Remove MANIFEST.
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')


#-----------------------------------------------------------------------------
# Check Python version
#-----------------------------------------------------------------------------
v = sys.version_info
if v[:2] < (2, 7) or (v[0] >= 3 and v[:2] < (3, 0)):
    error = "ERROR: TEN requires Python version 2.7 or 3.0 or above."
    print(error, file=sys.stderr)
    sys.exit(1)

PY3 = (sys.version_info[0] >= 3)
# At least we're on the python version we need, move on.


#-----------------------------------------------------------------------------
# Setup configuration
#-----------------------------------------------------------------------------
LONG_DESCRIPTION = """TEN

Collection of algorithms to simulate, using Monte Carlo method,the quantum
process of Energy Transfer in Nanoparticles (TEN for its acronym in Spanish)
in conjugated polymers.
TEN is designed to run efficiently on parallel computers.

It was developed at Laboratory of Advanced Optical Microscopy,
Universidad Nacional de Río Cuarto, Argentina. It is an open-source code,
distributed freely under the terms of the MIT License.

Please refer to the online documentation at
https://ten.readthedocs.org
"""
DISTNAME = 'ten'
DESCRIPTION = 'Simulation of energy transfer in nanoparticle'
MAINTAINER = 'Franco N. Bellomo, Lucas E. Bellomo'
MAINTAINER_EMAIL = 'fnbellomo@gmail.com, lbellomo@gmail.com'
URL = 'https://ten.readthedocs.org'
LICENSE = 'MIT'
DOWNLOAD_URL = 'http://github.com/pewen/ten'

# TEN version
with open('ten/__init__.py') as fid:
    for line in fid:
        if line.startswith('__version__'):
            VERSION = line.strip().split()[-1][1:-1]
            break

# Requires
with open('requirements.txt') as fid:
    INSTALL_REQUIRES = [l.strip() for l in fid.readlines() if l]

# Requirements for those browsing PyPI
REQUIRES = [r.replace('>=', ' (>= ') + ')' for r in INSTALL_REQUIRES]
REQUIRES = [r.replace('==', ' (== ') for r in REQUIRES]

setup(
    name=DISTNAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url=URL,
    license=LICENSE,
    download_url=DOWNLOAD_URL,
    version=VERSION,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Physics',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],

    packages=find_packages(exclude=['doc', 'IPython_notebook']),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    requires=REQUIRES,
    zip_safe=False, # the package can run out of an .egg file
    entry_points={
        'console_scripts': ['ten = ten.scripts.cli_main:main'],
    }
)
