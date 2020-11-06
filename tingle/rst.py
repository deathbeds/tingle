def rst2docutils(str):
    """convert rst into docutils nodes"""
    import docutils.core
    import docutils.parsers.rst

    settings = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser,)
    ).get_default_values()

    reporter = docutils.utils.Reporter(
        __import__('io').StringIO(),
        settings.report_level,
        settings.halt_level,
        stream=settings.warning_stream,
        debug=settings.debug,
        encoding=settings.error_encoding,
        error_handler=settings.error_encoding_error_handler)

    document = docutils.nodes.document(
        settings, reporter, source=reporter.source)

    docutils.parsers.rst.Parser().parse(str, document)
    return document
