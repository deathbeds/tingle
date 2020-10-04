import contextlib


@contextlib.contextmanager
def argv(list):
    import sys
    prior, sys.argv = sys.argv, list
    yield
    sys.argv = prior
