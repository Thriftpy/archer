# -*- coding: utf-8 -*-

import redis
from archer.ctx import _lookup_app_object, _app_ctx_stack, _app_ctx_err_msg, \
    current_app
from archer.event import before_api_call
from archer.local import LocalProxy


def _get_redis():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    top.archer_redis = current_app.extensions['archer_redis']
    return top.archer_redis


redis_cli = LocalProxy(_get_redis)


def inject_redis(meta):
    app = meta.app


def print_meta(meta):
    print(current_app)
    print (meta.start_time)
    print (meta.args)
    print (meta.name)
    print (meta.app)
    print (meta.f)
    info = meta.app.api_meta_map[meta.name]
    if info.get('shield'):
        print('shield api')


def print_result(meta, result):
    elapsed = result.end_time - meta.start_time
    print('time spend ', elapsed)


class Redis(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        from archer.event import before_api_call
        from archer.event import after_api_call

        app.extensions['archer_redis'] = self

        before_api_call.add_listener(inject_redis, app)
        before_api_call.add_listener(print_meta)
        after_api_call.add_listener(print_result)
        self.client = redis.StrictRedis()

    def __getattr__(self, item):
        return getattr(self.client, item)

