#!/usr/bin/env python3

class A:

    foo = 1

    def __init__(self):
        self.bar = 2

    @property
    def bar(self):
        return self._baz

    @bar.setter
    def bar(self, value):
        self._baz = value
