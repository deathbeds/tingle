# test literate python and markdown

    import pytest, tingle
    
tests for the `tingle` package.

    def test_md_import():
test the abilities to import different data and files.

        with __import__("tingle").Markdown():
            import tingle.tests.testmd
        assert tingle.tests.testmd.__file__.endswith(".md")

    def test_yml_import():
test the abilities to import different data and files.

        with __import__("tingle").YAML():
            import tingle.tests.testyml
        assert tingle.tests.testyml.__file__.endswith(".md")

    def test_schema():
        with tingle.YAML(lazy=True):
            import tingle.tests.testschema as module
        import jsonschema
        jsonschema.validate(dict(foo="xxx"), module.data)
        with pytest.raises(BaseException):
            jsonschema.validate(dict(), module.data)