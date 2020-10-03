# `tingle` command line interface

        import typer, typing, pathlib
        app = typer.Typer()        
        
        def main(ctx: typer.Context, file: pathlib.Path, weave: bool=typer.Option(False)):

The command line interface for running documents as code.
Documents are parameterized by their literal expressions.
            
            print(vars(ctx))
            if weave:
                typer.echo("")


        def tangle(file: pathlib.Path, target: str = None):

Translate a document from the document language to a target language;
the program is not executed.

        def export():

Export a collection of documents to another format.        

        app.command(context_settings={"allow_extra_args": True})(main)

        