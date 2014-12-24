# -*- coding: utf-8 -*-

from archer import Archer

app = Archer('example_app')


@app.api(name='mget', SDF=123, sdfxcof=123123)
def mget(ids):
    return 'mget %s' % ids


@app.api(name='ping')
def ping():
    return 'pong'


@app.api(name='query')
def query(id):
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
