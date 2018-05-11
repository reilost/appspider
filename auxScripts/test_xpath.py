# -*- coding: utf-8 -*-
# @Time    : 2018/5/11 0:49
# @Author  : ddvv
# @Site    : 
# @File    : test_xpath.py
# @Software: PyCharm

from lxml import etree

def main():
    f = open('../3.html', 'r', encoding='utf8')
    ht = f.read()
    f.close()
    tree = etree.HTML(ht)
    nodes = tree.xpath('//div[@id="hd-porn-dload"]/table/tr[last()]/td[2]/a/@href')
    # nodes = tree.xpath('//div[@class="mb"]/a/@href')
    # //*[@id="hd-porn-dload"]/table/tbody/tr[3]/td[2]/a
    print(nodes)


if __name__ == "__main__":
    main()