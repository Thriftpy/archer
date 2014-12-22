# -*- coding: utf-8 -*-
from mock import Mock


def test_app_register_api(app):
    dispatcher = Mock()
    dispatcher.test.__name__ = 'test'
    app.register_api('test', dispatcher.test)
    app.test()
    assert dispatcher.test.called

