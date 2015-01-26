# -*- coding: utf-8 -*-
import mock
import pytest


def handler(meta, result):
    return 'yeah'


def test_exception_would_be_caught(app):
    client = app.test_client
    with pytest.raises(app.thrift.PingPongException):
        client.mget(120)


def test_register_default_error_handler(app):
    app.register_default_error_handler(handler)
    client = app.test_client
    assert client.mget(120) == 'yeah'


def test_register_error_handler(app):
    app.register_default_error_handler(handler)

    @app.errorhandler(app.thrift.PingPongException)
    def hand(meta, result):
        return 'hand'

    client = app.test_client
    assert client.mget(120) == 'hand'


def test_before_api_call(app):
    mock1 = mock.MagicMock()
    mock2 = mock.MagicMock()
    app.before_api_call(mock1)
    app.before_api_call(mock2)
    client = app.test_client
    client.mget(15)
    assert mock1.call_count == 1
    assert mock2.call_count == 1


def test_after_api_call(app):
    mock1 = mock.MagicMock()
    mock2 = mock.MagicMock()
    app.after_api_call(mock1)
    app.after_api_call(mock2)
    client = app.test_client
    client.mget(15)
    assert mock1.call_count == 1
    assert mock2.call_count == 1


def test_tear_down_api_call(app):
    mock1 = mock.MagicMock()
    mock2 = mock.MagicMock()
    app.tear_down_api_call(mock1)
    app.tear_down_api_call(mock2)
    client = app.test_client
    client.mget(15)
    assert mock1.call_count == 1
    assert mock2.call_count == 1



