# -*- coding: utf-8 -*-
from functools import partial
import sys
from .local import LocalStack, LocalProxy


class AppContext(object):
    """The application context binds an application object implicitly
    to the current thread or greenlet
    """

    def __init__(self, app):
        self.app = app

        self._refcnt = 0

    def push(self):
        """Binds the app context to the current context."""
        self._refcnt += 1
        _app_ctx_stack.push(self)
        _app_ctx_stack.top.settings = self.app.config

    def pop(self, exc=None):
        """Pops the app context."""
        self._refcnt -= 1
        if self._refcnt <= 0:
            if exc is None:
                exc = sys.exc_info()[1]
        rv = _app_ctx_stack.pop()
        assert rv is self, 'Popped wrong app context.  (%r instead of %r)' \
                           % (rv, self)

    def __enter__(self):
        self.push()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.pop(exc_value)


_app_ctx_err_msg = '''\
Working outside of application context.

This typically means that you attempted to use functionality that needed
to interface with the current application object in a way.  To solve
this set up an application context with app.app_context().  See the
documentation for more information.\
'''


def _find_app():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return top.app


def _lookup_app_object(name):
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return getattr(top, name)


_app_ctx_stack = LocalStack()

current_app = LocalProxy(_find_app)

settings = LocalProxy(partial(_lookup_app_object, 'settings'))
