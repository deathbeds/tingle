def main():
    with __import__('tingle').Markdown():
        from . import readme

    readme.app()
