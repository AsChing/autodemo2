# -*- coding: utf-8 -*-
"""
@Time ： 2020/8/6 11:11
@Auth ： Ching
@File ：report_action.py
@IDE ：PyCharm
@Desc ：--- 
"""
import unittest
from BeautifulReport import BeautifulReport
from action import runcase
from util import send_email
from autodemo.config.public_data import *

'''
# suite方式组织测试用例
'''
# 定义一个测试集合
suite = unittest.TestSuite()
# 把写的用例加进来（将RunTest类）加进来
suite.addTest(unittest.makeSuite(runcase.RunTest))
# 实例化BeautifulReport模块
run = BeautifulReport(suite)
run.report(filename='测试报告', description='测试demo', report_dir=HTML_REPORT_PATH)
# 发送邮件
send_email.Email().sendemail()
