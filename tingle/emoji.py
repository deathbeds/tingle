"""permit emojis as validate python names."""


def demojize(lines, delimiters=('_', '_')):
    str = ''.join(lines or [])
    import tokenize
    import emoji
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
        return tokenize.untokenize(tokens).decode().splitlines(True)
    except BaseException:
        ...
    return ''.join(lines)


def load_ipython_extension(shell):
    if demojize not in shell.input_transformer_manager.cleanup_transforms:
        shell.input_transformer_manager.cleanup_transforms.append(demojize)


def unload_ipython_extension(shell):
    if demojize not in shell.input_transformer_manager.cleanup_transforms:
        shell.input_transformer_manager.cleanup_transforms.pop(
            shell.input_transformer_manager.cleanup_transforms.index(demojize)
        )
