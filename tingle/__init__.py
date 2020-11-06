"""Tangling operations for different literate files."""
__version__ = __import__("datetime").date.today().strftime("%Y.%m.%d")

from . import md, rst, python, loaders, util, weave
from .loaders import *
from . import parameterize
from .loaders import *

with Markdown(lazy=True):
    from . import yml, yml as yaml


def load_ipython_extension(shell):
    from . import extension
    extension.load_ipython_extension(shell)


def unload_ipython_extension(shell):
    from . import extension
    extension.unload_ipython_extension(shell)
