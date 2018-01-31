# -*- coding: utf-8 -*-
# @Time    : 30/01/2018 4:24 PM
# @Author  : ddvv
# @Site    : 
# @File    : common.py
# @Software: PyCharm

import json
import logging

format = '%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s'
logging.basicConfig(filename='postgre2mysql.log',
                    format=format,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger('*** ddvv log ***')

# 读取模板json
def readFiles(filename):
    with open('../datas/' + filename, 'r') as f:
        txt = f.read()
    js = json.loads(txt)
    return js

def main():
    pass


if __name__ == "__main__":
    main()