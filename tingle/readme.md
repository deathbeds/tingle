# `tingle` command line interface

        import typer, typing, pathlib, tingle
        app = typer.Typer()        
        
        def main(ctx: typer.Context, 
                
                file: pathlib.Path, 
                main: bool=typer.Option(True, "--main/--no-main"),
                weave: bool=typer.Option(False, "--weave/--no-weave")
        ):

The command line interface for running documents as code.
Documents are parameterized by their literal expressions.
            
                module, exec = tingle.loaders.Parameterized.load(file, main=main)
                app = typer.Typer()
                app.command()(exec)
                with tingle.util.argv([str(file)] + ctx.args):
                        try: typer.main.get_command(app).main()
                        except SystemExit: ...

if the weave option is active, show the output

                if weave:
                        woven = tingle.weave.weave(file.read_text(), **vars(module))
                        try:
                                import pygments
                                woven = pygments.highlight(woven, pygments.lexers.MarkdownLexer(), pygments.formatters.TerminalFormatter())
                        except: ...
                        typer.echo(woven)


        def tangle(file: pathlib.Path, target: str = None):

Translate a document from the document language to a target language;
the program is not executed.

        def export():

Export a collection of documents to another format.        

        app.command(context_settings={
                "allow_extra_args": True, "ignore_unknown_options": True
        })(main)

        