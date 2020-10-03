"""Tangle code to python."""

import textwrap
import functools

import tingle
QUOTES = "'''", '"""'


def continue_lead(object, indent=0, *, body="", continuing=True):
    non_empty = False
    for line in object.splitlines(True):
        empty = not line.strip()
        if empty:
            body += (' '*indent + "\\" if continuing else "") + line
        else:
            continuing = line.rstrip().endswith("\\")
            body += line

    return body


def dedent(str):
    """Dedent a block of non code."""
    str = textwrap.dedent(str)
    lines = str.splitlines(True)
    for i, line in enumerate(lines):
        if line.strip():
            lines[i] = textwrap.dedent(line)
            break
    return "".join(lines)


def quote(str, trailing=''):
    """Wrap a truple block quotations."""
    quote, length = QUOTES[QUOTES[0] in str], len(str)
    left, right = length - len(str.lstrip()), len(str.rstrip())
    if not str[left:right].strip():
        return str
    if str[right-1] == '\\':
        while str[right-1] == '\\':
            right -= 1
    else:
        if str[left:right].endswith(quote[0]):
            quote = {"'''": '"""', '"""': "'''"}[quote]
    return str[:left] + quote + str[left:right] + quote + trailing + str[right:]


def leading_indent(str):
    """Count the lead indent of a string"""
    if not isinstance(str, list):
        str = str.splitlines(True)
    for line in str:
        if line.strip():
            return len(line) - len(line.lstrip())
    return 0


def trailing_indent(str):
    """Count the lead indent of a string"""
    if not isinstance(str, list):
        str = str.splitlines(True)
    for line in reversed(str):
        if line.strip():
            return len(line) - len(line.lstrip())
    return 0


def filter_literal_blocks(document):
    for node in document.traverse():
        if node.tagname == 'literal_block' and node.attributes.get('language', "") in {"none", ""}:
            yield node


def hanging_indent(str, extra_indent):
    start = len(str)-len(str.lstrip())
    return str[:start] + ' ' * extra_indent + str[start:]


def md2py(object, parser=tingle.md.md2docutils):
    """convert text to python using docutils as an intermediate."""
    lines = [(x if x.strip() else x.strip()) +
             "\n" for x in object.splitlines()]
    body = """"""
    least_indent, ending_indent, prior_indent, extra_indent = 0, 0, 0, 0
    continued, quoted = False, False
    start_line, prior_line, end = 0, 0, len(lines)
    tokens = list(filter_literal_blocks(parser(object)))
    for i, node in enumerate(tokens):
        start_line = node.line

        if node.attributes.get('language', "none") == "none":
            start_line -= 1

        # get noncode block
        noncode = ''.join(lines[prior_line:start_line])
        noncode = dedent(noncode)

        # get code block
        end_line = start_line + len(node.rawsource.splitlines())

        code = ''.join(lines[start_line:end_line])
        if node.attributes.get('language', None) == "":
            code = textwrap.indent(code, ' '*4)

        this_indent = leading_indent(code) - least_indent
        if not least_indent:
            # this is base indent for the entire block
            least_indent = this_indent

        if noncode.strip():
            # indent the code relative to the prior indents
            if body:
                noncode = hanging_indent(noncode, max(
                    ending_indent + extra_indent, this_indent))
            noncode = textwrap.indent(noncode, " "*least_indent)

            # quote the noncode
            if not quoted:
                noncode = quote(
                    noncode, trailing=';' if node is None else '')

        noncode = continue_lead(noncode, least_indent, continuing=continued)
        body += noncode + code

        # update the line numbers and indents
        prior_line, prior_indent = end_line, ending_indent

        strip = code.rstrip()
        ending_indent = trailing_indent(code) - least_indent
        continued = strip.endswith("\\")
        extra_indent = 4*strip.endswith(':')
        quoted = strip.endswith(QUOTES)

    noncode = ''.join(lines[prior_line:len(lines)])
    noncode = hanging_indent(noncode, ending_indent + extra_indent)
    noncode = textwrap.indent(noncode, " "*least_indent)

    body += quote(noncode, ";")
    return textwrap.dedent(body)


rst2py = functools.partial(md2py, parser=tingle.rst.rst2docutils)
