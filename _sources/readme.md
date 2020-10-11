# `tingle` tangle

`tingle` is a library to _tangle_ modern markup and data languages
into python programs. _tangle_ is a concept from literate programming
that describes converting document into compiled program languages.

`tingle` allows folks to think different about their literature that
can serve alternative roles as programs and data.

`tingle` uses `docutils` and `myst_parser` to parse RST and Markdown to 
intermediate representations as `docutils` documents. from the `docutils`
document heuristics are applied to transform the document language to
python or yml files.

`tingle` is a `pytest` extension that can test literate programs written
in markdown or rst formats.

## importing literate programs and data

        import tingle
        with tingle.loaders.Markdown():
            ...

## the `tingle` extension

```ipython
%load_ext tingle
```

`tingle` is an `IPython` extension that makes small modifications to the interactive computing experience.

1. allows markdown input in cells, there is no weaving step, see `nowidget` for more on weaving.
2. top level returns
3. emojis

see the [`"extension.md"`](tingle/extension.md)


## developing

the tasks below require `doit`, `#pip install doit`.

        def task_book():

Build the docs using jupyter book.

            return dict(actions=["jb build ."], file_dep=['_toc.yml'], targets=['_build/html'])

        def task_pdf():
            return dict(actions=["jb build . --builder pdfhtml"], file_dep=['_toc.yml'], targets=['_build/pdf/book.pdf'])


        def task_test():

test the `tingle` package using `pytest`. extra pytest arguments are included in `"pyproject.toml"` meaning we can use the top-level `pytest` execution.

            return dict(actions=["pytest"])