# -*- coding: utf-8 -*-
"""
@Time ： 2021/4/23 9:21
@Auth ： Ching
@File ：config.py.py
@IDE ：PyCharm
@Desc ：--- 
"""
from pymysql.cursors import DictCursor


DB_CONFIG = {"user":"asset","password":"Youcheng2017!","host":'172.18.255.8',"port":3306,"db":"asset_test","charset":'utf8mb4',"cursorclass": DictCursor}
