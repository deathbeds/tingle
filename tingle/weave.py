"""# `tingle`, tangle, and weave

literate programming is a series of tangle and weave steps. the focus of `tingle`
is to provide machinery for converting documents to compiled code; this document
provides a minimal implementation of weaving and templating documents to strings.

we have to weave different files includes files and notebooks.
"""
import re


def weave(str, **globals):
    """Pass a set of globals through a string that has jinja templates that can be replaced with values
in the namespace.
"""
    import jinja2
    str = strip_shebang(str)
    str = strip_html_comment(str)
    return jinja2.Template(str).render(**globals)


def strip_shebang(str):
    return re.sub(re.compile(r"#!/.+\n"), "", str)


def strip_html_comment(str):
    return re.sub("(<!--[\s\S]*-->?)", "", str)


def post_run_cell(result):
    import IPython

    if result.info.raw_cell.splitlines()[0].strip():

        IPython.display.display(IPython.display.Markdown(
            weave(result.info.raw_cell, **IPython.get_ipython().user_ns)
        ))


def load_ipython_extension(shell):
    shell.events.register(post_run_cell.__name__, post_run_cell)


def unload_ipython_extension(shell):
    shell.events.unregister(post_run_cell.__name__, post_run_cell)
