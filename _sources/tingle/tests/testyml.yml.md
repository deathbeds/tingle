# a literate yaml file

this document demonstrates a hybrid markdown/yml syntax. it makes it possible to turn data into stories and stories to data.

in this hybrid, everything preceding the first code block is treated as a comment. following the first code block, markdown and yaml interact.

now we'll begin writing yaml as indented code.

        some key: some value
        foo: 
                {bar: 10, baz: 20}
        #
any markdown following a comment, pound, (ie #) is considered a comment.

more yaml can float beginning with inlined text.


## lists

        list_of_markdown:
- first thing
- second thing

        a conflicting list of markdown: >

* list beginning with star conflict with yaml
* `> and |` must be used to refer to the trailing markdown as block strings.

        plus lists are opaque to yaml: 

+ this is just a string.

        numbered lists are opaque to yaml: 

1. an opaque list item
        
