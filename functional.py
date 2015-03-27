# coding: utf-8
from __future__ import absolute_import, unicode_literals, print_function


class cached_property(object):

    def __init__(self, func, name=None):
        self.func = func
        self.name = name or func.__name__

    def __call__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res
