# -*- coding: utf-8 -*-

import redis


def print_meta(meta):
    print meta.start_time
    print meta.args
    print meta.name
    print meta.app
    print meta.f


def print_result(meta, result):
    elapsed = result.end_time - meta.start_time
    print('time spend ', elapsed)


class Redis(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        from archer.observer import before_api_call
        from archer.observer import after_api_call

        before_api_call.add_observer(print_meta)
        after_api_call.add_observer(print_result)

        self.client = redis.StrictRedis()

    def __getattr__(self, item):
        return getattr(self.client, item)

