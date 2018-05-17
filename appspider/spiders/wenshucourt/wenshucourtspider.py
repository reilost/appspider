# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 20:36
# @Author  : ddvv
# @Site    : 
# @File    : wenshucourtspider.py
# @Software: PyCharm

"""
第三方依赖库: Crypto
功能:
    1. 获取《裁判文书网》app数据
消息说明:
    1. "AppSpider-0007-001" : 分类结果
"""

import scrapy
from appspider.commonapis import *
from appspider.spiders.wenshucourt.wenshucore import *

CONST_INFO = {
    'app_name': 'com.lawyee.wenshuapp',
    'app_version': '1.1.1115',
    'spider_author': 'ddvv'
}


class WenshuCourtSpider(scrapy.Spider):
    """
    爬取中国裁判文书APP
    """
    # 爬虫名称
    name = 'WenshuCourtSpider'

    def __init__(self):
        self.header = {
            'Content-Type': 'application/json',
            'timespan': '',
            'nonce': '',
            'devid': '',
            'signature': '',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0; HUAWEI NXT-AL10 Build/HUAWEINXT-AL10)',
            'Host': 'wenshuapp.court.gov.cn',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate',
        }
        self.deviceid = 'f5fd4ccef4b0421a909bf452b64a4cda'

    # 爬虫入口，发起请求
    def start_requests(self):
        """

        """
        deviceid = self.deviceid
        header = self.header
        urls = ['http://wenshuapp.court.gov.cn/MobileServices/GetToken']
        post_param = '{"app":"cpws","devid":"%s","apptype":"1"}' % deviceid
        for url in urls:
            timespan = gettime()
            nonce = getrandomchr(4)
            sig = signature(timespan, nonce, deviceid)
            header['nonce'] = nonce
            header['signature'] = sig
            header['timespan'] = timespan
            header['devid'] = deviceid
            yield scrapy.Request(url=url,
                                 headers=header,
                                 method='POST',
                                 body=post_param,
                                 # meta={'proxy': 'http://172.16.104.31:8888'},
                                 callback=self.parse)

    # 解析返回值，推送至pipeline
    def parse(self, response):
        """

        :param response: 爬取的数据返回值。
        """
        token = ''
        try:
            js = json.loads(response.body.decode())
            token = js['token']
            item = setappspideritem('AppSpider-0007-001', 'json', js, **CONST_INFO)
            yield item
        except Exception as e:
            logger.error(str(e))

        deviceid = self.deviceid
        header = self.header
        urls = ['http://wenshuapp.court.gov.cn/MobileServices/GetAddCountAndTotalAndPVCount']
        post_param = '{"app":"cpws","reqtoken":"%s"}' % token
        for url in urls:
            timespan = gettime()
            nonce = getrandomchr(4)
            sig = signature(timespan, nonce, deviceid)
            # 这四个字段必须用小写
            header['nonce'] = nonce
            header['signature'] = sig
            header['timespan'] = timespan
            header['devid'] = deviceid
            yield scrapy.Request(url=url,
                                 headers=header,
                                 method='POST',
                                 body=post_param,
                                 meta={'timespan': timespan, 'token': token},
                                 # meta={'proxy': 'http://172.16.104.31:8888', 'timespan': timespan, 'token': token},
                                 callback=self.parse_list)

    def parse_list(self, response):
        try:
            chipher = response.body.decode()
            timespan = response.meta['timespan']
            token = response.meta['token']
            key = funs[StrToLong(token, 1) % 20](token + timespan)
            cleartext = decryptAES(key, chipher)
            item = setappspideritem('AppSpider-0007-002', 'json', cleartext, **CONST_INFO)
            yield item
        except Exception as e:
            logger.error(str(e))
