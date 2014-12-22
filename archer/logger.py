# -*- coding: utf-8 -*-

_logger = None


def log(type, message, *args, **kwargs):
    """Log into archer logger."""
    global _logger
    if _logger is None:
        import logging

        _logger = logging.getLogger('archer')
        # Only set up a default log handler if the
        # end-user application didn't set anything up.
        if not logging.root.handlers and _logger.level == logging.NOTSET:
            _logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            _logger.addHandler(handler)
    getattr(_logger, type)(message.rstrip(), *args, **kwargs)
