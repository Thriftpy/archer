# -*- coding: utf-8 -*-
import mock
import itertools


class BasicException(Exception):
    pass


class E1(BasicException):
    pass


class E2(E1):
    pass


class E3(E2):
    pass


class E4(E3):
    pass


def test_register_error_handler(app):
    f = mock.MagicMock()
    for e1, e2, e3, e4, e in itertools.permutations(
            (E1, E2, E3, E4, BasicException)):
        app.register_error_handler(e1, f)
        app.register_error_handler(e2, f)
        app.register_error_handler(e3, f)
        app.register_error_handler(e4, f)
        app.register_error_handler(e, f)
        assert app.registered_errors[0] is E4
        assert app.registered_errors[1] is E3
        assert app.registered_errors[2] is E2
        assert app.registered_errors[3] is E1
        assert app.registered_errors[4] is BasicException
        app.registered_errors = []
        app.error_handlers = {}


def f1(meta, result):
    return 'f1'


def f2(meta, result):
    return 'f2'


def f3(meta, result):
    return 'f3'


def test_error_handler_call_order(app):
    @app.api('error_order')
    def error_order():
        raise E3

    @app.api('error_order1')
    def error_order1():
        raise E2

    @app.api('error_order2')
    def error_order2():
        raise E1

    app.register_error_handler(E1, f1)
    app.register_error_handler(E2, f2)
    app.register_error_handler(E3, f3)
    client = app.test_client
    assert client.error_order() == 'f3'
    assert client.error_order1() == 'f2'
    assert client.error_order2() == 'f1'
