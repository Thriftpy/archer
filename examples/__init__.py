# -*- coding: utf-8 -*-
import os

from archer import Archer

app = Archer('test_app',
             os.path.join(os.path.dirname(__file__), 'pingpong.thrift'),
             service='PingPong')
app1 = Archer('test_app',
              os.path.join(os.path.dirname(__file__), 'pingpong.thrift'),
              service='PingPong')


@app.api(name='get', api=None, ksadf=123)
def get(id):
    return id + 2


@app.api(SDF=123, sdfxcof=123123)
def mget(ids):
    return u'you got it'


@app.api(name='ping')
def ping():
    return 'pong'


@app.api
def query(id):
    return 'id'


from archer.ext.archer_redis import Redis

app.testing = True
app.debug = True

redis = Redis(app)


@app.api
def redis_get(k):
    return redis.get(k) + ' from app'


@app.api
def redis_set(k, v):
    return redis.set(k, v)


@app.api(name='fuck_api', shield=True)
def fuck():
    return 'fuck??'


@app.shell_context_processor
def redis_ctx():
    return {'redis': redis}


if __name__ == '__main__':
    app.run()