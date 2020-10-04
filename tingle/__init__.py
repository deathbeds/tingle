"""Tangling operations for different literate files."""
__version__ = "0.1.0"

from . import md, rst, python, loaders, util
from .loaders import *

with Markdown(lazy=True):
    from . import yml, weave, parameterize
    from . import weave


def load_ipython_extension(shell):
    with Markdown():
        from . import extension
    extension.load_ipython_extension(shell)


def unload_ipython_extension(shell):
    with Markdown():
        from . import extension
    extension.unload_ipython_extension(shell)
