# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: spider.py
    Time: 2022/5/18 17:02
-------------------------------------------------
    Change Activity: 2022/5/18 17:02
-------------------------------------------------
    Desc: 
"""
import copy
import importlib
import threading
import time
from queue import Queue

from magician.sync_spider.http.request import Request
from magician.sync_spider.http.response import Response
from magician.sync_spider.middleware.download.downloader import Downloader
from magician.utils import load_objects
from magician.sync_spider.config.settings import Settings
from magician.sync_spider.common.log_setting import get_logger
from magician.sync_spider.databases.init_db import InitDatabase


class InitBaseSpider(object):
    name = 'init_base_spider'

    spider_start_time = time.time()

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', self.name)
        self.custom_setting = kwargs.get('custom_setting', {})
        self.settings_path = kwargs.get('settings_path')
        self.common_settings_path = kwargs.get('common_settings_path')

        self.__load_settings(self.custom_setting)

        self.logger = get_logger(self)

        self.__load_dbs()

    def __load_settings(self, custom_setting={}):
        self.init_settings = Settings()
        self.init_settings.set_dict(custom_setting)

        if self.settings_path:
            try:
                self.init_settings.load_config(importlib.import_module(self.common_settings_path))

            except Exception as e:
                pass

            self.init_settings.load_config(importlib.import_module(self.settings_path))

    def __load_dbs(self):
        self.dbs = InitDatabase(self).dbs

        for db in self.dbs:
            setattr(self, db['name'], db['instance'])

    def __close_dbs(self):
        for db in self.dbs:
            db['instance'] and db['instance'].close_pool()

    def close_spider(self, spider_name):
        self.__close_dbs()
        self.logger.success(f'{spider_name} Time usage: {time.time() - self.spider_start_time}')
        self.logger.success(f'{spider_name} Spider finished!')
        self.logger.success(f'{spider_name} Close Spider!')


class SyncSpider(InitBaseSpider):
    name = 'sync_spider'

    spider_data = {}
    default_custom_setting = {}
    settings_path = None
    base_spider = None
    common_settings_path = 'spiders.common.settings'

    def __init__(self, *args, **kwargs):
        self.custom_setting = kwargs.get('custom_setting', {})
        self.custom_setting.update(self.default_custom_setting)

        kwargs['custom_setting'] = self.custom_setting
        kwargs['name'] = self.name
        kwargs['settings_path'] = self.settings_path
        kwargs['common_settings_path'] = self.common_settings_path

        super().__init__(*args, **kwargs)

        self.settings = Settings()
        self.settings.set_dict({k: v.value for k, v in self.init_settings.attrs.items()})
        self.settings.set_dict(copy.deepcopy(self.custom_setting))

        self.__load_crawlers()

        self.consumer_thread_num = self.settings['CONSUMER_THREAD_NUM'] or 10
        self.spider_queue = Queue(1000)
        self.spider_event = threading.Event()

    def start_spider(self):
        raise NotImplementedError

    def start(self):
        self.logger.info(f'{self.__class__.__name__} Start Spider!')

        try:
            self.start_spider()

        except Exception as e:
            self.logger.exception(f'sync_spider.start.error: {e}')

        finally:
            self.close_spider(self.__class__.__name__)

    def close_spider(self, spider_name):
        """
        self.spider_init.close_spider = 关闭之前处理一些任务，例如发送爬虫采集的条数
        self.init_spider.close_spider = 爬虫结束，关闭数据库连接，log 输出
        """
        # if hasattr(self, 'spider_init'):
        #     if hasattr(self.spider_init, 'close_spider'):
        #         self.spider_init.close_spider()

        super().close_spider(spider_name)

    def __load_crawlers(self):
        crawlers = self.settings.get('CRAWLERS', {})

        for k, v, in crawlers.items():
            setattr(self, k, load_objects(v))

    @Downloader.download
    def download(self, request: Request = None, **kwargs) -> Response:
        """
        param request: Request 对象
        param kwargs:
            kwargs s5:                  是否启动 5s盾 请求，默认 False
            kwargs url:                 url
            kwargs data:                post 参数
            kwargs json:                post json 参数
            kwargs params:              url 参数
            kwargs method:              请求方式 GET POST
            kwargs encoding:            response 编码
            kwargs headers:             请求头
            kwargs session:             是否使用全局 session 对象请求，默认是 True
            kwargs use_middleware:      是否执行 response 中间件函数，默认 True
            kwargs kwargs:              其他参数 **kwargs
        return: Response or None
        """
