# `tingle` command line interface

        import typer, typing, pathlib
        app = typer.Typer()        
        
        def main(files: typing.List[pathlib.Path], weave: bool=typer.Option(False)):

The command line interface for running documents as code.
Documents are parameterized by their literal expressions.
            
            print(files)

        def tangle(file: pathlib.Path, target: str = None):

Translate a document from the document language to a target language;
the program is not executed.


        app.command()(main)

        