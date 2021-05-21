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
from autodemo.config.public_data import TOKEN

val = {"isRead": "false", "url": "/yc/monitor/court/subrogation/list-count", "method":"get","headers":"","body":"","params":{"222":"bbb"}}
# # params = {"token": "TOKEN"}
# val["params"] = "TOKEN"
# token ="eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyODcxIiwic3ViIjoiMTU1MjMzIiwiaWF0IjoxNjIwMjg2MTEwLCJyb2xlcyI6WyLnrqHnkIblkZjnlKjmiLciXSwiYXV0aG9yaXRpZXMiOltdLCJob3N0Ijoid3d3LnljemNqay5jb206ODAiLCJ1dWlkIjoiNmYwOTMwZDYtYWI5Yi00NjU3LWFmNmUtZjJkN2MwMDIzZTZlIiwiZXhwaXJlIjoxNjI4Njk3NTk5LCJleHAiOjE2MjAzNzI1MTB9.454MKbW3dpPXQrOneLiU4YxOH8m1zWnlsWmbFnQzsk0"
token = TOKEN
# params = {}
# params["token"] = token
# val["params"] = str(params)

# val["params"]["token"] = token
# print(val)
# res = send_request.HttpClient().request("https://www.yczcjk.com", val)
# res = requests.get("https://www.yczcjk.com/yc/monitor/court/subrogation/list-count", val).text

# data = {
# "mobile": "90909090909",
# "name": "9090",
# "passwd": "999999"
# }
# jsondata = {
# 	"Host": "172.18.255.8:8601",
# 	"Content-Length": "75",
# 	"Content-Type": "application/json;charset=UTF-8",
# 	"Cookie": " versionUpdate=false; firstLogin=false; userName=15990184842; token=eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxMTIxIiwic3ViIjoiMTU5OTAxODQ4NDIiLCJpYXQiOjE2MjEzMzA4MDQsInJvbGVzIjpbIueuoeeQhuWRmOeUqOaItyJdLCJhdXRob3JpdGllcyI6W10sImhvc3QiOiIxNzIuMTguMjU1Ljg6ODAiLCJ1dWlkIjoiMTE0ZTNhOTMtYWQ0NS00ZTRiLWE2NzYtMjZmNjU2M2Q2ZjE3IiwiZXhwaXJlIjoxNjI2MzY0Nzk5LCJleHAiOjE2MjE0MTcyMDR9.kUgUHYAMrn_VfvwTnulFIx_trrtMmTEpOUNZo0lH790; SESSION=NjUxNmIwOWMtZmYzNi00ODBkLWI0NTMtNzViY2E4ZTNmNGMy"
# }
#
# req = requests.post("http://172.18.255.8:8601/api/asset/admin/check/userCreate", data=data, json=jsondata).json()
# print(req)

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


import requests
import json

url = 'http://172.18.255.8:8601/api/asset/admin/check/userCreate'
headers = {
    'Content-Type': 'application/json;charset=UTF-8'
}
c = 'versionUpdate=false; firstLogin=false; userName=15990184842; token=eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxMTIxIiwic3ViIjoiMTU5OTAxODQ4NDIiLCJpYXQiOjE2MjEzMzA4MDQsInJvbGVzIjpbIueuoeeQhuWRmOeUqOaItyJdLCJhdXRob3JpdGllcyI6W10sImhvc3QiOiIxNzIuMTguMjU1Ljg6ODAiLCJ1dWlkIjoiMTE0ZTNhOTMtYWQ0NS00ZTRiLWE2NzYtMjZmNjU2M2Q2ZjE3IiwiZXhwaXJlIjoxNjI2MzY0Nzk5LCJleHAiOjE2MjE0MTcyMDR9.kUgUHYAMrn_VfvwTnulFIx_trrtMmTEpOUNZo0lH790; SESSION=YmZmZGE4NDUtMjYwMy00OWM3LWI1ZWQtOWU3NDY2ZjhkYjcz'
cookies = {x.split('=')[0]: x.split('=')[1] for x in c.split('; ')}
post_data = {"name": "77", "mobile": "77777777777", "password": "kQFWwuzagMsrtuv4KexJ6g=="}
response = requests.post(url, headers=headers, data=json.dumps(post_data), cookies=cookies).json()
print(response)

# import requests
#
# url = "http://172.18.255.8:8601/api/asset/admin/check/userCreate"
#
# payload="{\"name\":\"77\",\"mobile\":\"77777777777\",\"password\":\"kQFWwuzagMsrtuv4KexJ6g==\"}"
# headers = {
#   'Proxy-Connection': 'keep-alive',
#   'Pragma': 'no-cache',
#   'Cache-Control': 'no-cache',
#   'Accept': 'application/json, text/plain, */*',
#   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
#   'Content-Type': 'application/json;charset=UTF-8',
#   'Origin': 'http://172.18.255.8:8601',
#   'Accept-Language': 'zh-CN,zh;q=0.9',
#   'Cookie': 'versionUpdate=false; firstLogin=false; userName=15990184842; token=eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxMTIxIiwic3ViIjoiMTU5OTAxODQ4NDIiLCJpYXQiOjE2MjEzMzA4MDQsInJvbGVzIjpbIueuoeeQhuWRmOeUqOaItyJdLCJhdXRob3JpdGllcyI6W10sImhvc3QiOiIxNzIuMTguMjU1Ljg6ODAiLCJ1dWlkIjoiMTE0ZTNhOTMtYWQ0NS00ZTRiLWE2NzYtMjZmNjU2M2Q2ZjE3IiwiZXhwaXJlIjoxNjI2MzY0Nzk5LCJleHAiOjE2MjE0MTcyMDR9.kUgUHYAMrn_VfvwTnulFIx_trrtMmTEpOUNZo0lH790; SESSION=NjUxNmIwOWMtZmYzNi00ODBkLWI0NTMtNzViY2E4ZTNmNGMy'
# }
#
# response = requests.request("POST", url, headers=headers, data=payload)
#
# print(response.text)
