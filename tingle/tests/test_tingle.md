# test literate python and markdown

    

    def test_schema():
        import tingle 
        with tingle.YAML():
            import tingle.tests.testschema as module
        import jsonschema
        jsonschema.validate(dict(foo="xxx"), module.data)