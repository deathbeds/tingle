import markdown_it.extensions.footnote
import docutils.nodes
import myst_parser.docutils_renderer


def front_matter(state, startLine, endLine, silent=False):
    if startLine:
        return False

    if not state.src.startswith(("+++", "---")):
        return False

    lead = state.src[:3]

    if set(state.src[:state.eMarks[startLine]]) == set(lead):
        return False

    nextLine = startLine + 1

    while nextLine < endLine:
        if state.src[state.bMarks[nextLine]: state.eMarks[nextLine]].startswith(lead):
            auto_closed = True
            break
        nextLine += 1
    else:
        return False

    old_parent = state.parentType
    old_line_max = state.lineMax
    state.parentType = "container"

    # this will prevent lazy continuations from ever going past our end marker
    state.lineMax = nextLine

    token = state.push("front_matter", "", 0)
    token.hidden = True
    token.markup = lead
    token.content = state.src[
        state.bMarks[startLine + 1]: state.eMarks[nextLine-1]
    ]

    token.block = True
    token.meta = state.src[:state.bMarks[0]]

    state.parentType = old_parent
    state.lineMax = old_line_max
    state.line = nextLine
    token.map = [startLine, state.line - 1]

    return True


def code(state, startLine, endLine, silent=False):
    if state.sCount[startLine] - state.blkIndent < 4:
        return False

    last = nextLine = startLine + 1

    while nextLine < endLine:
        if state.isEmpty(nextLine):
            nextLine += 1
            continue
        start = state.bMarks[nextLine] + state.tShift[nextLine]
        if state.src[start: start+4] == '>>> ':
            break
        if state.sCount[nextLine] - state.blkIndent >= 4:
            nextLine += 1
            last = nextLine
            continue
        break

    state.line = last

    token = state.push("code_block", "code", 0)
    token.content = state.getLines(startLine, last, 4 + state.blkIndent, True)
    token.map = [startLine, state.line]

    return True


def doctest(state, startLine, endLine, silent, *, offset=0, continuation=True):
    """A doctest lexer for markdownit"""
    nextLine, start, maximum = (startLine, state.bMarks[startLine] +
                                state.tShift[startLine], state.eMarks[startLine])

    if not state.src[start:maximum].startswith(">>> "):
        return False
    while nextLine < endLine:
        nextLine += 1
        start, maximum = state.bMarks[nextLine] + \
            state.tShift[nextLine], state.eMarks[nextLine]
        if continuation:
            continuation = state.src[start:maximum].startswith("... ")
            if continuation:
                continue

        if state.src[start:maximum].strip():
            if state.src[start:maximum].startswith(">>> "):
                offset = 1
                break
            continue
        break

    old_parent, old_line_max = state.parentType, state.lineMax
    state.parentType, state.lineMax = "container", nextLine-offset

    token = state.push("doctest", "code", 0)
    token.content = state.src[state.bMarks[startLine]
        : state.eMarks[state.lineMax]]
    token.map = [startLine, state.lineMax]
    state.parentType, state.lineMax, state.line = old_parent, old_line_max, nextLine

    return True


def render_doctest(self, token):
    """A missing docutils rendered for myst."""
    node = docutils.nodes.doctest_block(
        ''.join(token.content), ''.join(token.content))
    self.add_line_and_source_path(node, token)
    self.current_node.append(node)


myst_parser.docutils_renderer.DocutilsRenderer.render_doctest = render_doctest


class MarkdownIt(markdown_it.MarkdownIt):
    def parse(self, src, env):
        env = markdown_it.utils.AttrDict() if env is None else env
        if not isinstance(env, markdown_it.utils.AttrDict):
            raise TypeError(
                f"Input data should be an AttrDict, not {type(env)}")
        if not isinstance(src, str):
            raise TypeError(f"Input data should be a string, not {type(src)}")

        state = markdown_it.rules_core.state_core.StateCore(src, self, env)
        self.core.process(state)
        return state.tokens


markdown = MarkdownIt().disable('inline')
markdown.block.ruler.before("code", "doctest", doctest, {"alt": []},)
markdown.disable("code")
markdown.disable("html_block")
markdown.enable("table")
markdown.block.ruler.after("doctest", "code", code, {"alt": []},)
markdown.use(markdown_it.extensions.footnote.footnote_plugin)
markdown.block.ruler.before(
    "table",
    "front_matter",
    front_matter,
    {"alt": ["paragraph", "reference", "blockquote", "list"]},
)


def md2docutils(str):
    global markdown
    env = markdown_it.utils.AttrDict()
    tokens = markdown.parse(str, env)
    return myst_parser.docutils_renderer.DocutilsRenderer(markdown).render(
        tokens, {}, env)
