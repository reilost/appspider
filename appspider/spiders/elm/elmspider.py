# -*- coding: utf-8 -*-
# @Time    : 2018/5/3 23:38
# @Author  : ddvv
# @Site    :
# @File    : elmspider.py
# @Software: PyCharm

"""
第三方依赖库: 无
功能:
    1. 获取店铺列表
    2. 获取菜品价格
消息说明:
    1. "Bang-0001-001" : 店铺列表
    2. "Bang-0001-002" : 菜品价格
"""

import json
import hashlib
import scrapy
from appspider.commonapis import *

CONST_INFO = {
    'app_name': 'me.ele',
    'app_version': '5.0.2',
    'spider_author': 'ddvv'
}


class ElmSpider(scrapy.Spider):
    """
    饿了么爬虫
    """
    name = 'ElmSpider'

    # 爬虫入口，发起请求
    def start_requests(self):
        """

        """
        # header = {
        #     'Cache-Control': 'no-cache',
        #     'User-Agent': 'Rajax/1 HUAWEI_NXT-AL10/NXT-AL10 Android/6.0 Display/NXT-AL10C00B386 Eleme/7.20 ID/c7fc544a-7b7c-3d6e-aec3-54976dfd6637; KERNEL_VERSION:3.10.90-g01f8576 API_Level:23 Hardware:64877422432b78f996a0bcbc7c32ce92',
        #     'X-DeviceInfo': 'aW1laTo4NjMzMzYwMzczODQ2NjAgc2VyaWFsOkNKTDVUMTZBMjgwMTE3ODkgYW5kcm9pZF9pZDozZjRmOWEwOWJkNmVhNTVlIGJyYW5kOkhVQVdFSSBtb2RlbDpIVUFXRUlfTlhULUFMMTAgbmV0d29ya09wZXJhdG9yOjQ2MDExIG1hY0FkZHJlc3M6MDJfMDBfMDBfMDBfMDBfMDAgbmV0VHlwZTpXSUZJIHNpbVNlcmlhbE51bWJlcjo4OTg2MDMxNTA0MDI4ODc3MTc1OCBzaW1TdGF0ZTo1IGxhdGl0dWRlOjMwLjUzNDI3NyBsb25naXR1ZGU6MTA0LjA1ODcxMSBjaWQ6MTYyMjAgbGFjOjExIHdpZmlMaXN0OjBjXzcyXzJjX2NhX2I4Xzc0LDY0XzNhX2IxX2Q1XzRmXzcyLDM4X2FkXzhlXzlhX2E2X2QzLDM4X2FkXzhlXzlhX2E2X2Q1LDZjXzU5XzQwXzUwX2M1Xzg0LDk4XzJmXzNjXzQwXzJhXzdhLDY0XzA5XzgwXzZlX2NjX2I0LDM0X2NlXzAwXzdjXzFiXzk1LDAwXzZiXzhlX2U3XzdkX2MwLDgwXzg5XzE3XzBiX2JjX2JjIGhhdmVCbHVldG9vdGg6dHJ1ZSB0cmFja19pZDogbWVtb3J5OjI0NjEgZW5lcmd5X3BlcmNlbnQ6ODAgZmlyc3Rfb3BlbjoxNTA3NDUwODAzIGxhc3Rfb3BlbjoxNTI1MzYwOTQ2IG5ldF90eXBlOldJRkkgaGFyZHdhcmVfaWQ6NjQ4Nzc0MjI0MzJiNzhmOTk2YTBiY2JjN2MzMmNlOTI=',
        #     'X-Shard': 'loc=104.0590999647975,30.53091986104846',
        #     'X-Eleme-RequestID': '0E3E63600D134A01B0025910B1A9452A|1525361658282',
        #     'Host': 'restapi.ele.me',
        #     'Connection': 'close',
        #     'Accept-Encoding': 'gzip, deflate',
        #     'Cookie': 'track_id=1507450835%7Cdd65f73d4bfaead45474f9793a76b2f7b4c5de7a3a248243f8%7Cc176aecb51d9e75e9670fecf11737f80; _utrace=c25cd6313974f755e0672296b932bc6a_2017-10-08; SID=Qr1uqTt9uXoJhxPAk2rhwQ10ABYI0Aadz1rg'
        # }
        header = {
            'Host': 'restapi.ele.me'
        }
        # 获取分类
        url_t = 'https://restapi.ele.me/shopping/v3/restaurants?extras[]=activities&extras[]=identification&latitude=30.53091986104846&longitude=104.0590999647975&city_id=14&rank_id=0f2f16d1e3a941ad9b54f97acb1be9e9&network=WIFI&network_operator=46011&weather_code=CLOUDY&extra_filters=home&deivce=HUAWEI%20NXT-AL10&os=Android/6.0&offset={offset}&limit=20'
        for offset in range(20, 60, 20):
            url = url_t.format(offset=offset)
            yield scrapy.Request(url=url,
                                 headers=header,
                                 method='GET',
                                 meta={'proxy': 'https://192.168.2.119:8888'},
                                 callback=self.parse_list)

    # 解析返回值，推送至pipeline
    @staticmethod
    def parse_list(response):
        """

        :param response: 爬取的数据返回值。
        """
        try:
            js = json.loads(response.body.decode())
            recordlist = js['items']
            count = len(recordlist)
            if 0 != count:
                item = setbangcleitem('Bang-001-001', 'json', js, **CONST_INFO)
                yield item
        except Exception as e:
            logger.error(str(e))

