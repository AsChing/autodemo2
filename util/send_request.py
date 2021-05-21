# -*- coding: utf-8 -*-
"""
@Time ： 2020/7/23 14:53
@Auth ： Ching
@File ：send_request.py
@IDE ：PyCharm
@Desc ：--- 
"""
import requests
import json
from log import my_log
from autodemo.config.public_data import HEADERS


class HttpClient(object):
    logger = my_log.Logger('../log/log/all.log', level='debug').logger
    error_log = my_log.Logger('../log/log/error.log', level='error').logger

    def my_request(self, ip, apiData, **kwargs):
        try:
            # Excel中获取参数传递
            # 请求方法 post/get/update...
            method = apiData["method"]
            # 请求链接
            url = ip+apiData["url"]
            # 请求参数
            if apiData["params"] == "":
                params = None
            else:
                params = apiData["params"]
            # 请求头
            if apiData["headers"] == "":
                header = HEADERS
            else:
                header = eval(apiData["headers"])
            if apiData["cookies"] == "":
                cookies = None
            else:
                cookies = {x.split('=')[0]: x.split('=')[1] for x in apiData["cookies"].split('; ')}
            # 请求体
            if apiData["body"] == "":
                body_data = None
            else:
                body_data = eval(apiData["body"])
            if method == "post":
                # 请求体类型 data/json/url
                type1 = apiData["type"]
                if type1.lower() == "data":
                    response = self.__post(url=url, data=json.dumps(body_data), headers=header, **kwargs)
                    return response
                elif type1.lower() == "json":
                    response = self.__post(url=url, data=json.dumps(body_data), params=params, headers=header, **kwargs)
                    return response
                elif type1.lower() == "cookie":
                    response = self.__post(url=url, data=json.dumps(body_data), headers=header, cookies=cookies, **kwargs)
                    return response
                else:
                    self.logger.warning("---------------------------------请求格式{0}不支持----------------------------------".format(type1))
            elif method.lower() == "get":
                # print(params)
                # params = "token=eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyODcxIiwic3ViIjoiMTU1MjMzIiwiaWF0IjoxNjIwMjg2MTEwLCJyb2xlcyI6WyLnrqHnkIblkZjnlKjmiLciXSwiYXV0aG9yaXRpZXMiOltdLCJob3N0Ijoid3d3LnljemNqay5jb206ODAiLCJ1dWlkIjoiNmYwOTMwZDYtYWI5Yi00NjU3LWFmNmUtZjJkN2MwMDIzZTZlIiwiZXhwaXJlIjoxNjI4Njk3NTk5LCJleHAiOjE2MjAzNzI1MTB9.454MKbW3dpPXQrOneLiU4YxOH8m1zWnlsWmbFnQzsk0"
                # print(params)
                response = self.__get(url=url, params=params, headers=header, **kwargs)
                return response
            else:
                self.logger.warning("---------------------------------暂不支持{0}请求方法----------------------------------".format(method))
        except Exception as e:
            self.error_log.error("请求报错了---", e)

    def __post(self, url, data=None, params=None, headers=None, cookies=None, **kwargs):
        self.logger.info("--------------------------->{0}<---------------------------".format("post请求"))
        response = requests.post(url, data=data, params=params, headers=headers, cookies=cookies).json()
        return response

    def __get(self, url, params=None, **kwargs):
        self.logger.info("--------------------------->{0}<---------------------------".format("get请求"))
        response = requests.get(url, params=params, **kwargs).json()
        return response

# from util.read_excel import ReadExcel
# from autodemo.config.public_data import *
#
# if __name__ == "__main__":
#     hc = HttpClient()
#     headers = '{"Content-Type": "application/json;charset=UTF-8"}'
#     # dat = '{"token":"eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4MzkiLCJzdWIiOiIxNzYwNjUyNTk3NSIsImlhdCI6MTU5NTkwODI0NCwicm9sZXMiOlsi566h55CG5ZGY55So5oi3Il0sImF1dGhvcml0aWVzIjpbXSwiaG9zdCI6IjE3Mi4xOC4yNTUuMjUxOjgwIiwidXVpZCI6Ijk0YzQ0ZmZkLTFhN2UtNDhiMi04MGEwLWQzMDg5YTA2YjdiNCIsImV4cGlyZSI6MTYwMjE3Mjc5OSwiZXhwIjoxNTk1OTk0NjQ0fQ.IxbHFgd-6OKiEfFRzvLoUhEL_3FCFouPO4Gf6k7v_0o","page": "1"}'
#     # res = hc.request("get", "http://172.18.255.251:8588/yc/monitor/bankruptcy/list", "url", dat, headers)
#     # print(res.json())
#
#     # data = '{"username": "17606525975", "password": "B49UhVDmrDJJ4jD+9IeWbH5rWZmdfBR+2ICkt/Q2EYOq5CIsRRYu4hhdYzVWTKxiiGS312ycg550jX9f/NBWFB4JjqsKqOCHO3drB4AQHqsnRc66UwgE3mPW7rn/mezqjrSCdXmlwH+lBkEG2k4w27iKXx8ohNl/s6T+/UC1jdk="}'
#     # re = hc.request("post", "http://172.18.255.251:8588/api/auth/login", "form", data, headers)
#     # print(re.json())
#
#     testdata = ReadExcel(FILE_PATH, u"Sheet1").read_data()
#     for data in testdata:
#         res = hc.request("http://172.18.255.251:8588", data)
#         print(res)

