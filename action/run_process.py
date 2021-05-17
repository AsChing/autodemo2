
import unittest, requests
from unittest.case import _ShouldStop
import json
from ddt import ddt, data, unpack
from util import write_excel, read_excel, req_params, dict_merge
from autodemo.config.public_data import TOKEN, HEADERS, FILE_PATH, REPORT_FILE_PATH
from log import my_log


@ddt
class MyTestCase(unittest.TestCase):
    ip = "http://172.18.255.8:8011"
    logger = my_log.Logger('../log/log/all.log', level='debug').logger
    litigation = read_excel.ReadExcel(FILE_PATH).read_data()

    @data(litigation)
    def test_litigation(self, test_data):
        self.logger.info("测试用例数据长度： ", len(test_data))
        if test_data is None or test_data == []:
            self.logger.warning('{}{}'.format(self.get_now_datetime('%Y-%m-%d %H:%M:%S'), '------暂未读取到有效测试用例-----'))
        else:
            for datai in test_data:
                params = {"token": TOKEN}
                original = req_params.ReqParams[datai["CASE"]].value  # 初始所有参数
                body = eval(datai["body"])  # 需要填写的参数
                result = dict_merge.DictMerge(body, original)
                res = requests.post(url=self.ip+datai["URL"], data=json.dumps(result), params=params, headers=HEADERS).json()
                if res["code"] == 200:
                    write_excel.WriteExcel(REPORT_FILE_PATH).write_somewhere(datai['row'], "PASS", str(res))
                    self.logger.info("流程 --------- 用例{0}测试通过".format(datai["casenum"]))
                else:
                    self.logger.info("实际返回code： ", res)
                    write_excel.WriteExcel(REPORT_FILE_PATH).write_somewhere(datai['row'], "FAIL", str(res))
                    self.logger.warning("流程 --------- 用例{0}测试不通过，流程类接口终止测试~~~~~".format(datai["casenum"]))
                    raise _ShouldStop
                # self.assertEqual(res["code"], 200, "流程 --------- 用例{0}测试不通过,与预期返回code不一致".format(datai["casenum"]))


if __name__ == '__main__':
    unittest.main()
