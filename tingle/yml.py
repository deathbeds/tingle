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


def md2yml(object, parser=tingle.md.md2docutils):
    """convert text to python using docutils as an intermediate."""
    lines = [(x if x.strip() else x.strip()) +
             "\n" for x in object.splitlines()]
    body = """"""
    least_indent, ending_indent, prior_indent, extra_indent = 0, 0, 0, 0
    continued, quoted, commented = False, False, False
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
            # indent the code relative to the prior indent
            if commented or not body:
                noncode = textwrap.indent(noncode, "# ")
            noncode = textwrap.indent(
                noncode, " "*(least_indent + ending_indent + 4))

            # quote the noncode

        noncode = continue_lead(noncode, least_indent, continuing=continued)
        body += noncode + code

        commented = lines[end_line-1].lstrip().startswith('#')

        # update the line numbers and indents
        prior_line, prior_indent = end_line, ending_indent

        ending_indent = trailing_indent(code) - least_indent

    noncode = ''.join(lines[prior_line:len(lines)])

    if commented or not body:
        noncode = textwrap.indent(noncode, "# ")

    noncode = textwrap.indent(
        noncode, " "*(least_indent + ending_indent + 4))

    body += noncode
    return textwrap.dedent(body)


rst2yml = functools.partial(md2yml, parser=tingle.rst.rst2docutils)
