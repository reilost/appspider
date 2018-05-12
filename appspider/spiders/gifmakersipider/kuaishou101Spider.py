# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 10:47
# @Author  : ddvv
# @Site    : https://www.bangcle.com/
# @File    : kuaishou101Spider.py
# @Software: PyCharm


import scrapy
from appspider.spiders.gifmakersipider.gifmakercore import *
from appspider.commonapis import *

CONST_INFO = {
    'app_name': 'com.smile.gifmaker',
    'app_version': 'unkown',
    'spider_author': 'ddvv'
}


class kuaishou101Spider(scrapy.Spider):
    # 设置爬虫名称
    name = "kuaishou101Spider"
    header = {
        'User-Agent': 'kwai-android',
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'api.gifshow.com'
    }

    # lat, lon
    url_param = {'app': '0', 'appver': '5.4.7.5589', 'c': '360APP', 'country_code': 'cn',
                 'did': 'ANDROID_3f4f9a09bd6ea55e', 'ftt': '', 'iuid': '', 'language': 'zh-cn', 'lat': 0, 'lon': 0,
                 'max_memory': '384', 'mod': 'HUAWEI(HUAWEI%20NXT-AL10)', 'net': 'WIFI', 'oc': 'UNKNOWN',
                 'sys': 'ANDROID_6.0', 'ud': '0', 'ver': '5.4'}
    # count, id, page, type
    post_param = {'client_key': '3c2cd3f3', 'coldStart': 'false', 'count': '20', 'id': 1, 'os': 'android',
                  'page': 1, 'pcursor': '', 'pv': 'false', 'refreshTimes': '1',
                  'type': '7'}

    host = 'http://api.gifshow.com'
    path = '/rest/n/feed/hot?'

    def start_requests(self):
        custom_param = self.url_param
        post_param = self.post_param
        page = 0
        logger.info(self.name + ' start.')
        while page < 1000:
            page += 1
            custom_param['lon'] = 116.382148
            custom_param['lat'] = 39.901457
            url = self.host + self.path + dict2str(custom_param)
            post_param['page'] = page
            post_param['id'] = page % 100
            tmp_post_data = dict2str(post_param)
            post_data = sign_gifshow(url, tmp_post_data)
            yield scrapy.Request(url=url,
                                 headers=self.header,
                                 method='POST',
                                 body=post_data,
                                 # meta={'proxy': 'http://172.16.200.200:8888'},
                                 callback=self.parseList)
            logger.info(self.name + ' url ' + url)
        logger.info(self.name + ' finished.')

    def parseList(self, response):
        try:
            js = json.loads(response.body.decode())
            item = setappspideritem('AppSpider-0005-001', 'json', js, **CONST_INFO)
            yield item
        except Exception as e:
            logger.error(str(e))
