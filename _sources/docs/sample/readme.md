# fizzbuzz literate program

a fizzbuzz program written as a literate program.

## continuous integration

tests and builds documentation using the same content. usually documentation, tests, and code are separated which is useful for mature ideas. meanwhile, literate programs are more flex in more ambiguous problems.

* tests the module with [`pytest`][pytest]
* produces documentation on [github pages].
* this repository produces a pdf artifact.

## developer

the [`doit`][doit] tasks are used by github actions to test and build docs. the `"readme.md"` document
is imported in the `"dodo.py"` configuration file, and any function beginning with `"task_"` is 
recognized by [`doit`][doit].

        #pip install doit 

### building the documentation.

        # pip install .[doc] # requires the module tests dependencies.
        def task_book():

build a html book with [jupyter book] based on the `"_toc.yml" and "_config.yml"` configuration files.

            return dict(actions=["jb build ."], file_dep=["_toc.yml"], targets=["_build/html"])

        def task_pdf():

build a pdf version of the html book.

            return dict(actions=["jb build . --builder pdfhtml"], file_dep=['_toc.yml'], targets=['_build/pdf/book.pdf'])

### development mode

        def task_develop():

setup up develop mode using [`flit`][flit] with the configuration defined in `"pyproject.yml"`.

            return dict(actions=["flit install -s"], file_dep=['pyproject.yml'])

### testing mode.

run `pytest` in the root directory to test this module, extended settings are set in `"pyproject.yml"`.

        #!pytest

[jupyter book]: #
[flit]: #
[doit]: #
[pytest]: #
[github pages]: #