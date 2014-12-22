# -*- coding: utf-8 -*-
from ._compat import iteritems
from collections import defaultdict


class Event(object):
    __events__ = {}

    def __new__(cls, name):
        if name not in cls.__events__:
            event = super(Event, cls).__new__(cls)
            cls.__events__[name] = event
            return event
        return cls.__events__[name]

    def __init__(self, name):
        self.name = name
        self.listeners = defaultdict(list)

    def add_listener(self, f, target=None):
        self.listeners[target].append(f)

    def detach_listener(self, f, target=None):
        self.listeners[target].remove(f)

    def notify(self, *args, **kwargs):
        target = kwargs.pop('target', None)
        if target is None:
            for target, listeners in iteritems(self.listeners):
                for listener in listeners:
                    listener(*args, **kwargs)
        else:
            for listener in self.listeners[target]:
                listener(*args, **kwargs)


before_api_call = Event('before_api_call')
after_api_call = Event('after_api_call')

tear_down_api_call = Event('tear_down_api_call')
