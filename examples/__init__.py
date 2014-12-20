# -*- coding: utf-8 -*-


from archer import Archer

app = Archer(__name__, 'examples/pingpong.thrift', service='PingPong')


@app.api(name='get', api=None, ksadf=123)
def get(id):
    return id + 2



@app.api(SDF=123, sdfxcof=123123)
def mget(ids):
    # raise ValueError("no such id {}".format(ids))
    return u'you got it'


@app.api(name='ping')
def ping():
    return 'pong'


@app.api
def query(id):
    return 123


from archer.extensions.archer_redis import Redis

redis = Redis(app)


@app.api
def redis_get(k):
    return redis.get(k) + 'from app'

@app.api
def redis_set(k, v):
    return redis.set(k, v)

@app.api(name='fuck_api')
def fuck():
    return 'fuck??'

# app.mget(123)
# print app.get(12)
# print app.query(123)
# print app.ping()
app.run()