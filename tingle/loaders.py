import importnb
import tingle

__all__ = "Markdown", "RST", "YAML"


class LiterateMixin(importnb.Notebook):
    format = None

    def get_data(self, path):
        if self.path.endswith(self.format):
            return self.code(self.decode())
        return super().get_data(path)

    get_source = get_data


class Markdown(LiterateMixin):
    format = ".md"
    extensions = F".py{format} {format} {format}.ipynb".split()

    def code(self, str):
        return tingle.python.md2py(str)

    def exec_module(self, module):
        super().exec_module(module)
        module._ipython_display_ = lambda: print(module.__file__) or __import__(
            "IPython").display.display(__import__("IPython").display.Markdown(filename=module.__file__))


class RST(LiterateMixin):
    format = 'rst'
    extensions = F".py.{format} .{format} .{format}.ipynb".split()

    def code(self, str):
        return tingle.python.rst2py(str)


class LiterateDataMixin(LiterateMixin):

    def code(self, code):
        if self.path.endswith(".md"):
            return tingle.yml.md2yml(code)

        if self.path.endswith(".rst"):
            return tingle.yml.rst2yml(code)
        return code


class YAML(LiterateDataMixin):
    format = '.md'
    extensions = F".yml .yaml .yml.md .yaml.md".split()

    def code(self, str):
        code = F"""data = __import__('yaml').safe_load('''{super().code(str)}''')"""
        return code

    def exec_module(self, module):
        super().exec_module(module)
        module._ipython_display_ = lambda:  __import__(
            "IPython").display.display(__import__("IPython").display.JSON(module.data, root=module.__file__))


class Parameterized:
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
            if isinstance(element, ast.AnnAssign) and element.target.id[0].islower():
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

    def exec_module(loader, module=None, **globals):
        import runpy
        module = module or loader.create_module()
        vars(module).update(globals)
        runpy._run_code(loader.main_code, vars(module), {},
                        '__main__', module.__spec__, None, None)
        return module

    @classmethod
    def load(cls, filename, dir=None, main=False, loaders=(Markdown, RST), **kwargs):
        import importlib
        import inspect
        for loader in loaders:
            if str(filename).endswith(tuple(loader.extensions)):
                loader = type('tmploader', (loader,), {})
                loader.visit = cls.visit
                loader = loader(str(filename), str(filename), **kwargs)
                spec = importlib.util.spec_from_loader(str(filename), loader)
                module = cls.create_module(loader)

                def main(**kwargs):
                    nonlocal loader, module
                    cls.exec_module(loader, module, **kwargs)
                    return module

                main.__signature__ = inspect.Signature(parameters=[
                    inspect.Parameter(
                        k, inspect.Parameter.KEYWORD_ONLY, annotation=v, default=getattr(
                            module, k)
                    ) if hasattr(module, k) else inspect.Parameter(
                        k, inspect.Parameter.POSITIONAL_ONLY, annotation=v
                    )

                    for k, v in module.__annotations__.items()
                ])
                return module, main
