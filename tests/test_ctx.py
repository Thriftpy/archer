# -*- coding: utf-8 -*-
import pytest
from archer.ctx import AppContext
from archer import current_app, settings


def test_context_push(app):
    with pytest.raises(RuntimeError):
        current_app.name
    app_context = AppContext(app)
    app_context.push()
    assert current_app.name == app.name
    app_context.pop()
    with pytest.raises(RuntimeError):
        current_app.name


def test_settings(app):
    with pytest.raises(RuntimeError):
        settings['DEBUG']
    app_context = AppContext(app)
    app_context.push()
    assert 'DEBUG' in settings
    assert hasattr(settings, 'DEBUG')


def test_app_context(app):
    with AppContext(app):
        assert current_app.name == app.name
