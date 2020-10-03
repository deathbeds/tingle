def rst2docutils(str):
    import docutils.core

    settings = docutils.frontend.OptionParser(
        components=(docutils.parsers.rst.Parser,)
    ).get_default_values()

    io = __import__('io').StringIO()

    reporter = docutils.utils.Reporter(
        io,
        settings.report_level,
        settings.halt_level,
        stream=settings.warning_stream,
        debug=settings.debug,
        encoding=settings.error_encoding,
        error_handler=settings.error_encoding_error_handler)

    document = docutils.nodes.document(settings, reporter, source=io)

    docutils.parsers.rst.Parser().parse(str, document)
    return document
