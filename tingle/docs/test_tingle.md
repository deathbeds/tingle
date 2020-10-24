# test literate python and markdown

    import pytest, tingle
    
tests for the `tingle` package.

    def test_md_import():
test the abilities to import different data and files.

        with __import__("tingle").Markdown(lazy=True):
            import tingle.docs.testmd
        assert tingle.docs.testmd.__file__.endswith(".md")

    def test_yml_import():
test the abilities to import different data and files.

        with __import__("tingle").YAML(lazy=True):
            import tingle.docs.testyml
        assert tingle.docs.testyml.__file__.endswith(".md")
        
    def test_xsh_import():
        with __import__("tingle").loaders.XO(lazy=True):
            import tingle.docs.testxo

    def test_schema():
        with tingle.YAML(lazy=True):
            import tingle.docs.testschema as module
        import jsonschema
        jsonschema.validate(dict(foo="xxx"), module.data)
        with pytest.raises(BaseException):
            jsonschema.validate(dict(), module.data)