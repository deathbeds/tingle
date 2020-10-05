    import tingle
    import traitlets

    class Extension(traitlets.HasTraits):
        shell = traitlets.Any()
        markup = traitlets.Unicode()
        def __call__(self, lines):
            if self.markup == 'md':
                return tingle.python.md2py(''.join(lines)).splitlines(True)
            elif self.markdup == 'rst':
                return tingle.python.rst2py(''.join(lines)).splitlines(True)
            return lines


    def load_ipython_extension(shell):
        if not shell.has_trait('tingle'):
            shell.add_traits(tingle=traitlets.Any())
            shell.tingle = Extension(shell=shell, markup="md")

        if shell.tingle.__call__ not in shell.input_transformer_manager.cleanup_transforms:
            shell.input_transformer_manager.cleanup_transforms.insert(0, shell.tingle.__call__)

    def unload_ipython_extension(shell):
        if shell.has_trait('tingle'):
            shell.input_transformer_manager.cleanup_transforms = [
                x for x in shell.input_transformer_manager.cleanup_transforms
                if x != shell.tingle.__call__
            ]

        
