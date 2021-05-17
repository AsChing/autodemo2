# -*- coding: utf-8 -*-
"""
@Time ： 2020/11/3 14:11
@Auth ： Ching
@File ：runcase.py
@IDE ：PyCharm
@Desc ：--- 
"""

import unittest, ddt
from autodemo.config.public_data import *
from util import send_request, read_excel, write_excel, oracle_util, mysql_util
import configparser as cparser
from log import my_log


@ddt.ddt
class RunTest(unittest.TestCase):
    logger = my_log.Logger('../log/log/all.log', level='debug').logger
    select_data = read_excel.ReadExcel(FILE_PATH, u"查询").read_data()
    add_data = read_excel.ReadExcel(FILE_PATH, u"新增").read_data()
    update_data = read_excel.ReadExcel(FILE_PATH, u"修改").read_data()
    delete_data = read_excel.ReadExcel(FILE_PATH, u"删除").read_data()

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self) -> None:
        self.logger.info("----每个测试case运行之前运行----")

    def tearDown(self) -> None:
        self.logger.info("----每个测试case运行完之后执行----\n")

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger.info("----必须使用@classmethod装饰器, 所有case运行之前只运行一次----")
        cf = cparser.ConfigParser()
        cf.read("../config/config.ini", encoding='UTF-8')
        cls.ip = cf.get("ip", "business_ip")
        if DATATYPE == "ORACLE":
            cls.data_type = oracle_util.Oracle()
        else:
            cls.data_type = mysql_util.MySQL()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.logger.info("----必须使用@classmethod装饰器, 所有case运行完之后只运行一次----")

    @ddt.data(*select_data)
    def test01_get_data(self, data):
        if data is None:
            self.logger.warning("~~~~~~~~~~~~~~~~~~~~没有查询测到试数据~~~~~~~~~~~~~~~~~")
        else:
            if data["params"] == "":
                params = {}
                params["token"] = TOKEN
                data["params"] = str(params)
            # data["headers"] = HEADERS
            res = send_request.HttpClient().my_request(self.ip, data)
            if res["code"] == int(data["pre"]):
                result = "PASS"
                if res["code"] == 200:
                    sql = data["sql"]
                    sql_result = self.data_type.my_select(sql)
                    if len(sql_result) != res["data"]["total"]:
                        result = "FAIL"
                        self.assertEqual(len(sql_result), res["data"]["total"], "查询 --------- 用例{0}测试不通过，与预期返回结果总量不一致".format(data["casenum"]))
            else:
                result = "FAIL"
            write_excel.WriteExcel(REPORT_FILE_PATH, "查询").write_data(data['row'], result, str(res))
            self.assertEqual(res["code"], int(data["pre"]), "查询 --------- 用例{0}测试不通过,与预期返回code不一致".format(data["casenum"]))

    @ddt.data(*add_data)
    def test02_add_user(self, data):
        if data is None:
            print("~~~~~~~~~~~~~~~~~~~~没有查询到测试数据~~~~~~~~~~~~~~~~~")
        else:
            if data["params"] == "":
                params = {}
                params["token"] = TOKEN
                data["params"] = str(params)
            res = send_request.HttpClient().my_request(self.ip, data)
            if res["code"] == int(data["pre"]):
                result = "PASS"
                sql = data["sql"]
                sql_result = self.data_type.my_select(sql)
                if len(sql_result) != 1:
                    result = "FAIL"
                    self.assertEqual(len(sql_result), 1, "新增 --------- 用例{0}测试不通过，新增失败".format(data["casenum"]))
                # if res["code"] == 200:
                #     if len(sql_result) != 1:
                #         result = "FAIL"
                #         self.assertEqual(len(sql_result), 1, "新增 --------- 用例{0}测试不通过，新增失败".format(data["casenum"]))
                # else:
                #     if res["message"] == "新增失败,工号已存在!":
                #         if len(sql_result) != 1:
                #             result = "FAIL"
                #             self.assertEqual(len(sql_result), 1, "新增 --------- 用例{0}测试不通过，新增失败".format(data["casenum"]))
            else:
                result = "FAIL"
            write_excel.WriteExcel(REPORT_FILE_PATH, "新增").write_data(data['row'], result, str(res))
            self.assertEqual(res["code"], int(data["pre"]), "新增 --------- 用例{0}测试不通过,与预期返回code不一致".format(data["casenum"]))

    @ddt.data(*update_data)
    def test03_get_data(self, data):
        if data is None:
            print("~~~~~~~~~~~~~~~~~~~~没有查询到测试数据~~~~~~~~~~~~~~~~~")
        else:
            if data["params"] == "":
                params = {}
                params["token"] = TOKEN
                data["params"] = str(params)
            res = send_request.HttpClient().my_request(self.ip, data)
            if res["code"] == int(data["pre"]):
                result = "PASS"
                if res["code"] == 200:
                    sql = data["sql"]
                    sql_result = self.data_type.my_select(sql)
                    if len(sql_result) != 1:
                        result = "FAIL"
                        self.assertEqual(len(sql_result), 1, "新增 --------- 用例{0}测试不通过，新增失败".format(data["casenum"]))
            else:
                result = "FAIL"
            write_excel.WriteExcel(REPORT_FILE_PATH, "修改").write_data(data['row'], result, str(res))
            self.assertEqual(res["code"], int(data["pre"]), "更新 --------- 用例{0}测试不通过,与预期返回code不一致".format(data["casenum"]))

    @ddt.data(*delete_data)
    def test04_get_data(self, data):
        if data is None:
            print("~~~~~~~~~~~~~~~~~~~~没有查询到测试数据~~~~~~~~~~~~~~~~~")
        else:
            if data["params"] == "":
                params = {}
                params["token"] = TOKEN
                data["params"] = str(params)
                print(data)
            res = send_request.HttpClient().my_request(self.ip, data)
            if res["code"] == int(data["pre"]):
                result = "PASS"
                if res["code"] == 200:
                    sql = data["sql"]
                    sql_result = self.data_type.my_select(sql)
                    if len(sql_result) != 0:
                        result = "FAIL"
                        self.assertEqual(len(sql_result), 0, "新增 --------- 用例{0}测试不通过，新增失败".format(data["casenum"]))
            else:
                result = "FAIL"
            # writeexcel.WriteExcel(REPORT_FILE_PATH, "删除").write_data(data['row'], result, str(res))
            self.assertEqual(res["code"], int(data["pre"]), "删除 --------- 用例{0}测试不通过,与预期返回code不一致".format(data["casenum"]))


if __name__ == '__main__':
    unittest.main()
