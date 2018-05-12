# -*- coding: utf-8 -*-
# @Time    : 2018/1/11 17:23
# @Author  : ddvv
# @Site    : https://www.bangcle.com/
# @File    : douyin3Spider.py
# @Software: PyCharm


import scrapy
from appspider.spiders.douyinspider.douyincore import *
from appspider.commonapis import *

'''
app: douyin
备注：爬取频道接口的数据，msg_type = 3，4，5，6，7
'''
CONST_INFO = {
    'app_name': 'com.ss.android.ugc.aweme',
    'app_version': '1.6.2',
    'spider_author': 'ddvv'
}

class douyin3Spider(scrapy.Spider):
    # 设置爬虫名称
    name = "douyin3Spider"

    host = 'http://aweme.snssdk.com'
    path = '/aweme/v1/category/list/?'
    header = {
        'Cache-Control': 'max-stale=10',
        'Host': 'aweme.snssdk.com',
        'Cookie': 'qh[360]=1; install_id=22634572655; ttreq=1$3375933f15c3efe431fc2ea5b9bffa9f9b1a38a2',
        'User-Agent': 'okhttp/3.8.1',
        'Connection': 'close'
    }
    base_param = {'_rticket': 1515464298999, 'ac': 'wifi', 'aid': '1128', 'app_name': 'aweme', 'channel': 'aweGW',
                   'count': 20, 'cursor': 0, 'device_brand': 'HUAWEI', 'device_id': '46408460323',
                   'device_platform': 'android', 'device_type': 'HUAWEI+NXT-AL10', 'dpi': '480', 'iid': '22634572655',
                   'language': 'zh', 'manifest_version_code': '166', 'openudid': '3f4f9a09bd6ea55e', 'os_api': '23',
                   'os_version': '6.0', 'resolution': '1080*1812', 'retry_type': 'retry_http', 'ssmix': 'a',
                   'ts': 1515464299, 'update_version_code': '1662', 'uuid': '863336037384660', 'version_code': '166',
                   'version_name': '1.6.6'}

    cursor = 0
    has_more = 1
    exit_code = 1
    sub_has_more = 1
    sub_exit_code = 1

    def setCustomParam(self, param, cursor):
        custom_param = param
        _rticket = int(round(time.time() * 1000))
        ts = int(round(_rticket / 1000))
        custom_param['_rticket'] = _rticket
        custom_param['ts'] = ts
        custom_param['cursor'] = cursor

        return custom_param


    def getFullURL(self, host, url, custom_param):
        sig = calcSig()
        base_url = host + url + dict2str(custom_param)
        full_url = sig.work(base_url, custom_param['ts'])

        return full_url

    def start_requests(self):
        logger.info(self.name + ' start working')
        while 1:
            custom_param = self.setCustomParam(self.base_param, self.cursor)
            full_url = self.getFullURL(self.host, self.path, custom_param)

            logger.info(self.name + ' url ' + full_url)
            yield scrapy.Request(url=full_url,
                                 headers=self.header,
                                 # meta={'proxy':'http://172.16.200.200:8888'},
                                 callback=self.parseList)
            if self.has_more == 0  or self.exit_code == 0:
                break

    def parseList(self, response):
        try:
            js = json.loads(response.body.decode())
            if js['status_code'] == 0:
                self.has_more = js['has_more']
                category_list = js['category_list']
                count = len(category_list)
                item = setappspideritem('AppSpider-0003-003', 'json', js, **CONST_INFO)
                self.cursor += count
                yield item
                # yield from self.subRequest(category_list)
            else:
                self.exit_code = 0
        except Exception as e:
            logger.error(str(e))

    def subRequest(self, category_list):
        for one in category_list:
            if one['desc'] == '热门挑战':
                yield from self.getChallenge(one)
            elif one['desc'] == '热门音乐':
                yield from self.getMuisc(one)

    def getChallenge(self, one):
        urls = {4: '/aweme/v1/challenge/aweme/?', 5: '/aweme/v1/challenge/fresh/aweme/?'}
        for msg_type, url in urls.items():
            id = one['challenge_info']['cid']
            yield from self.subRe(id, msg_type, url)

    def getMuisc(self, one):
        urls = {6: '/aweme/v1/music/aweme/?', 7: '/aweme/v1/music/fresh/aweme/?'}
        for msg_type, url in urls.items():
            id = one['music_info']['id']
            yield from self.subRe(id, msg_type, url)

    def subRe(self, id, msg_type, url):
        cursor = 0
        while cursor < 2000:
            custom_param = self.setCustomParam(self.base_param, cursor)
            custom_param['type'] = 5
            #custom_param['count'] = 200
            if msg_type == 4 or msg_type == 5:
                custom_param['ch_id'] = id
            elif msg_type == 6 or msg_type == 7:
                custom_param['music_id'] = id
            full_url = self.getFullURL(self.host, url, custom_param)
            logger.info(self.name + ' url ' + full_url)
            yield scrapy.Request(url=full_url,
                                 headers=self.header,
                                 # meta={'proxy':'http://172.16.200.200:8888'},
                                 # meta={'msg_type':msg_type, 'proxy':'http://172.16.200.200:8888'},
                                 callback=self.parseSubList)
            cursor += 20
            if self.sub_has_more == 0:
                break

    def parseSubList(self, response):
        try:
            js = json.loads(response.body.decode())
            msg_type = response.meta['msg_type']
            if js['status_code'] == 0:
                item = setappspideritem('AppSpider-0003-00{msg_type}'.format(msg_type=msg_type), 'json', js, **CONST_INFO)
                yield item
        except Exception as e:
            logger.error(str(e))
