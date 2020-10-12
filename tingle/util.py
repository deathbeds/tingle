import contextlib


def append_ast_transformers(shell, transformer):
    if any(
        x for x in shell.ast_transformers
        if isinstance(x, transformer)
    ):
        return
    shell.ast_transformers.append(transformer())


def remove_ast_transformers(shell, transformer):
    shell.ast_transformers = [
        x for x in shell.ast_transformers
        if not isinstance(x, transformer)
    ]


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
    except BaseException:
        ...
    return code
