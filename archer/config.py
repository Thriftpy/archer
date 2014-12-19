# -*- coding: utf-8 -*-


class Config(object):
    pass

class ConfigAttribute(object):
    def __init__(self, name, converter=None):
        self.name = name
        self.converter = converter

    def __get__(self, instance, owner):
        if instance is None:
            return self
        rv = instance.config[self.name]
        if self.converter is not None:
            return self.converter(rv)
        return rv

    def __set__(self, instance, value):
        instance.config[self.name] = value
