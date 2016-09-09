#!/usr/bin/env python


"""Install script for `treniformis`."""


import itertools
import os

from setuptools import find_packages
from setuptools import setup


def _parse_dunder(line):

    """Parse a line like:

        __version__ = '1.0.1'

    and return:

        1.0.1
    """

    item = line.split('=')[1].strip()
    item = item.strip('"').strip("'")
    return item


root_dir = os.path.dirname(__file__)
data_files = []
for root, _, paths in os.walk(os.path.join(root_dir, 'treniformis')):
    paths = filter(lambda x: not x.startswith('.'), paths)
    for p in paths:
        name, ext = os.path.splitext(p)
        if ext not in ['.py', '.pyc']:
            data_files.append(os.path.join(root, p))


version = None
author = None
email = None
source = None
with open(os.path.join('treniformis', '__init__.py')) as f:
    for line in f:
        if line.find('__author__') >= 0:
            author = _parse_dunder(line)
        elif line.find('__email__') >= 0:
            email = _parse_dunder(line)
        elif line.find('__source__') >= 0:
            source = _parse_dunder(line)
        elif None not in (version, author, email, source):
            break

with open('VERSION') as f:
    version = f.read().strip()

with open('README.rst') as f:
    readme = f.read()


extra_reqs = {'test': ['pytest>=2.8.2', 'pytest-cov>=2.2.0']}

# Add all extra requirements
extra_reqs['all'] = list(set(itertools.chain(*extra_reqs.values())))


setup(
    name='treniformis',
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    package_data={
        'treniformis': data_files
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    version=version,
    description='Global Fishing Watch vessel lists',
    license='Apache 2.0',
    long_description=readme,
    author=author,
    author_email=email,
    url=source,
    keywords='GFW Global Fishing Watch vessel lists',
    zip_safe=True,
    extras_require=extra_reqs,
    install_requires=['six']
)
