# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: log_setting.py
    Time: 2022/5/18 17:46
-------------------------------------------------
    Change Activity: 2022/5/18 17:46
-------------------------------------------------
    Desc: 
"""
import logging.config

import os
import datetime
import logging
import logging.handlers
import sys

from loguru import logger


class SpiderLogger(object):
    instance = {}
    init_flag = {}

    def __new__(cls, *args, **kwargs):
        spider = kwargs['spider']
        name = spider.name

        if not cls.instance.get(name):
            cls.instance[name] = super().__new__(cls)

        return cls.instance[name]

    def __init__(self, spider):
        name = spider.name
        if SpiderLogger.init_flag.get(name):
            return
        SpiderLogger.init_flag[name] = True

        self.logger = logging.getLogger(name)
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            day_date = datetime.datetime.now().strftime("%Y-%m-%d")
            log_path = spider.init_settings['LOGGER_PATH']
            self.log_path = os.path.join(log_path or 'logs/', f'{day_date}/')
            if not os.path.exists(self.log_path):
                os.makedirs(self.log_path)

            self.log_name = f'{self.log_path}{name + ".log"}'
            fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')
            fh.setLevel(logging.INFO)
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '[%(asctime)s] [%(process)d -> %(thread)d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)
            fh.close()
            ch.close()


class LogUruLogger(object):
    logger = logger
    logger.remove()

    def __init__(self, spider):
        name = spider.name

        day_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_path = spider.init_settings['LOGGER_PATH']
        log_path = os.path.join(log_path or 'logs/', f'{day_date}/')
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        log_name = f'{log_path}{name + ".log"}'

        formatter = '[<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>] ' \
                    '[<cyan>{process}</cyan> -> <cyan>{thread}</cyan>] ' \
                    '[<level>{level: <8}</level>] ' \
                    '<cyan>{file:}</cyan> -> <cyan>{function}</cyan>: <cyan>{line}</cyan> - ' \
                    '<level>{message}</level>'

        logger.add(sys.stdout, enqueue=True, format=formatter)
        logger.add(log_name, rotation='100 MB', retention='15 days', enqueue=True, format=formatter)


def get_logger(spider):
    return LogUruLogger(spider=spider).logger
    # return SpiderLogger(spider=spider).logger
