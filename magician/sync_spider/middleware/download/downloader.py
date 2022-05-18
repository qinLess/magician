# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: downloader.py
    Time: 2022/5/18 19:10
-------------------------------------------------
    Change Activity: 2022/5/18 19:10
-------------------------------------------------
    Desc: 
"""
from functools import wraps

import requests
import urllib3
from requests import adapters

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
adapters.DEFAULT_RETRIES = 5


class Downloader(object):

    @staticmethod
    def __download(request):
        """开始下载

        Args:
            request: request 对象
        Returns:
            response 对象
        """

        if request.s5:
            instance = self.scrape
            if request.session:
                instance = self.scrape_session

        elif request.session:
            instance = self.session

        else:
            instance = requests

        request.kwargs['timeout'] = request.kwargs.get('timeout', self.settings['REQUEST_TIMEOUT'])

        if request.method.upper() == 'POST':
            response = instance.post(
                request.url,
                data=request.data,
                json=request.json,
                headers=request.headers,
                params=request.params,
                stream=request.stream,
                proxies=request.meta.get('proxy'),
                verify=self.settings['REQUEST_VERIFY'],
                **request.kwargs
            )

        else:
            response = instance.get(
                request.url,
                headers=request.headers,
                params=request.params,
                stream=request.stream,
                proxies=request.meta.get('proxy'),
                verify=self.settings['REQUEST_VERIFY'],
                **request.kwargs
            )

        response.encoding = request.encoding

        res = Response(response, request)

        self.logger.info(f"Downloaded ({res.status}) {str(request)}")
        return res

    @staticmethod
    def download(func):
        print('fetch1: ', func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            r = func(*args, **kwargs)
            return r

        return wrapper
