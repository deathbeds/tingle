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
        return tingle.util.ipy_transform(tingle.python.md2py(str))

    def exec_module(self, module):
        super().exec_module(module)
        module._ipython_display_ = lambda: print(module.__file__) or __import__(
            "IPython").display.display(__import__("IPython").display.Markdown(filename=module.__file__))


class XO(LiterateMixin):
    format = ".md"
    extensions = F".xsh{format} .xsh{format}.ipynb".split()

    @property
    def execer(self):
        import xonsh.execer
        import builtins
        if hasattr(self, '_execer'):
            return self._execer
        if (
            hasattr(builtins, "__xonsh__")
            and hasattr(builtins.__xonsh__, "execer")
            and builtins.__xonsh__.execer is not None
        ):
            self._execer = execer = builtins.__xonsh__.execer
        else:
            self._execer = xonsh.execer.Execer(unload=False)
        return self._execer

    def code(self, str):
        return tingle.util.ipy_transform(tingle.python.md2py(str))

    def parse(self, input):
        execer = self.execer
        execer.filename = self.path
        ctx = {}  # dummy for modules
        return self.execer.parse(input, ctx, mode='exec',
                                 filename=self.path, transform=True)

    def exec_module(self, module):
        super().exec_module(module)
        module._ipython_display_ = lambda: print(module.__file__) or __import__(
            "IPython").display.display(__import__("IPython").display.Markdown(filename=module.__file__))


class RST(LiterateMixin):
    format = 'rst'
    extensions = F".py.{format} .{format} .{format}.ipynb".split()

    def code(self, str):
        return tingle.util.ipy_transform(tingle.python.rst2py(str))


class LiterateDataMixin(LiterateMixin):

    def code(self, code):
        if self.path.endswith(".md"):
            code = tingle.yml.md2yml(code)

        if self.path.endswith(".rst"):
            code = tingle.yml.rst2yml(code)

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


YML = YAML
