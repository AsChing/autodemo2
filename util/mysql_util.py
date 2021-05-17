# -*- coding: utf-8 -*-
"""
@Time ： 2020/7/22 14:29
@Auth ： Ching
@File ：mysql_util.py
@IDE ：PyCharm
@Desc ：--- 封装数据库操作
"""
from pymysql import connect, cursors, OperationalError
import configparser as cparser
from log import my_log


class MySQLUtil(object):
    logger = my_log.Logger('../log/log/error.log', level='error').logger

    def __init__(self):
        # --------- 读取config.ini配置文件 ---------------
        cf = cparser.ConfigParser()
        cf.read("../config/config.ini", encoding='UTF-8')
        db_config = eval(cf.get("mysql", "db_config"))
        db_config['cursorclass'] = cursors.DictCursor
        try:
            # 连接数据库
            self.conn = connect(**db_config)
            self.cursor = self.conn.cursor()
        except OperationalError as e:
            self.logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 查询数据
    def my_select(self, select_sql):
        self.conn.ping()
        self.cursor.execute(select_sql)
        data = self.cursor.fetchall()
        return data

    # 新增、更新、删除数据
    def add_update_delete(self, my_sql):
        # with self.conn.cursor() as cursor:
        #     # 取消表的外键约束
        #     cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        self.conn.ping()
        self.cursor.execute(my_sql)
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        # else:
        #     self.conn.commit()

    def __del__(self):
        self.conn.close()
        self.cursor.close()


if __name__ == '__main__':
    with MySQLUtil() as mysql:
        sql = "select title,source_id from lab_model_auction where id < 10"
        data1 = mysql.my_select(sql)
        print(type(data1))
        print(data1)
