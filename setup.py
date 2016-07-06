#!/usr/bin/env python


"""Install script for `treniformis`."""


import os

from setuptools import find_packages
from setuptools import setup


# Grab all non python files in the treniformis
# tree
here = os.path.dirname(__file__)
data_files = []
for root, dirs, files in os.walk(os.path.join(here, 'treniformis')):
    dirs[:] = [x for x in dirs if not x.startswith('.')]
    for filename in files: 
        name, ext = os.path.splitext(filename)
        if ext not in ['.py', '.pyc']:
            data_files.append(os.path.join(root, filename))


setup(
    name='treniformis',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'treniformis': data_files
    },
    version='0.1',
    description='',
    author='Global Fishing Watch',
    author_email='info@GlobalFishingWatch.org',
    url='https://github.com/GlobalFishingWatch/treniformis',
)
