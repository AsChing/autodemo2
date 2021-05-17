# -*- coding: utf-8 -*-
"""
@Time ： 2021/5/6 15:26
@Auth ： Ching
@File ：1111.py
@IDE ：PyCharm
@Desc ：--- 
"""
from util import send_request
import requests

val = {"isRead": "false", "url": "/yc/monitor/court/subrogation/list-count", "method":"get","headers":"","body":"","params":{"222":"bbb"}}
# # params = {"token": "TOKEN"}
# val["params"] = "TOKEN"
token ="eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyODcxIiwic3ViIjoiMTU1MjMzIiwiaWF0IjoxNjIwMjg2MTEwLCJyb2xlcyI6WyLnrqHnkIblkZjnlKjmiLciXSwiYXV0aG9yaXRpZXMiOltdLCJob3N0Ijoid3d3LnljemNqay5jb206ODAiLCJ1dWlkIjoiNmYwOTMwZDYtYWI5Yi00NjU3LWFmNmUtZjJkN2MwMDIzZTZlIiwiZXhwaXJlIjoxNjI4Njk3NTk5LCJleHAiOjE2MjAzNzI1MTB9.454MKbW3dpPXQrOneLiU4YxOH8m1zWnlsWmbFnQzsk0"

# params = {}
# params["token"] = token
# val["params"] = str(params)

val["params"]["token"] = token
print(val)
# res = send_request.HttpClient().request("https://www.yczcjk.com", val)
# res = requests.get("https://www.yczcjk.com/yc/monitor/court/subrogation/list-count", val).text
# print(res)

# data1 = ["1a", "2b", "3c"]
#
# @data(data1)
# def test_value(self, data1):
#     for i in data1:
#         if i == "1a":
#             data1[0] = 111
#             self.flag = 222
#             print(data1)
#             # sys.exit(0)
#             raise _ShouldStop
#         else:
#             data1[1] = self.flag
#     print(1111111)
#     # for i in range(len(data1)):
#     #     print(i)
#     # print(data1)
#
# info = [(1, 2), (3, 4)]
#
# @data((1, 2), (3, 4))
# @unpack
# def test_add01(self, *args):
#     print("-----")
#     print(*args)
#
#     val = {
#         "a": "1", "b": "2"
#     }
#     val1 = {
#         "c": "3"
#     }
#     print({**val, **val1})
#
# @data(*info)
# @unpack
# # 下边用例会执行两次/解包
# def test_add02(self, num1, num2):
#     print(num1 + num2)


'''
# 使用discover方式组织测试用例
'''
# "."表示当前目录，"*demo.py"匹配当前目录下所有demo.py结尾的用例
# suite_tests = unittest.defaultTestLoader.discover("../action", pattern="*demo.py", top_level_dir=None)
# # log_path='.'把report放到当前目录下
# BeautifulReport(suite_tests).report(filename='测试报告aa', description='测试demo', log_path='.')


'''
# 运行指定测试类中的case，suite方式组织测试用例
'''
# 仅运行指定的case　RunTest是类名，test01_login是类中的测试方法名
# caseList = [Music("test05")]
# # 使用suite组织测试用例
# suite = unittest.TestSuite()
# suite.addTests(caseList)
# # 运行并生成测试报告
# run = BeautifulReport(suite)
# run.report(filename="测试报告bb", description="测试demo")