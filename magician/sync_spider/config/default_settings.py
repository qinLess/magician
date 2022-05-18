# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: default_settings.py
    Time: 2022/5/18 17:39
-------------------------------------------------
    Change Activity: 2022/5/18 17:39
-------------------------------------------------
    Desc: 
"""

# -------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------------------------

# post ger sql 操作类
POST_GRE_SQL_HANDLER = 'magician.sync_spider.databases.post_gre_sql_pool.PostGreHandle'

# mysql 操作类
MYSQL_HANDLER = 'magician.sync_spider.databases.mysql_pool.MysqlHandler'

# redis 操作类
REDIS_HANDLER = 'magician.sync_spider.databases.redis_pool.RedisHandler'

# -------------------------------------------------------------------------------------------------------------------

# 初始化 代理 IP 数量
PROXY_NUM = 5

# 重试次数
RETRY_COUNT = 3

# 包含一下状态吗，重试
RETRY_STATUS_CODES = [500, 502, 503, 504, 400, 403, 408]

# 忽略 ssl 验证
REQUEST_VERIFY = False

# 请求超时时间
REQUEST_TIMEOUT = 30

# 5s盾，delay 时间
SCRAPER_DELAY = 30

# 消费者线程数
CONSUMER_THREAD_NUM = 10
