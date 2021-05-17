# -*- coding: utf-8 -*-
"""
@Time ： 2020/7/20 11:31
@Auth ： Ching
@File ：public_data.py
@IDE ：PyCharm
@Desc ：全局变量
"""

import os

# baseDir1 = os.path.dirname(__file__)
'''
 获取项目的根目录绝对路径
'''
base_dir = os.path.dirname(os.path.dirname(__file__))
# 获取测试数据文件所在绝对路径
FILE_PATH = base_dir + "/testdata/test.xlsx"
# 获取测试结果数据文件所在相对路径
REPORT_FILE_PATH = "../report/reportdata/testreport.xlsx"
HTML_REPORT_PATH = base_dir + "/report"
# test_file = base_dir + "/testdata/sourcedata/test.xlsx"

# 登陆接口密码rsa加密的key
AUCTION_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" \
                     "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDle/hFqi80v633AqkjnkZPzVu2\n" \
                     "waST+cNVe1gEcDNq6tifFpjjyfXXAEtXD8pAAv6zl0nuFFT9CSOPuAq0kdUc70vT\n" \
                     "1jxTMkK0H9iZ74pN4zTu1gsG+RrIcMHKjFFsBrF/D2dI4TJ4ZjMhcxcXuTsNHJ0q\n" \
                     "H5e2bLq6VSELhY5PzQIDAQAB\n" \
                     "-----END PUBLIC KEY-----"
BUSINESS_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" \
                      "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyaPGORSsRUC5wN6CODBp\n" \
                      "sX5e1PP8n45J+f+AK2NcRLMRQM5gPCGIv+Ol/blaqOdn4HFO6BEcMCafWCQVUwdP\n" \
                      "QzatAJ37xC74PqG/KMSCMOcZVtu2guYJgJCHLmyh2Vmks/+FLRIxxXrTVoFfg+4W\n" \
                      "rURrgo6CXTTIqbH1ImA+zoMH9g8lCEK2bBPrzm8qXbIN2Y5Q7v1oNyKoVSUOo/RN\n" \
                      "iRNHqDqELuc1EyOR/AVpL5d/CNq81I5SePW3Kc0vPohjV+95VS/qY50QGA+AAhU9\n" \
                      "2Nbok8sfjid/lxQUxU6inGGvl7fj6+NMm6kO4WrkGcAwwP/YCnJ3Qoe6J3YUVO7c\n" \
                      "0wIDAQAB\n" \
                      "-----END PUBLIC KEY-----"

HEADERS = {"Content-Type": "application/json;charset=UTF-8"}

TOKEN = 'eyJuYW1lIjoiY2NjMSIsImFsZyI6IkhTMjU2In0.eyJqdGkiOiIxMjczNTAxNjM0NjcxOTM5NTg1Iiwic3ViIjoiY2NjIiwiaWF0IjoxNjIwNjE0Nzk3LCJpcCI6IjE3Mi4xOC4yNTUuMTMzIiwiZXhwIjoxNjIwODczOTk3fQ.2snunpRTzhGz2htq6ulEkXuauopkcpaVrKZ5K77VUeM'
DATATYPE = "ORACLE"