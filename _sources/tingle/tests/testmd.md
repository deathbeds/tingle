# sample document of `tingle` syntaxes.

`tingle` transforms markdown to python according to the relative position of the code blocks. this document describes the formations between code and _non_code blocks.

the most basic conformation are complete python statements and expressions with markdown narrative woven in between. under these conditions the code and _non_code do not interact.

        # state writing the program here
        import tingle
        ["xo"[i%2] for i in range(10)]

this is a basic case that happes commonly when describing scripts. `tingle` affords abilities where code and _non_code can interact.

## using markdown as strings

        blocks_of_narrative =\

are defined as variables using lines continuations.

        ...
        >>> blocks_of_narrative
        "are defined as variables using lines continuations."

blocks string can be defined explicitly.

        explicit_block = """
        
the body of markdown is wrapped in a block string that can be operated on.
        
        """.upper()

        tight_explicit_block = """\
        
the body of markdown is wrapped in a block string that can be operated on.\
        
        """.upper()

        tight_paren_block = (
        
the body of markdown is wrapped in a block string that can be operated on.\
        
        )  

## block statements

`tingle` handles indentations for python code relative block statements and expressions.

        def a_noop_function():
retains the following markdown and doctests as the docstring for the preceeding function defintion.

        def a_useful_function():
retains the following markdown and doctests as the docstring for the preceeding function defintion. the identation can be guided by the body of the function.

                    "this is a big indent"

but the interleaved strings are indented according to the `tingle` heuristics.

        class AClass:

definition also retains following narrative as the docstring.

                def for_nested_methods(self):

the narrative is indented and represents a more complicated `tingle` syntax that returns the formatted body of the narrative

                        return 


        if __name__ == '__main__':

test the defined docstrings.

                import doctest
                print(doctest.testmod())