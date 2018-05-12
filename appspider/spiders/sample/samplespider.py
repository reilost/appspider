# -*- coding: utf-8 -*-
# @Time    : 2018/3/15 15:38
# @Author  : ddvv
# @Site    : 
# @File    : samplespider.py
# @Software: PyCharm

"""
第三方依赖库: 无
功能:
    1. 获取《判决文书》app第一页统计数据
消息说明:
    1. "Bang-0000-000" : 分类结果
"""

import json
import hashlib
import scrapy
from appspider.commonapis import *

CONST_INFO = {
    'app_name': 'com.chongfa.panjueshu',
    'app_version': '1.0.1',
    'spider_author': 'Shuang.liu'
}


class SampleSpider(scrapy.Spider):
    """
    样例爬虫
    """
    # 爬虫名称
    name = 'SampleSpider'

    # 爬虫入口，发起请求
    def start_requests(self):
        """

        """
        header = {
            'Charset': 'UTF-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; ONEPLUS A5000 Build/LMY48Z)',
            'Host': 'api.panjueshu.com',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        # 获取分类
        post_param = 'time={t}&code={code}'
        urls = ['http://api.panjueshu.com/Verdict/GetCaseType']
        for url in urls:
            curtime = round(time.time())
            code = self._sig(t=curtime)
            post_data = post_param.format(t=curtime, code=code)
            yield scrapy.Request(url=url,
                                 headers=header,
                                 method='POST',
                                 body=post_data,
                                 # meta={'proxy': 'http://172.16.200.200:8888'},
                                 callback=self.parse_list)

    # 解析返回值，推送至pipeline
    @staticmethod
    def parse_list(response):
        """

        :param response: 爬取的数据返回值。
        """
        try:
            js = json.loads(response.body.decode())
            recordlist = js['CaseTypeList']
            count = len(recordlist)
            if 0 != count:
                item = setappspideritem('Bang-0000-000', 'json', js, **CONST_INFO)
                yield item
        except Exception as e:
            logger.error(str(e))

    # 计算校验字段
    @staticmethod
    def _sig(t, s='panjueshu.com'):
        """

        :param t: 时间戳
        :param s: 计算签名的附加字符串
        :return: 返回签名
        """
        st = str(t)
        sig_str = st[2:] + st[0:2] + s
        m = hashlib.md5()
        m.update(sig_str.encode())
        return m.hexdigest()

    def parse(self, response):
        pass
