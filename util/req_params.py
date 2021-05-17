# -*- coding: utf-8 -*-
"""
@Time ： 2021/5/7 11:31
@Auth ： Ching
@File ：req_params.py
@IDE ：PyCharm
@Desc ：--- 
"""
from enum import Enum
import random
import string
import time
from copy import deepcopy


class ReqParams(Enum):
    phone_list = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    transfer_record_id = "1275"+str(random.randint(0, 99999999)).zfill(15)
    picture_id = 1390934146029309954

    发起诉讼 = {
                # "transferRecordId": "1275361916071448118",
                # "nextTransferNodeCode": "B003",
                # "businessObligorIdList": None,
                "type": 1,
                "trialRequest": {
                    "litigationType": 0,
                    "contractNumber": "HZ738722002444",
                    "verificationStyle": 1,
                    "agencyAuthority": 1,
                    # "obligorName": "吉林省地方呀666",
                    # "obligorNumber": "",
                    "obligorIds": [
                        "1275361915811401729"
                    ],
                    "agent": {
                        "agencyContactFirst": str(random.choice(phone_list)+"".join(random.choice("0123456789") for i in range(8))),
                        "agencyPersonFirst": random.choice(["小张", "小赵", "小李", "小王"])
                    },
                    "transferRecordId": "127536191607141118578",
                    "nextTransferNodeCode": "B003"
                }
            }
    待立案 = {
                "transferRecordId": transfer_record_id,
                "nextTransferNodeCode": "B006",
                "businessObligorIdList": None,
                "caseNumber": "案号A"+"".join(map(lambda x: random.choice(string.digits), range(8))),
                "court": random.choice(["第一法院", "第二法院", "第三法院", "第四法院"]),
                "filingAcceptTime": time.strftime('%Y-%m-%d %H:%M:%S'),
                "capital": round(random.uniform(0, 1000000), 2),
                "interest": round(random.uniform(0, 1000000), 2),
                "validate1": [
                    picture_id
                ],
                "caseAcceptAttach": [
                    picture_id
                ]
            }

    my_sql = "SELECT ID FROM BMS_TRANSFER_RECORD WHERE PRE_TRANSFER_RECORD_ID = '1273504454452187138'"

    aa = {
            "trialRequest":{
                "contractNumber":"HZ738722002555111111",
                "obligorIds":[
                    "127536191599595110511111"
                ],
                "nextTransferNodeCode":"B0031111"
            }
        }

    bb = {
            "nextTransferNodeCode":"B00622222",
            "caseAcceptAttach":[
                2222
            ]
        }

    # def sub_params(params, original):
    #     result = deepcopy(original)
    #     for key1, value1 in params.items():
    #         for key2, value2 in original.items():
    #             if key1 == key2:
    #                 if isinstance(value1, dict) and isinstance(value2, dict):
    #                     for key3, value3 in value1.items():
    #                         for key4 in value2:
    #                             if key3 == key4:
    #                                 result[key2][key4] = value3
    #                 else:
    #                     result[key2] = value1
    #     return result

# a = Parammm["发起诉讼"].value
# b = Parammm["aa"].value
# c = {**a, **b}
# print(a)
# print(b)
#
# print(c)
# print(Parammm["待立案"].value)


# if __name__ == '__main__':
#     pa = Parammm
#     a = Parammm["待立案"].value
#     b = Parammm["bb"].value
#     print(pa.sub_params(b, a))

# 随机整数：
# print(random.randint(1, 50))

# 随机选取0到100间的偶数：
# print random.randrange(0, 101, 2)
#
# 随机浮点数：
# print(random.random())
# print(random.uniform(1, 10))
#
# # 随机字符：
# print random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()')
#
# # 多个字符中生成指定数量的随机字符：
# print(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
#
# 从a-zA-Z0-9生成指定数量的随机字符：
# ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
# print(ran_str)
#
# # 多个字符中选取指定数量的字符组成新字符串：
# print(''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5)))
#
# # 随机选取字符串：
# print(random.choice(['剪刀', '石头', '布']))
#
# # 打乱排序
# items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
# print(random.shuffle(items))
# str1 = "".join(map(lambda x: random.choice(string.digits), range(8)))
# str2 = str(random.randint(0, 99999999)).zfill(11)
# print(str1)
# print(str2)
#
# str4 = time.strftime('%Y-%m-%d %H:%M:%S')
# print(str4)

# prelist=["130","131","132","133","134","135","136","137","138","139","147","150","151","152","153","155","156","157","158","159","186","187","188"]
# str3 = random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))
# print(str3)

# list和dict
