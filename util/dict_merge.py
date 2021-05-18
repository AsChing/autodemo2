# -*- coding: utf-8 -*-
"""
@Time ： 2021/5/17 10:23
@Auth ： Ching
@File ：dict_merge.py
@IDE ：PyCharm
@Desc ：--- 
"""

from copy import deepcopy


def DictMerge(params, original):
    result = deepcopy(original)
    for key1, value1 in params.items():
        for key2, value2 in original.items():
            if key1 == key2:
                if isinstance(value1, dict) and isinstance(value2, dict):
                    for key3, value3 in value1.items():
                        for key4 in value2:
                            if key3 == key4:
                                result[key2][key4] = value3
                else:
                    result[key2] = value1
    return result
