"""# parameterize modules

`tingle` parameterizes modules based on expressions that have annotations.

1. create module finds the annotated statements that can be literally evaluated.
2. the loader returns an intermediate representation.
3. the intermediate representation is called to trigger exec module with a modified context.


---

    

# the `Parameterized` type"""

import tingle
import typing
import types


class Parameterized:

    # analyze the abstract syntax tree

    def visit(self, node):
        import sys
        import ast
        node = super(type(self), self).visit(node)
        if sys.version_info[1] > 7:
            body, annotations = ast.Module([], []), ast.Module([], [])
        else:
            body, annotations = ast.Module([]), ast.Module([])
        while node.body:
            element = node.body.pop(0)
            if isinstance(element, ast.Assign) or (isinstance(element, ast.AnnAssign) and element.target.id[0].islower()):
                try:
                    if element.value:
                        ast.literal_eval(element.value)
                    annotations.body.append(element)
                    continue
                except:
                    ...
            if isinstance(element, (ast.Import, ast.ImportFrom)):
                annotations.body.append(element)
            body.body.append(element)
        self.arg_code = compile(annotations, self.path, 'exec')
        return body

    # parameterized module creation

    def create_module(loader, spec=None):
        import runpy
        if spec is None:
            import importlib
            spec = importlib.util.spec_from_loader(loader.name, loader)
            module = super(type(loader), loader).create_module(spec)
        loader.main_code = loader.get_code(loader.name)
        runpy._run_code(loader.arg_code, vars(module),
                        {}, '__main__', spec, None, None)
        return module

    # defered module execution

    def exec_module(loader, module=None, **globals):
        import runpy
        module = module or loader.create_module()
        vars(module).update(globals)
        runpy._run_code(loader.main_code, vars(module), {},
                        '__main__', module.__spec__, None, None)
        return module

    # defer module loader

    @classmethod
    def load(cls, filename, main=False, loaders=(tingle.Markdown, tingle.RST), **kwargs) -> typing.Tuple[types.ModuleType, typing.Callable]:

        import importlib
        import inspect
        if '.xsh' in str(filename):
            loaders = (tingle.loaders.XO, ) + loaders

        for loader in loaders:
            if str(filename).endswith(tuple(loader.extensions)):
                loader = type('tmploader', (loader,), {})
                loader.visit = cls.visit
                loader = loader(str(filename), str(filename), **kwargs)
                module = cls.create_module(loader)

                def main(**kwargs):
                    nonlocal loader, module
                    cls.exec_module(loader, module, **kwargs)
                    return module

                # update the function docstring and signature allowing other tools to infer apis.

                main.__doc__ = module.__doc__

                # below we build an cli with `typer`, by modifying the signature here `typer` can infer a cli from the signature.

                parameters = []
                for k in set(dir(module) + list(getattr(module, "__annotations__", {}))):
                    if not k[0].islower():
                        continue
                    kwargs = {}
                    kind = hasattr(
                        module, k) and inspect.Parameter.KEYWORD_ONLY or inspect.Parameter.POSITIONAL_ONLY
                    if hasattr(module, k):
                        kwargs['default'] = getattr(module, k)
                    if k in getattr(module, "__annotations__", {}):
                        kwargs['annotation'] = module.__annotations__[k]
                    parameters += [inspect.Parameter(k, kind, **kwargs)]
                main.__signature__ = inspect.Signature(
                    parameters=parameters)
                return module, main

# create a command using `typer`

    @classmethod
    def command(cls, file, **kwargs):
        import typer
        module, exec = cls.load(file, **kwargs)
        app = typer.Typer(add_completion=False)
        app.command(context_settings=dict(
            allow_extra_args=True,
            ignore_unknown_options=True,
            help_option_names=['-h', '--help']
        ))(exec)
        return module, typer.main.get_command(app)
