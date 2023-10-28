#!/usr/bin/env python

import os
from distutils.core import setup
import subprocess

# convert readme to rst format
try:
   import pypandoc
   long_description = pypandoc.convert('README.md', 'rst')
except:
   long_description = ''

versionfile = "podsixnet/version.py"
if not os.path.isfile(versionfile):
    # assume git checkout
    __version__ = subprocess.check_output(["git", "describe", "--tag", "--always"]).decode("utf8").strip("\n")
else:
    # created by pip
    exec(open(versionfile).read())

setup(
    version=__version__,
    name='podsixnet2',
    description='Multiplayer networking library for games',
    long_description=long_description,
    author='Chris McCormick',
    author_email='chris@mccormick.cx',
    url='https://github.com/chr15m/PodSixNet',
    packages=['podsixnet2'],
)
