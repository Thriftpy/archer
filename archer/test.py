# -*- coding: utf-8 -*-


class TestClient(object):
    """
    fake_client will call the wrapped api function,
    going through all middlewares
    """

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
    fake_client will call the original api function directly,
     bypass all middlewares
    """

    def __init__(self, app):
        self.app = app

    def __getattr__(self, item):
        api = self.app.api_map.get(item)
        if api is None:
            raise ValueError(
                'app didn\'t registered this api: {}'.format(item))
        return self.app.api_map.get(item).__wrapped__