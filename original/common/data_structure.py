# -*- coding: utf-8 -*-
from __future__ import absolute_import


class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    TODO: 字典内置保留字无法复制
    """
    def __getattr__(self, name):
        # type: (str) -> Any
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        # type: (str, Any) -> None
        self[name] = value
