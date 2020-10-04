"""Tangling operations for different literate files."""
__version__ = "0.1.0"

from . import md, rst, python, loaders, util
from .loaders import *

with Markdown(lazy=True):
    from . import yml, weave, parameterize
