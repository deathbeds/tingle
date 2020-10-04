# `tingle` command line interface


        import typer, typing, pathlib, tingle, sys
        
        
        def main(ctx: typer.Context, 
                file: pathlib.Path, 
                main: bool=typer.Option(True, "--main/--no-main"),
                weave: bool=typer.Option(False, "--weave/--no-weave")
        ):

The command line interface for running documents as code.
Documents are parameterized by their literal expressions.
            
                module, command = tingle.parameterize.Parameterized.command(file, main=main)
                with tingle.util.argv([str(file)] + ctx.args):
                        try: command.main()
                        except SystemExit as e:
                                if e.args != (0,):
                                        return
                                if any(x for x in "-h --help".split() if x in sys.argv):
                                        return

if the weave option is active, show the output

                if module and weave:
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


        app = typer.Typer(
                no_args_is_help=True,                 
                add_completion=False,
                add_help_option=False)        
        app.command(context_settings=dict(                              
                        allow_extra_args=True, 
                        ignore_unknown_options=True,
                ))(main)

        