# -*- coding: utf-8 -*-
# @Time    : 11/04/2018 3:27 PM
# @Author  : ddvv
# @Site    :
# @File    : debug.py
# @Software: PyCharm

from scrapy import cmdline


def main():
    name = 'douyin2Spider'
    # cmd = 'scrapy crawl {name} -L INFO -a keyword=福记生煎'.format(name=name)
    cmd = 'scrapy crawl {name} -L WARNING'.format(name=name)
    cmdline.execute(cmd.split())


if __name__ == "__main__":
    main()
