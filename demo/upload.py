# -*- coding: utf-8 -*-
"""
@Time ： 2021/5/11 14:28
@Auth ： Ching
@File ：upload.py
@IDE ：PyCharm
@Desc ：--- 
"""

import requests

HOST = "http://127.0.0.1:80"
fileUpload_path = "/user/doUpload"
fileUpload_data = {
    "file": ("窗口.png", open("../../static/images/窗口.png", "rb"), "image/png")
}


class FileUpload:
    def __init__(self, path, indata):
        self.url = f'{HOST}{path}'
        self.headers = {
            "Content-Type": "multipart/form-data",
        }
        self.payload = indata
        self.response = requests.post(self.url, files=self.payload)

    def get_response_json(self):
        return self.response.json()


fileUpload = FileUpload(fileUpload_path, fileUpload_data)
print(fileUpload.get_response_json())