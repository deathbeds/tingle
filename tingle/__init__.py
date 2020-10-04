"""Tangling operations for different literate files."""
__version__ = "0.1.0"

from . import md, rst, python, loaders, yml, util
from .loaders import *

with Markdown(lazy=True):
    from . import weave
