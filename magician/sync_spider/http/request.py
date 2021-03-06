# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: request.py
    Time: 2022/5/18 19:07
-------------------------------------------------
    Change Activity: 2022/5/18 19:07
-------------------------------------------------
    Desc: 
"""
from pickle import dumps, loads
from urllib.parse import urlencode


class Request(object):
    def __init__(self, url, params=None, method='GET', data={}, headers={}, meta={},
                 json=None, encoding='utf-8', use_middleware=True, session=True, s5=False,
                 stream=False, **kwargs):
        self.s5 = s5
        self.url = url
        self.data = data
        self.json = json
        self.params = params
        self.method = method
        self.encoding = encoding
        self.headers = headers
        self.session = session
        self.use_middleware = use_middleware
        self.stream = stream
        self.kwargs = kwargs

        self.meta = self._load_meta(meta)

    def copy(self, *args, **kwargs):
        keys = [
            'url', 'method', 'data', 'json', 'params', 'headers', 'meta', 'session',
            'use_middleware', 's5', 'stream'
        ]
        for key in keys:
            kwargs.setdefault(key, getattr(self, key))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)

    def dumps(self):
        return dumps(self)

    def loads(self):
        return loads(self)

    @staticmethod
    def _load_meta(custom_meta):
        meta = {
            'test_key': 'test_key1',
            'proxy': None,
            'retry_count': 0
        }

        if isinstance(custom_meta, dict):
            meta.update(custom_meta)

        return meta

    def __str__(self):
        return "<Request: retry_count<%d> %s %s>" % (
            self.meta['retry_count'],
            self.method,
            self.url + urlencode(self.meta.get('params')) if self.meta.get('params') else self.url
        )

    __repr__ = __str__
