.. _errorhandling:

errorhandling
=============

register error handler
----------------------

Exceptions occurs during an API calling would be caught by the error handlers
registered. if no one is provided, the default handler would catch it.
In Archer,an error handler is registed like::

    app.register_error_handler(error, handler)

In which,e is the Exception,f is the error handler,for example::

    class BasicException(Exception):
        pass

    def BasicErrorHandler(meta, result):
        return 'BasicException'

    app.register_error_handler(BasicException, BasicErrorHandler)

The two arguments meta and result refers to :class:`~archer.app.ApiMeta` and :class:`~archer.app.ResultMeta`.

Whenever a BasicException occurs,Archer will catch it and call BasicErrorHandler to handle it.
