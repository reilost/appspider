# -*- coding: utf-8 -*-
# @Time    : 2018/1/16 15:15
# @Author  : ddvv
# @Site    : https://www.bangcle.com/
# @File    : miaopai41xSpider.py
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


class miaopaixSpider(scrapy.Spider):
    # 设置爬虫名称
    name = "miaopaixSpider"
    # 首页 appid:428
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

    # cateid, ip, timestamp, lastUpdateTime, unique_id
    url_param = {'abId': '50-103', 'appName': '%E7%A7%92%E6%8B%8D', 'brand': 'Xiaomi', 'carrier': '%E6%9C%AA%E7%9F%A5',
                 'cateid': 205, 'channel': 'xiaomi_market', 'cpu': 'AArch64', 'density': '3.0',
                 'devId': '9ACD8CAC309DEC599489AD9B9F87B3B8', 'dpi': '480', 'facturer': 'Xiaomi', 'idfa': '',
                 'imei': '868930029585485', 'ip': '118.112.72.53', 'kg_udid': '477EAD89EEC8ED0869EE3D8FED7BAF14',
                 'lastUpdateTime': 1516085818576, 'mac': 'B0:E2:35:CB:DE:A4', 'model': 'MI_5', 'net': '1',
                 'network': 'WIFI', 'os': 'android', 'pName': 'com.yixia.videoeditor', 'page': '1', 'partnerId': '1',
                 'pcId': 'xiaomi_market', 'plat': 'android', 'platformId': '1', 'refresh': '1',
                 'resolution': '1080x1920', 'sessionid': '4dff62eb5fd9451d865adaf4cfcf24a3',
                 'timestamp': 1516085818679, 'token': 'SWUQk~H7wyHqsQLFDVZNJ~QuOc1UzzXi', 'type': 'up',
                 'udid': '74BC13F90575A96DD6E37CE5AC4D1D51', 'unique_id': 'fa16a817-da0f-3c6e-8ff0-d6fbb9386345',
                 'userId': 'DozcVQWmWgkGG89WKy1-Hw__', 'vApp': '65198', 'vName': '6.7.51', 'vOs': '6.0.1',
                 'vend': 'miaopai', 'version': '6.7.51', 'weiboUid': '', 'withExtend': '1'}

    host = 'http://c.miaopai.com'
    path = '/1/recommend/cateChannel.json?'

    def start_requests(self):
        header = self.header
        # 203 影视
        cateids = {410: 128, 411: 136, 412: 124, 413: 210, 414: 196, 415: 237, 416: 172, 417: 164, 418: 28, 419: 140,
                   420: 114, 421: 160, 422: 203, 423: 165, 424: 205}
        for msg_type, cateid in cateids.items():
            custom_param = self.url_param
            page = 0
            while page < 5:
                _rticket = int(round(time.time() * 1000))
                custom_param['timestamp'] = _rticket
                custom_param['lastUpdateTime'] = _rticket + 1001
                random_uuid = str(uuid.uuid4())
                custom_param['unique_id'] = random_uuid
                custom_param['cateid'] = cateid
                header['sign'] = sign(self.path[:-1], random_uuid, _rticket)
                page += 1
                custom_param['page'] = page
                url = self.host + self.path + dict2str(custom_param)
                yield scrapy.Request(url=url,
                                     headers=header,
                                     method='GET',
                                     # meta={'proxy': 'http://172.16.200.200:8888'},
                                     meta={'msg_type': msg_type, 'url': page},
                                     callback=self.parseList)
                custom_param['type'] = 'down'
                custom_param['page'] = page
                logger.debug(self.name + ' url ' + url)


    def parseList(self, response):
        try:
            js = json.loads(decodeData(response.body))
            msg_type = response.meta['msg_type']
            # url = response.meta['url']
            # for a in js['result']['list']:
            #     logger.warning(a['channel']['title'])
            # logger.warning('%s%d:%d%s' % (30 * '-', msg_type, url, 30 * '-'))
            item = setappspideritem('AppSpider-0006-{msg_type}'.format(msg_type=msg_type), 'json', js, **CONST_INFO)
            yield item
        except Exception as e:
            logger.error(str(e))
