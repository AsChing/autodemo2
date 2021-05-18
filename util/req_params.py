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
            "trialRequest": {
                "contractNumber": "HZ738722002555111111",
                "obligorIds": [
                    "127536191599595110511111"
                ],
                "nextTransferNodeCode": "B0031111"
            }
        }

    bb = {
            "nextTransferNodeCode": "B00622222",
            "caseAcceptAttach": [
                2222
            ]
        }
