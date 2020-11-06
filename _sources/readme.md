# `tingle` tangle

`tingle` is a library to __import__ modern markup and data languages into python programs. it provides machinery to _tangle_ code from its document language to python modules. tangle is a concept from literate programming that describes converting document into compiled program languages.

currently, `tingle` supports 

        from tingle import md, rst, yml, yaml

`tingle` is primarily designed for interactive computing to generalize the reuse of code in different formats. `tingle` can be used with `jupyter` or `IPython` to import alternative document formats as python modules.

`tingle` is a `pytest` extension that can test literate programs written
in markdown or rst formats. it ensures that your documentation stays up to date with your code.

## importing literate programs and data

`tingle` uses context managers to modify pythons conventional imports.

        import tingle
        with tingle.loaders.Markdown():
            ...

`tingle.loaders.Markdown` is a loader that can discover notebooks with cells written in markdown and individual markdown files.

context managers can combined into a single context manager.

        import importnb
        with importnb.Notebook(), tingle.loaders.Markdown():
            ...

or used in serial

        with importnb.Notebook():
            ...
        with tingle.loaders.Markdown():
            ...

serial loading is necessary in the special case that two modules are loaded from files with the same name, but different extensions.

### parameterized modules

## fuzzy imports

a feature of `importnb` is the discovery of invalidate python module names. consider a notebook that is a blog post. `1968-12-09-mother-of-all-demos.ipynb`

        with tingle.loaders.Markdown():
            try:
                from .docs import _968_12_09_mother_of_all_demos, __mother_of_all_demos
            except:
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

            return dict(actions=[
                "jb build . --toc docs/_toc.yml --config docs/_config.yml"
            ], file_dep=['docs/_toc.yml', 'docs/_config.yml'], targets=['_build/html'])

        def task_pdf():

configure a pdf to build from the book task.

            object = task_book()
            object['actions'][0] += F"  --builder pdfhtml" 
            object['targets'][0] = object['targets'][0].replace('html', 'pdf')
            return object

        def task_test():

test the `tingle` package using `pytest`. extra pytest arguments are included in `"pyproject.toml"` meaning we can use the top-level `pytest` execution.

            return dict(actions=["pytest"])