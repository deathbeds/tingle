# `tingle` documents schema specifications

it turns out that the literate yaml format provides a keen interface for
building documents and specifying schema.

        title:

a schema written in a literate format.

        required: [foo]
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

        #

it is necessary to use > or | markup for the previous description because of the
leading tick that breaks the yaml parsers.

todo: it is possible use yaml features like anchors and aliases to build rich schema.