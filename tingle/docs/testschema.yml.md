# `tingle` documents schema specifications

it turns out that the literate yaml format provides a keen interface for
building documents and specifying schema. this demonstrates a sample.

## Top level information

        title:

a schema written in a literate format.

        required: [foo]
        
## Properties        
        
        properties:
                foo:
                        type: string
                        title: Foo
                        description:

an example of a dictionary that has a string property `foo`.

                bar:
                        type: number
                        title: Bar
                        description: >

`bar` is another, but it is not required.


### a note

        # everything after this point is a comment until more code is found.

it is necessary to use > or | markup for the previous description because of the
leading tick that breaks the yaml parsers.

todo: it is possible use yaml features like anchors and aliases to build rich schema.

## definitions

        defs: {}