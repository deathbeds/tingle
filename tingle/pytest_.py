import importnb.utils.pytest_importnb
from . import loaders


def pytest_collect_file(parent, path):
    return Tests(parent, path)


class Markdown(importnb.utils.pytest_importnb.NotebookModule):

    # the pytest extension is named poorly
    loader = loaders.Markdown


class RST(importnb.utils.pytest_importnb.NotebookModule):

    # the pytest extension is named poorly
    loader = loaders.RST


class Tests(importnb.utils.pytest_importnb.NotebookTests):

    modules = Markdown, RST
