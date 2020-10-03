# test literate python and markdown

    
    import pytest
    def test_schema():
        import tingle 
        with tingle.YAML():
            import tingle.tests.testschema as module
        import jsonschema
        jsonschema.validate(dict(foo="xxx"), module.data)
        with pytest.raises(BaseException):
            jsonschema.validate(dict(), module.data)