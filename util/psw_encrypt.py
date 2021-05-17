# -*- coding: utf-8 -*-
"""
@Time ： 2020/7/22 14:16
@Auth ： Ching
@File ：psw_encrypt.py
@IDE ：PyCharm
@Desc ：--- 接口种密码加密
"""
import base64
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA


def PswEncrpt(public_key, password):
    try:
        rsa_key = RSA.importKey(public_key)
        cipher = Cipher_pksc1_v1_5.new(rsa_key)
        cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
        result = cipher_text.decode()
        return result
    except Exception as e:
        raise e
