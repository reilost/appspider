# -*- coding: utf-8 -*-
# @Time    : 2018/1/13 17:19
# @Author  : ddvv
# @Site    : https://www.bangcle.com/
# @File    : douyin2Spider.py
# @Software: PyCharm


import scrapy
from appspider.spiders.douyinspider.douyincore import *
from appspider.commonapis import *

'''
app: 抖音短视频
备注：爬取首页-附近接口的数据
     目前尚未分析清楚是怎么定位的。
'''

CONST_INFO = {
    'app_name': 'com.ss.android.ugc.aweme',
    'app_version': '1.6.2',
    'spider_author': 'ddvv'
}

class douyin2Spider(scrapy.Spider):
    # 设置爬虫名称
    name = "douyin2Spider"

    host = 'http://aweme.snssdk.com'
    path = '/aweme/v1/nearby/feed/?'

    header = {
        'Cache-Control': 'max-stale=10',
        'Host': 'aweme.snssdk.com',
        'Cookie': 'qh[360]=1; install_id=22634572655; ttreq=1$3375933f15c3efe431fc2ea5b9bffa9f9b1a38a2',
        'User-Agent': 'okhttp/3.8.1',
        'Connection': 'close'
    }
    base_param = {'_rticket': 1515835388867, 'ac': 'wifi', 'aid': '1128', 'app_name': 'aweme',
                   'channel': 'aweGW', 'count': 20,
                   'device_brand': 'HUAWEI', 'device_id': '46408460323', 'device_platform': 'android',
                   'device_type': 'HUAWEI+NXT-AL10', 'dpi': '480', 'feed_style': '1', 'iid': '22634572655',
                   'language': 'zh', 'manifest_version_code': '166', 'max_cursor': 0, 'min_cursor': '0',
                   'openudid': '3f4f9a09bd6ea55e', 'os_api': '23', 'os_version': '6.0', 'resolution': '1080*1812',
                   'retry_type': 'retry_http', 'ssmix': 'a', 'ts': 1515835388, 'update_version_code': '1662',
                   'uuid': '863336037384660', 'version_code': '166', 'version_name': '1.6.6'}

    def start_requests(self):
        sig = calcSig()
        custom_param = self.base_param
        self.has_more = 1
        self.exit_code = 1
        logger.info(self.name + ' start working')
        while 1:
            _rticket = int(round(time.time() * 1000))
            ts = int(round(_rticket / 1000))
            custom_param['_rticket'] = _rticket
            custom_param['ts'] = ts
            base_url = self.host + self.path + dict2str(custom_param)
            full_url = sig.work(base_url, ts)

            logger.info(self.name + ' url ' + full_url)
            yield scrapy.Request(url=full_url,
                                 headers=self.header,
                                 # meta={'proxy':'http://172.16.200.200:8888'},
                                 callback=self.parseList)
            if 'min_cursor' in custom_param.keys():
                custom_param.pop('min_cursor')
            if self.has_more == 0 or self.exit_code == 0:
                break

    def parseList(self, response):
        try:
            js = json.loads(response.body.decode())
            status_code = js['status_code']
            if js['status_code'] == 0:
                self.has_more = js['has_more']
                item = setappspideritem('AppSpider-0003-002', 'json', js, **CONST_INFO)
                yield item
            elif status_code == 2145:
                logger.warning('请求已过期')
                self.exit_code = 0
            elif status_code == 2151:
                logger.warning('签名错误')
                self.exit_code = 0
            elif status_code == 2154:
                logger.warning('请求太频繁，设备被禁')
                self.exit_code = 0
            else:
                logger.warning(response.body.decode())
                self.exit_code = 0
        except Exception as e:
            logger.error(str(e))
