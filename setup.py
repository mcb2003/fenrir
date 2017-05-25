#!/bin/python
#https://python-packaging.readthedocs.io/en/latest/minimal.html
import os
from setuptools import find_packages
from setuptools import setup
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    # Application name:
    name="fenrir",
    # Version number (initial):
    version="1.5a",

    # Application author details:
    author="Chrys, storm_dragon, Jeremiah and others",
    author_email="christian.hempfling@linux-a11y.org",

    # Packages
    packages=find_packages('src/fenrir'),
    package_dir={'': 'src/fenrir'},
    scripts=['src/fenrir/fenrir','src/fenrir/fenrir-daemon'],
    #entry_points = {
    #    "console_scripts": ['fenrir = fenrir:main']
    #    },

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/chrys87/fenrir/",
    zip_safe=False,
    #
    # license="MIT",
     description="An TTY  Screen Reader For Linux.",
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
],
    # Dependent packages (distributions)
    install_requires=[
        "evdev",
        "sox"
    ],
    
)

