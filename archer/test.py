# -*- coding: utf-8 -*-


class TestClient(object):
    def __init__(self, app):
        self.app = app

    def __getattr__(self, item):
        api = self.app.api_map.get(item)
        if api is None:
            raise ValueError(
                'app didn\'t registered this api: {}'.format(item))
        return self.app.api_map.get(item)


class FakeClient(TestClient):
    """
    call the original api function directly, bypass all middlewares
    """

    def __init__(self, app):
        self.app = app

    def __getattr__(self, item):
        api = self.app.api_map.get(item)
        if api is None:
            raise ValueError(
                'app didn\'t registered this api: {}'.format(item))
        return self.app.api_map.get(item).__wrapped__