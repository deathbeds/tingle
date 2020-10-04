# test literate python and markdown

    import pytest
    
tests for the `tingle` package.

    def test_imports():
test the abilities to import different data and files.
    
    def test_schema():
        import tingle 
        with tingle.YAML(lazy=True):
            import tingle.tests.testschema as module
        import jsonschema
        jsonschema.validate(dict(foo="xxx"), module.data)
        with pytest.raises(BaseException):
            jsonschema.validate(dict(), module.data)