# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: spider1.py
    Time: 2022/5/18 18:55
-------------------------------------------------
    Change Activity: 2022/5/18 18:55
-------------------------------------------------
    Desc: 
"""
from magician.sync_spider.core.spider import SyncSpider


class TestSpider1(SyncSpider):
    name = 'test_spider1'
    settings_path = 'spiders.test1.settings'

    default_custom_setting = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_spider(self):
        print('start_spider')


if __name__ == '__main__':
    TestSpider1().start()
