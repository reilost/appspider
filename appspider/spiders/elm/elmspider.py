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
    1. "AppSpider-0001-001" : 店铺列表
    2. "AppSpider-0001-002" : 菜品价格
# -*- coding: utf-8 -*-
# @Time    : ${DATE} ${TIME}
# @Author  : ddvv
# @Site    : ${SITE}
# @File    : ${NAME}.py
# @Software: ${PRODUCT_NAME}

def main() :
    pass

if __name__ == "__main__" :
    main()
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
                                 # meta={'proxy': 'https://192.168.2.119:8888'},
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
                item = setbangcleitem('AppSpider-0001-001', 'json', js, **CONST_INFO)
                yield item
        except Exception as e:
            logger.error(str(e))

