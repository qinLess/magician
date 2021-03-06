# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: init_db.py
    Time: 2021/4/29 下午6:58
-------------------------------------------------
    Change Activity: 2021/4/29 下午6:58
-------------------------------------------------
    Desc: 
"""
from magician.utils import load_objects


class InitDatabase(object):

    def __init__(self, spider):

        self.spider = spider
        self.logger = spider.logger
        self.settings = spider.init_settings

        self.post_gre_config = self.settings['POST_GRE_CONFIG']
        self.mysql_config = self.settings['MYSQL_CONFIG']
        self.redis_config = self.settings['REDIS_CONFIG']

        self.dbs = []

        self.__load_dbs()
        self.__init_dbs()

    def __set_dict(self, name, instance=None):
        self.dbs.append({'name': name, 'instance': instance})

    def __load_dbs(self):
        self.sql_handler = load_objects(self.settings['POST_GRE_SQL_HANDLER'])
        self.redis_handler = load_objects(self.settings['REDIS_HANDLER'])
        self.mysql_handler = load_objects(self.settings['MYSQL_HANDLER'])

    def __init_dbs(self):
        # redis
        if isinstance(self.redis_config, dict):
            self.__set_dict('redis', self.redis_handler(config=self.redis_config))
        elif isinstance(self.redis_config, list):
            for rc in self.redis_config:
                self.__set_dict(rc["name"], self.redis_handler(config=rc))
        else:
            self.logger.warning('未添加 redis 配置')
            self.__set_dict('redis')

        # PostGreSql
        if isinstance(self.post_gre_config, dict):
            self.__set_dict('post_gre', self.sql_handler(config=self.post_gre_config, spider=self.spider))
        elif isinstance(self.post_gre_config, list):
            for pgc in self.post_gre_config:
                self.__set_dict(pgc["name"], self.sql_handler(config=pgc, spider=self.spider))
        else:
            self.logger.warning('未添加 post gre sql 配置')
            self.__set_dict('post_gre')

        # mysql
        if isinstance(self.mysql_config, dict):
            self.__set_dict('mysql', self.mysql_handler(config=self.mysql_config, spider=self.spider))
        elif isinstance(self.mysql_config, list):
            for my in self.mysql_config:
                self.__set_dict(my["name"], self.mysql_handler(config=my, spider=self.spider))
        else:
            self.logger.warning('未添加 mysql 配置')
            self.__set_dict('mysql')
