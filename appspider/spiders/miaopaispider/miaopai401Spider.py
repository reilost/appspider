# -*- coding: utf-8 -*-
# @Time    : 2018/1/16 9:40
# @Author  : ddvv
# @Site    : https://www.bangcle.com/
# @File    : miaopai401Spider.py
# @Software: PyCharm

import uuid
import scrapy
from appspider.spiders.miaopaispider.miaopaicore import *
from appspider.commonapis import *


CONST_INFO = {
    'app_name': 'com.yixia.videoeditor',
    'app_version': '6.7.51',
    'spider_author': 'ddvv'
}

class miaopai1Spider(scrapy.Spider):
    # 设置爬虫名称
    name = "miaopai1Spider"
    # 直播 appid:428
    header = {
        'appid': '428',
        'kg_udid': '477EAD89EEC8ED0869EE3D8FED7BAF14',
        'sessionid': '84555f172fd45b65ab7a7b522bca0bab',
        'udid': '74BC13F90575A96DD6E37CE5AC4D1D51',
        'sign': 'bd98212d2fa41dfc19f12848eb89c56e',
        'User-Agent': 'Miaopai/6.7.51/65198/xiaomi_market(Xiaomi_MI_5_23)',
        'Accept-Language': 'zh-Hans',
        'Host': 'c.miaopai.com'
    }

    # lat, lon
    url_param = {'abId': '50-103', 'appName': '%E7%A7%92%E6%8B%8D', 'brand': 'Xiaomi', 'carrier': '%E6%9C%AA%E7%9F%A5',
                 'cateid': '-1', 'channel': 'xiaomi_market', 'columns': '2', 'cpu': 'AArch64', 'density': '3.0',
                 'devId': '9ACD8CAC309DEC599489AD9B9F87B3B8', 'dpi': '480', 'extend': '1', 'facturer': 'Xiaomi',
                 'idfa': '', 'imei': '868930029585485', 'ip': '119.6.97.143',
                 'kg_udid': '477EAD89EEC8ED0869EE3D8FED7BAF14', 'mac': 'B0:E2:35:CB:DE:A4', 'model': 'MI_5', 'net': '1',
                 'network': 'WIFI', 'os': 'android', 'pName': 'com.yixia.videoeditor', 'page': 1, 'partnerId': '1',
                 'pcId': 'xiaomi_market', 'per': '20', 'plat': 'android', 'platformId': '1', 'resolution': '1080x1920',
                 'sessionid': '84555f172fd45b65ab7a7b522bca0bab', 'timestamp': 1516066556189, 'token': '',
                 'type': 'news', 'udid': '74BC13F90575A96DD6E37CE5AC4D1D51',
                 'unique_id': 'fa16a817-da0f-3c6e-8ff0-d6fbb9386345', 'userId': '', 'vApp': '65198', 'vName': '6.7.51',
                 'vOs': '6.0.1', 'vend': 'miaopai', 'version': '6.7.51', 'weiboUid': ''}

    host = 'http://c.miaopai.com'
    path = '/1/yzb/livelist.json?'

    def start_requests(self):
        custom_param = self.url_param
        header = self.header
        page = 0
        while page < 500 :
            _rticket = int(round(time.time() * 1000))
            custom_param['timestamp'] = _rticket
            random_uuid = str(uuid.uuid4())
            custom_param['unique_id'] = random_uuid
            header['sign'] = sign(self.path[:-1], random_uuid, _rticket)
            page += 1
            custom_param['page'] = page
            url = self.host + self.path + dict2str(custom_param)
            yield scrapy.Request(url=url,
                                 headers=header,
                                 method='GET',
                                 # meta={'proxy': 'http://172.16.200.200:8888'},
                                 callback=self.parseList)
            logger.debug(self.name + ' url ' + url)

    def parseList(self, response):
        try:
            js = json.loads(decodeData(response.body))
            count = js['result']['count']
            if 0 != count:
                item = setappspideritem('AppSpider-0006-001', 'json', js, **CONST_INFO)
                yield item
        except Exception as e:
            logger.debug(str(e))
