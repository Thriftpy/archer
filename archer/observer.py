# -*- coding: utf-8 -*-


class Observable(object):
    def __init__(self, name):
        self.name = name
        self.observers = []

    def add_observer(self, f):
        self.observers.append(f)

    def detach_observer(self, f):
        self.observers.remove(f)

    def notify(self, *args, **kwargs):
        for observer in self.observers:
            observer(*args, **kwargs)


before_api_call = Observable('before_api_call')
after_api_call = Observable('after_api_call')
tear_down_api_call = Observable('tear_down_api_call')

