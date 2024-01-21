#!/usr/bin/env python3
'''
A simple Python library to create .ICO files (Windows icon file format).
'''

import importlib.metadata
__version__ = importlib.metadata.version(__package__)

from .IcoFile import IcoFile
from . import IcoFile
