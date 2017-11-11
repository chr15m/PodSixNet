#!/usr/bin/env python

from distutils.core import setup

# convert readme to rst format
try:
   import pypandoc
   long_description = pypandoc.convert('README.md', 'rst')
except:
   long_description = ''

setup(
    name='PodSixNet',
    description='Multiplayer networking library for games',
    author='Chris McCormick',
    author_email='chris@mccormick.cx',
    url='https://github.com/chr15m/PodSixNet',
    packages=['PodSixNet'],
    version="0.8",
)
