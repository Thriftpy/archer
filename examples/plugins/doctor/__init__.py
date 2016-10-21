# -*- coding: utf-8 -*-

import logging
logging.basicConfig()

from archer import Archer
from doctor.plugins.archer import Doctor

app = Archer('PingPong')
doctor = Doctor(app.thrift.PingPongException(
    -1,
    'HEALTH_CHECK_FAIL',
    'Api is not heathy',
    ))
doctor.init_app(app)

@app.api(name='mget', SDF=123, sdfxcof=123123)
def mget(ids):
    return 'mget %s' % ids


@app.api(name='ping')
def ping():
    import time
    time.sleep(1)
    return 'pong'


@app.api(name='health_check')
def health_check(id):
    raise Exception


@app.api(name='query')
def query(id):
    raise Exception
    return 'id'

cache = {}


@app.api(name='set_v')
def set_v(k, v):
    cache[k] = v


@app.api(name='get', api=None, ksadf=123)
def get(k):
    return cache.get('k', 'not found')


@app.shell_context_processor
def redis_ctx():
    return {'redis': 'redis'}


if __name__ == '__main__':
    app.run()
