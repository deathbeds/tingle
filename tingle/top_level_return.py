import ast
import tingle


class ExtraSyntax(ast.NodeTransformer):
    def visit_FunctionDef(self, node): return node
    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Return(self, node):
        replace = ast.parse(
            '''__import__('IPython').display.display()''').body[0]
        replace.value.args = node.value.elts if isinstance(
            node.value, ast.Tuple) else [node.value]
        return ast.copy_location(replace, node)

    def visit_Expr(self, node):
        if isinstance(node.value, (ast.Yield, ast.YieldFrom)):
            return ast.copy_location(self.visit_Return(node.value), node)
        return node

    visit_Expression = visit_Expr


def load_ipython_extension(shell):
    tingle.util.append_ast_transformers(shell, ExtraSyntax)


def unload_ipython_extension(shell):
    tingle.util.remove_ast_transformers(shell, ExtraSyntax)
