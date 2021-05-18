# -*- coding: utf-8 -*-
"""
@Time ： 2021/5/18 14:10
@Auth ： Ching
@File ：code_deal.py
@IDE ：PyCharm
@Desc ：--- 
"""


class CodeDeal:

    def deal(self, actual_res):
        list1 = []
        for i in actual_res.values():
            if type(i) == str:
                if i.lower() == "true":
                    list1.append("1")
                if i.lower() == "false":
                    list1.append("0")
                else:
                    list1.append(i)
            else:
                list1.append(i)
        # 数据库查询结果为tuple，处理成tuple方便比对
        tuple1 = tuple(list1)
        return tuple1