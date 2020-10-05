import contextlib


@contextlib.contextmanager
def argv(list):
    import sys
    prior, sys.argv = sys.argv, list
    yield
    sys.argv = prior


def ipy_transform(code):
    try:
        import IPython
        code = IPython.core.inputtransformer2.TransformerManager().transform_cell(code)
    except:
        ...
    return code
