# -*- coding: utf-8 -*-
"""
@Time ： 2020/11/3 14:11
@Auth ： Ching
@File ：runcase.py
@IDE ：PyCharm
@Desc ：--- 
"""

import unittest, ddt
from autodemo.config.public_data import DATATYPE, TOKEN, FILE_PATH, REPORT_FILE_PATH
from util import send_request, read_excel, write_excel, oracle_util, mysql_util, code_deal
import configparser as cparser
from log import my_log


@ddt.ddt
class RunTest(unittest.TestCase):
    logger = my_log.Logger('../log/log/all.log', level='debug').logger
    select_data = read_excel.ReadExcel(FILE_PATH, u"Sheet2").read_data()
    # add_data = read_excel.ReadExcel(FILE_PATH, u"新增").read_data()
    # update_data = read_excel.ReadExcel(FILE_PATH, u"修改").read_data()
    # delete_data = read_excel.ReadExcel(FILE_PATH, u"删除").read_data()

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def setUp(self) -> None:
        self.logger.info("==========================----测试case开始----==========================\n")

    def tearDown(self) -> None:
        self.logger.info("==========================----测试case结束----==========================\n")

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger.info("-=============================---必须使用@classmethod装饰器, 所有case运行之前只运行一次--======================--")
        cf = cparser.ConfigParser()
        cf.read("../config/config.ini", encoding='UTF-8')
        cls.ip = cf.get("ip", "auction_ip")
        if DATATYPE == "ORACLE":
            cls.data_type = oracle_util.OracleUtil()
        else:
            cls.data_type = mysql_util.MySQLUtil()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.logger.info("-===========================---必须使用@classmethod装饰器, 所有case运行完之后只运行一次--===========================--")

    @ddt.data(*select_data)
    def test_case_01(self, data):
        # data中没数据则提示
        if data is None or data == []:
            self.logger.warning("================没有查询到数据================")
        else:
            # 参数params设置，没有其他参数则只放入token
            if data["type"].lower() != "cookie":
                if data["params"] == "":
                    data["params"] = str("token=" + TOKEN)
                else:
                    data["params"] = str(data["params"] + "&token=" + TOKEN)
            res = send_request.HttpClient().my_request(self.ip, data)
            self.logger.info("=========响应结果中code为：" + str(res["code"]))
            self.logger.info("=========预期结果中code为：" + str(int(data["pre"])))
            if res["code"] == int(data["pre"]):
                result = "PASS"
                # 用例中sql、可断言字段取出
                sql = data["sql"]
                field = data['field']
                code_type = data['code_type']
                pre_value = data['pre_value']
                # 有sql语句则断言sql语句执行结果与接口返回结果
                if sql != '':
                    sql_result = self.data_type.my_select(sql)
                    # 如果需要数据库某个字段与预期值对比，可以在pre_value中添加预期值
                    if pre_value != '':
                        self.logger.info("=========数据库查询结果中为：" + str(sql_result[0][0]))
                        self.logger.info("=========预期数据库查询结果为：" + str(pre_value))
                        write_excel.WriteExcel(REPORT_FILE_PATH, "Sheet2").write_data(data['row'], result, str(res))
                        self.assertEqual(str(sql_result[0][0]), str(pre_value),  "查询 --------- 用例{0}测试不通过，与预期返回结果总量不一致".format(data["casenum"]))
                    # 如果field字段有值，进行响应结果字段校验
                    if field != '':
                        # 如果code_type是all，则比对接口返回的list中某一条记录
                        if code_type == 'all':
                            actual_res = eval(field)
                            # 接口返回的为键值对，处理成只有值方便与数据查询结果做比对
                            # 数据库查询结果为tuple，处理成tuple方便比对,调用写的方法deal处理数据
                            tuple1 = code_deal.CodeDeal().deal(actual_res)
                            # 预期结果与实际结果比较
                            if str(sql_result[0]) != str(tuple1):
                                result = "FAIL"
                            self.logger.info("响应结果中为：" + str(tuple1))
                            self.logger.info("预期结果中为：" + str(sql_result[0]))
                            write_excel.WriteExcel(REPORT_FILE_PATH, "Sheet2").write_data(data['row'], result, str(res))
                            self.assertEqual(str(sql_result[0]), str(tuple1), "查询 --------- 用例{0}测试不通过，与预期返回结果总量不一致".format(data["casenum"]))
                        else:
                            # eval执行field得到实际结果
                            actual_res = str(eval(field))
                            # 预期结果与实际结果比较
                            if str(sql_result[0][0]) != actual_res:
                                result = "FAIL"
                            self.logger.info("=======响应结果中为：" + actual_res)
                            write_excel.WriteExcel(REPORT_FILE_PATH, "Sheet2").write_data(data['row'], result, str(res))
                            self.logger.info("=======预期结果中为：" + str(sql_result[0][0]))
                            self.assertEqual(str(sql_result[0][0]), actual_res, "查询 --------- 用例{0}测试不通过，与预期返回结果总量不一致".format(data["casenum"]))
            else:
                result = "FAIL"
                # 无sql语句则直接断言code，结束
                write_excel.WriteExcel(REPORT_FILE_PATH, "Sheet2").write_data(data['row'], result, str(res))
                self.logger.info("用例" + str(data["casenum"]) + "执行结果为：" + str(res["code"] == int(data["pre"])))
                self.assertEqual(res["code"], int(data["pre"]), "用例{0}测试不通过,与预期返回code不一致".format(data["casenum"]))

    # @ddt.data(*select_data)
    # def test01_get_data(self, data):
    #     if data is None:
    #         self.logger.warning("~~~~~~~~~~~~~~~~~~~~没有查询测到试数据~~~~~~~~~~~~~~~~~")
    #     else:
    #         if data["params"] == "":
    #             params = {}
    #             params["token"] = TOKEN
    #             data["params"] = str(params)
    #         # data["headers"] = HEADERS
    #         res = send_request.HttpClient().my_request(self.ip, data)
    #         if res["code"] == int(data["pre"]):
    #             result = "PASS"
    #             if res["code"] == 200:
    #                 sql = data["sql"]
    #                 sql_result = self.data_type.my_select(sql)
    #                 if len(sql_result) != res["data"]["total"]:
    #                     result = "FAIL"
    #                     self.assertEqual(len(sql_result), res["data"]["total"], "查询 --------- 用例{0}测试不通过，与预期返回结果总量不一致".format(data["casenum"]))
    #         else:
    #             result = "FAIL"
    #         write_excel.WriteExcel(REPORT_FILE_PATH, "查询").write_data(data['row'], result, str(res))
    #         self.assertEqual(res["code"], int(data["pre"]), "查询 --------- 用例{0}测试不通过,与预期返回code不一致".format(data["casenum"]))
    #
    # @ddt.data(*add_data)
    # def test02_add_user(self, data):
    #     if data is None:
    #         print("~~~~~~~~~~~~~~~~~~~~没有查询到测试数据~~~~~~~~~~~~~~~~~")
    #     else:
    #         if data["params"] == "":
    #             params = {}
    #             params["token"] = TOKEN
    #             data["params"] = str(params)
    #         res = send_request.HttpClient().my_request(self.ip, data)
    #         if res["code"] == int(data["pre"]):
    #             result = "PASS"
    #             sql = data["sql"]
    #             sql_result = self.data_type.my_select(sql)
    #             if len(sql_result) != 1:
    #                 result = "FAIL"
    #                 self.assertEqual(len(sql_result), 1, "新增 --------- 用例{0}测试不通过，新增失败".format(data["casenum"]))
    #         else:
    #             result = "FAIL"
    #         write_excel.WriteExcel(REPORT_FILE_PATH, "新增").write_data(data['row'], result, str(res))
    #         self.assertEqual(res["code"], int(data["pre"]), "新增 --------- 用例{0}测试不通过,与预期返回code不一致".format(data["casenum"]))
    #
    # @ddt.data(*update_data)
    # def test03_get_data(self, data):
    #     if data is None:
    #         print("~~~~~~~~~~~~~~~~~~~~没有查询到测试数据~~~~~~~~~~~~~~~~~")
    #     else:
    #         if data["params"] == "":
    #             params = {}
    #             params["token"] = TOKEN
    #             data["params"] = str(params)
    #         res = send_request.HttpClient().my_request(self.ip, data)
    #         if res["code"] == int(data["pre"]):
    #             result = "PASS"
    #             if res["code"] == 200:
    #                 sql = data["sql"]
    #                 sql_result = self.data_type.my_select(sql)
    #                 if len(sql_result) != 1:
    #                     result = "FAIL"
    #                     self.assertEqual(len(sql_result), 1, "新增 --------- 用例{0}测试不通过，新增失败".format(data["casenum"]))
    #         else:
    #             result = "FAIL"
    #         write_excel.WriteExcel(REPORT_FILE_PATH, "修改").write_data(data['row'], result, str(res))
    #         self.assertEqual(res["code"], int(data["pre"]), "更新 --------- 用例{0}测试不通过,与预期返回code不一致".format(data["casenum"]))
    #
    # @ddt.data(*delete_data)
    # def test04_get_data(self, data):
    #     if data is None:
    #         print("~~~~~~~~~~~~~~~~~~~~没有查询到测试数据~~~~~~~~~~~~~~~~~")
    #     else:
    #         if data["params"] == "":
    #             params = {}
    #             params["token"] = TOKEN
    #             data["params"] = str(params)
    #             print(data)
    #         res = send_request.HttpClient().my_request(self.ip, data)
    #         if res["code"] == int(data["pre"]):
    #             result = "PASS"
    #             if res["code"] == 200:
    #                 sql = data["sql"]
    #                 sql_result = self.data_type.my_select(sql)
    #                 if len(sql_result) != 0:
    #                     result = "FAIL"
    #                     self.assertEqual(len(sql_result), 0, "新增 --------- 用例{0}测试不通过，新增失败".format(data["casenum"]))
    #         else:
    #             result = "FAIL"
    #         # writeexcel.WriteExcel(REPORT_FILE_PATH, "删除").write_data(data['row'], result, str(res))
    #         self.assertEqual(res["code"], int(data["pre"]), "删除 --------- 用例{0}测试不通过,与预期返回code不一致".format(data["casenum"]))


if __name__ == '__main__':
    unittest.main()
