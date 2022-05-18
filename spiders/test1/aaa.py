# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: aaa.py
    Time: 2022/5/18 18:17
-------------------------------------------------
    Change Activity: 2022/5/18 18:17
-------------------------------------------------
    Desc: 
"""
import types
from functools import wraps


class Request(object):

    def __init__(self, func):
        wraps(func)(self)

    @staticmethod
    def fetch(func):
        print('fetch: ', func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            print('fetch: ', args)

            r = func(*args, **kwargs)
            return r

        return wrapper

    @staticmethod
    def __test1():
        print('test1')

    @staticmethod
    def fetch1(func):
        print('fetch1: ', func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            print('fetch1: ', args)

            args[1]['a'] = 'fetch1'

            Request.__test1()

            r = func(*args, **kwargs)
            return r

        return wrapper


class Spider(object):

    @Request
    def __init__(self):
        print('BBB')

        self.aaa = 'aaa'

    # @Request.fetch
    # def b(self, ppp):
    #     print('ppp: ', ppp)
    #
    #     return 'hello world 1'

    @Request.fetch1
    def b(self, ppp):
        print('ppp: ', ppp)

        return 'hello world 2'


if __name__ == '__main__':
    print(Spider().b({'a': 'ppp'}))
