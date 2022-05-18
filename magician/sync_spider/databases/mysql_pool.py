# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    Author: qinLess
    File: mysql_pool.py
    Time: 2021/4/22 上午12:41
-------------------------------------------------
    Change Activity: 2021/4/22 上午12:41
-------------------------------------------------
    Desc: 
"""

import pymysql
from DBUtils.PooledDB import PooledDB
from warnings import filterwarnings

filterwarnings('error', category=pymysql.Warning)


class MysqlHandler(object):

    def __init__(self, config, spider):

        self.log = spider.logger
        self.config = config

        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=0,
            mincached=5,
            maxcached=5,
            maxshared=3,
            blocking=True,
            maxusage=None,
            setsession=[],
            ping=0,
            host=self.config['host'],
            port=self.config['port'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['db'],
            charset=self.config['charset']
        )

    def get_pool(self):
        conn = self.pool.connection()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cur

    def execute(self, sql, info_data=None):
        conn, cur = self.get_pool()
        try:
            if isinstance(info_data, dict):
                cur.execute(sql, info_data)
            elif isinstance(info_data, list):
                cur.executemany(sql, info_data)
            else:
                cur.execute(sql)

            sql_id = cur.lastrowid
            conn.commit()
            return sql_id

        except pymysql.err.IntegrityError as e:
            self.log.error(f'pymysql.err.IntegrityError.e  : {e}')
            self.log.error(f"pymysql.err.IntegrityError.sql: {sql}")
            return False

        except Exception as e:
            if '1062, "Duplicate entry ' in str(e):
                self.log.error(f'Duplicate entry.e  : {e}')

            else:
                self.log.error(f'mysql db      : {e}')
                self.log.error(f"execute failed: {sql}")

            return False

        finally:
            cur.close()
            conn.close()

    def insert_dict(self, table_name, info_dict, ignore=False, replace=False):
        fs = ','.join(list(map(lambda x: '`' + x + '`', [*info_dict.keys()])))
        vs = ','.join(list(map(lambda x: '%(' + x + ')s', [*info_dict.keys()])))

        sql = f"insert into `{table_name}` ({fs}) values ({vs});"
        if ignore:
            sql = f"insert ignore into `{table_name}` ({fs}) values ({vs});"
        elif replace:
            sql = f"replace into {table_name} ({fs}) values ({vs});"

        try:
            return self.execute(sql, info_dict)

        except Exception as e:
            self.log.exception(f'insert_dict.mysql db: {e}')
            self.log.error(f'insert_dict.failed: {sql}\t{str(info_dict.values())}')

    def insert_list(self, table_name, info_list, ignore=False, replace=False):
        keys = list(info_list[0].keys())
        fs = ', '.join(keys)
        vs = ', '.join(list(map(lambda x: '%(' + x + ')s', keys)))

        sql = f"insert into {table_name} ({fs}) values ({vs});"
        if ignore:
            sql = f"insert ignore into {table_name} ({fs}) values ({vs});"
        elif replace:
            sql = f"replace into {table_name} ({fs}) values ({vs});"

        try:
            return self.execute(sql, info_list)
        except Exception as e:
            self.log.exception(f'insert_list.mysql db: {e}')

    def select(self, sql):
        execute_res = []
        conn, cur = self.get_pool()

        try:
            if isinstance(sql, list):
                for i in sql:
                    cur.execute(i)
                    result = cur.fetchall()
                    execute_res.append(result)
                    conn.commit()

            else:
                cur.execute(sql)
                execute_res = cur.fetchall()
                conn.commit()

        finally:
            conn.close()
            cur.close()
            return execute_res

    def close_pool(self):
        self.pool.close()
