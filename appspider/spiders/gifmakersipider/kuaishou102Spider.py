# -*- coding: utf-8 -*-
# @Time    : 2018/1/15 11:48
# @Author  : ddvv
# @Site    : https://www.bangcle.com/
# @File    : kuaishou102Spider.py
# @Software: PyCharm


import scrapy
from appspider.spiders.gifmakersipider.gifmakercore import *
from appspider.commonapis import *

CONST_INFO = {
    'app_name': 'com.smile.gifmaker',
    'app_version': 'unkown',
    'spider_author': 'ddvv'
}

'''
app: gifshow
备注：快手--附近接口爬虫
重要：这个接口是同步类型的接口，而SCRAPY框架是异步的，现在只能通过降低效率的方式来尽可能的获取不重复的数据。现在爬取一条记录大约需要4秒的时间。
'''

class kuaishou102Spider(scrapy.Spider):
    # 设置爬虫名称
    name = "kuaishou102Spider"
    header = {
        'User-Agent': 'kwai-android',
        'Accept-Language': 'zh-cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'api.gifshow.com'
    }
    # 降低效率，单线程，每个请求延迟3秒
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY':4
    }
    # lat, lon
    url_param = {'app': '0', 'appver': '5.4.8.5615', 'c': 'XIAOMI', 'country_code': 'CN',
                 'did': 'ANDROID_9070f3768be09689', 'ftt': '', 'iuid': '', 'language': 'zh-cn', 'lat': 30.53969,
                 'lon': 104.074776, 'max_memory': '256', 'mod': 'Xiaomi(MI%205)', 'net': 'WIFI', 'oc': 'XIAOMI',
                 'sys': 'ANDROID_6.0.1', 'ud': '665798801', 'ver': '5.4'}
    # count, id, page, type, refreshTimes
    post_param = {'client_key': '3c2cd3f3', 'coldStart': 'true', 'count': '20', 'id': '17', 'os': 'android',
                  'page': '3', 'refreshTimes': '1',
                  'token': '2d08fd2efcab4c2286a7e9e0c23ce083-665798801', 'type': '10'}

    host = 'http://api.gifshow.com'
    path = '/rest/n/feed/nearby?'
    pcursor = ''

    def start_requests(self):
        custom_param = self.url_param
        post_param = self.post_param
        page = 1
        logger.info(self.name + ' start.')
        while page < 1000:
            if page == 2 :
                page += 1
                continue
            custom_param['lon'] = 116.382148
            custom_param['lat'] = 39.90145
            post_param['page'] = page
            post_param['id'] = page % 100
            if page != 1 :
                post_param['pcursor'] = self.pcursor
            tmp_post_data = dict2str(post_param)
            url = self.host + self.path + dict2str(custom_param)
            post_data = sign_gifshow(url, tmp_post_data, True)
            yield scrapy.Request(url=url,
                                 headers=self.header,
                                 method='POST',
                                 body=post_data,
                                 callback=self.parseList)
            page += 1
            logger.info(self.name + ' url ' + url)
        logger.info(self.name + ' finished.')


    def parseList(self, response):
        try :
            js = json.loads(response.body.decode())
            self.pcursor = js['pcursor']
            item = setappspideritem('AppSpider-0005-002', 'json', js, **CONST_INFO)
            yield item
        except Exception as e:
            logger.error(str(e))
