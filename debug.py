# -*- coding: utf-8 -*-
# @Time    : 11/04/2018 3:27 PM
# @Author  : ddvv
# @Site    :
# @File    : debug.py
# @Software: PyCharm

from scrapy import cmdline


def main():
    name = 'ElmSpider'
    # cmd = 'scrapy crawl {name} -L INFO -a caseTypeId=10 -a startPage=72 -a endPage=77'.format(name=name)
    cmd = 'scrapy crawl {name} -L WARNING'.format(name=name)
    cmdline.execute(cmd.split())


if __name__ == "__main__":
    main()
