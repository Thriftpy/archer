# -*- coding: utf-8 -*-
import os
import pytest
from archer import Archer


@pytest.fixture
def app():
    app = Archer(
        'pingpong',
        os.path.join(os.path.dirname(__file__), 'pingpong.thrift'),
        service='PingPong')

    @app.api(SDF=123, sdfxcof=123123)
    def mget(ids):
        if ids > 100:
            raise app.thrift_module.PingPongException(200, 'id cannot greater than 100')
        # raise ValueError("no such id {}".format(ids))
        return u'you got it'

    @app.api(name='ping')
    def ping():
        return 'pong'

    @app.api
    def query(id):
        return 'id'

    @app.api(name='fuck_api', shield=True)
    def fuck():
        return 'fuck??'

    return app
