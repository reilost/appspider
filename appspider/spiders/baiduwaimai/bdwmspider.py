# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 11:21
# @Author  : ddvv
# @Site    : 
# @File    : bdwmspider.py
# @Software: PyCharm

"""
第三方依赖库: 无
功能:
    1. 获取店铺列表
    2. 获取菜品价格
消息说明:
    1. "AppSpider-0002-001" : 店铺列表
    2. "AppSpider-0002-002" : 菜品价格
"""

import json
import scrapy
from appspider.commonapis import *

CONST_INFO = {
    'app_name': 'com.baidu.lbs.waimai',
    'app_version': '3.8.1',
    'spider_author': 'ddvv'
}


class BaiduWMSpider(scrapy.Spider):
    """
    百度爬虫
    """
    name = 'BaiduWMSpider'

    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'client.waimai.baidu.com',
        'User-Agent': 'okhttp/3.2.0',
        'Cookie': 'WMST=1525835459; BAIDUID=C7906451BBA82A1EAE4C9F174866CA6C:FG=1; '
                  'WMID=da6ff461c2d6ebcb3aaabfda45cd82f9 '
    }

    # 爬虫入口，发起请求
    def start_requests(self):
        """

        """
        # 获取分类
        burl = 'http://client.waimai.baidu.com/shopui/na/v1/cliententry?resid=1001&from=na-android&os=7.0&sv=3.8.1' \
               '&cuid=D95EE2BA0EEE849BB92E5447923A9027%7C066483730633368&model=HUAWEINXT-AL10&screen=1080*1812' \
               '&channel=com.xiazaiyewaimai&loc_lat=2560675.81&loc_lng=1.268400692E7&city_id=340&address=%E8%85%BE%E8' \
               '%AE%AF%E5%A4%A7%E5%8E%A6&net_type=wifi&isp=46011&request_time={request_time}'
        post_data = 'lat=2560675.81&lng=1.268400692E7&count=20&page={page}&bduss=NA&stoken=bdwm&sortby=&taste=&city_id=340' \
                    '&promotion=&return_type=refresh '
        for page in range(1, 5):
            request_time = int(round(time.time() * 1000))
            url = burl.format(request_time=request_time)
            data = post_data.format(page=page)
            yield scrapy.Request(url=url,
                                 headers=self.header,
                                 method='POST',
                                 body=data,
                                 # meta={'proxy': 'http://172.16.104.31:8888'},
                                 callback=self.parse_list)

    # 解析返回值，推送至pipeline
    def parse_list(self, response):
        """

        :param response: 爬取的数据返回值。
        """
        try:
            js = json.loads(response.body.decode())
            shops_info = js['result']['shop_info']
            count = len(shops_info)
            if 0 != count:
                item = setappspideritem('AppSpider-0002-001', 'json', js, **CONST_INFO)
                yield item
                yield from self.getdetail(shops_info)
        except Exception as e:
            logger.error(str(e))

    def getdetail(self, shops_info):
        burl = 'http://client.waimai.baidu.com/shopui/na/v1/shopmenu?resid=1001&from=na-android&os=7.0&sv=3.8.1&cuid' \
               '=D95EE2BA0EEE849BB92E5447923A9027%7C066483730633368&model=HUAWEINXT-AL10&screen=1080*1812&channel=com' \
               '.xiazaiyewaimai&loc_lat=2560675.81&loc_lng=1.268400692E7&city_id=340&address=%E8%85%BE%E8%AE%AF%E5%A4' \
               '%A7%E5%8E%A6&net_type=wifi&isp=46011&utm_source=waimai&utm_medium=shoplist&utm_content=default' \
               '&utm_term=default&utm_campaign=default&cid=988272&request_time={request_time}'
        post_data = 'lat=2560675.81&lng=1.268400692E7&shop_id={shop_id}&bduss=NA&stoken=bdwm&key=O%255CFTSTDTT%255CMX%2521W3%252F%2523%2525N%255B%2521%2526O%255EUPBXV%2526O%2528VS5.P%25273TTRN%2511S%255DN%255DPWEXRWEXUQDWSPD%255DQTF%255DTT'
        for shop_info in shops_info:
            shop_id = shop_info['shop_id']
            request_time = int(round(time.time() * 1000))
            url = burl.format(request_time=request_time)
            data = post_data.format(shop_id=shop_id)
            yield scrapy.Request(url=url,
                                 headers=self.header,
                                 method='POST',
                                 body=data,
                                 # meta={'proxy': 'http://172.16.104.31:8888'},
                                 callback=self.parse_detail)

    def parse_detail(self, response):
        try:
            js = json.loads(response.body.decode())
            takeout_menu = js['result']['takeout_menu']
            count = len(takeout_menu)
            if 0 != count:
                item = setappspideritem('AppSpider-0002-002', 'json', js, **CONST_INFO)
                yield item
        except Exception as e:
            logger.error(str(e))
