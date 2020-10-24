# `tingle` tangle

`tingle` is a library to __import__ modern markup and data languages
into python programs. it provides machinery to _tangle_ code; a concept from literate programming that describes converting document into compiled program languages.

`tingle` allows folks to think about literature that can serve as programs and data.

`tingle` brings the ability to __import__ and test markdown, yaml, json, images, xonsh, and lisp literate programs as python modules.


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

## what does it do?

the import discovery hooks are implemented in the `importnb` package. `tingle` is specifically concerned with the need to __tangle__ input to source code.

it uses `docutils` and `myst_parser` to parse RST and Markdown to 
intermediate representations as `docutils` documents. from the `docutils`
document heuristics are applied to transform the document language to
python or yml files.



## developing

the tasks below require `doit`, `#pip install doit`.

        def task_book():

Build the docs using jupyter book.

            return dict(actions=["jb build . --toc docs/_toc.yml --config docs/_config.yml"], file_dep=['docs/_toc.yml', 'docs/_config.yml'], targets=['_build/html'])

        def task_pdf():
            return dict(actions=["jb build . --builder pdfhtml"], file_dep=['_toc.yml'], targets=['_build/pdf/book.pdf'])


        def task_test():

test the `tingle` package using `pytest`. extra pytest arguments are included in `"pyproject.toml"` meaning we can use the top-level `pytest` execution.

            return dict(actions=["pytest"])