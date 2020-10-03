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


def demojize(lines, delimiters=('_', '_')):
    str = ''.join(lines or [])
    import tokenize
    import emoji
    import stringcase
    tokens = []
    try:
        for token in list(tokenize.tokenize(
                __import__('io').BytesIO(str.encode()).readline)):
            if token.type == tokenize.ERRORTOKEN:
                string = emoji.demojize(token.string, delimiters=delimiters
                                        ).replace('-', '_').replace("’", "_")
                if tokens and tokens[-1].type == tokenize.NAME:
                    tokens[-1] = tokenize.TokenInfo(tokens[-1].type, tokens[-1].string +
                                                    string, tokens[-1].start, tokens[-1].end, tokens[-1].line)
                else:
                    tokens.append(
                        tokenize.TokenInfo(
                            tokenize.NAME, string, token.start, token.end, token.line))
            else:
                tokens.append(token)
        return tokenize.untokenize(tokens).decode()
    except BaseException:
        ...
    return ''.join(lines)
