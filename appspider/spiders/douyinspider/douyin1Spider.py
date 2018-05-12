# -*- coding: utf-8 -*-
# @Time    : 2018/1/9 15:52
# @Author  : ddvv
# @Site    : https://www.bangcle.com/
# @File    : douyin1Spider.py
# @Software: PyCharm


import scrapy
from appspider.spiders.douyinspider.douyincore import *
from appspider.commonapis import *

'''
app: 抖音短视频
备注：爬取首页-推荐接口的数据
'''

CONST_INFO = {
    'app_name': 'com.ss.android.ugc.aweme',
    'app_version': '1.6.2',
    'spider_author': 'ddvv'
}

class douyin1Spider(scrapy.Spider):
    name = "douyin1Spider"

    host = 'http://aweme.snssdk.com'
    path = '/aweme/v1/feed/?'
    header = {
        'Cache-Control': 'max-stale=10',
        'Host': 'aweme.snssdk.com',
        'Cookie': 'qh[360]=1; install_id=22634572655; ttreq=1$3375933f15c3efe431fc2ea5b9bffa9f9b1a38a2',
        'User-Agent': 'okhttp/3.8.1',
        'Connection': 'close'
    }

    base_param = {'_rticket': 1515461857142, 'ac': 'wifi', 'aid': '1128', 'app_name': 'aweme',
                  'channel': 'aweGW', 'count': 20,
                  'device_brand': 'HUAWEI', 'device_id': '46408460320', 'device_platform': 'android',
                  'device_type': 'HUAWEI+NXT-AL10', 'dpi': '480', 'iid': '22634572655', 'language': 'zh',
                  'manifest_version_code': 166, 'max_cursor': 0, 'min_cursor': 0, 'openudid': '3f4f9a09bd6ea55e',
                  'os_api': '23', 'os_version': '6.0', 'resolution': '1080*1812', 'retry_type': 'retry_http',
                  'ssmix': 'a', 'ts': 1515461857, 'type': '0', 'update_version_code': '1662',
                  'uuid': '863336037384660', 'version_code': '166', 'version_name': '1.6.6', 'volume': '0.0'}

    def setCustomParam(self, param, cursor):
        custom_param = param
        _rticket = int(round(time.time() * 1000))
        ts = int(round(_rticket / 1000))
        custom_param['_rticket'] = _rticket
        custom_param['ts'] = ts
        custom_param['cursor'] = cursor

        return custom_param

    def getFullURL(self, host, path, custom_param):
        sig = calcSig()
        base_url = host + path + dict2str(custom_param)
        full_url = sig.work(base_url, custom_param['ts'])

        return full_url

    def start_requests(self):
        logger.info(self.name + ' start working')
        count = 0
        self.exit_code = 0
        while 1:
            custom_param = self.setCustomParam(self.base_param, 0)
            full_url = self.getFullURL(self.host, self.path, custom_param)

            yield scrapy.Request(url=full_url,
                                 headers=self.header,
                                 # meta={'proxy':'http://172.16.200.200:8888'},
                                 callback=self.parseList)
            logger.debug(self.name + ' url ' + full_url)
            count += 1
            # 一次最多可以连续发送120个请求。 超过120个需要等待一段时间才能继续发送，并获取到返回值。
            if self.exit_code != 0 :
                break
            if count >= 120:
                count = 0
                logger.info(self.name + ' sleep 10s')
                time.sleep(30)

    def parseList(self, response):
        try:
            js = json.loads(response.body.decode())
            status_code = js['status_code']
            if status_code == 0:
                item = setappspideritem('AppSpider-0003-001', 'json', js, **CONST_INFO)
                yield item
            elif status_code == 2145:
                logger.warning('请求已过期')
                self.exit_code = 2145
            elif status_code == 2151:
                logger.warning('签名错误')
                self.exit_code = 2151
            elif status_code == 2154:
                logger.warning('请求太频繁，设备被禁')
                self.exit_code = 2154
            else:
                logger.warning(response.body.decode())
                self.exit_code = 2100
        except Exception as e:
            logger.error(str(e))
