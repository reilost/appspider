# -*- coding: utf-8 -*-
# @Time    : 30/01/2018 4:23 PM
# @Author  : ddvv
# @Site    : 
# @File    : setItems.py
# @Software: PyCharm

from flatten_json import flatten
from auxScripts.common import logger


def setItems(cols, datas):
    values = []
    for data in datas:
        tmp = flatten(data)
        value = {}
        for col in cols:
            try:
                value[col] = tmp[col]
            except Exception as e:
                value[col] = '**unknown**'
        values.append(value)
    return values

def main():
    setItems()

if __name__ == "__main__":
    main()