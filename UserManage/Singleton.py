# -*- coding: utf-8 -*-
class singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):

        if not cls._instance:
            cls._instance = super(singleton,cls).__new__(cls,*args,**kwargs)

        return cls._instance