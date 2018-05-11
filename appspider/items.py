# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rid = scrapy.Field()
    date = scrapy.Field()
    app_name = scrapy.Field()
    app_version = scrapy.Field()
    spider_author = scrapy.Field()
    msg_type = scrapy.Field()
    data_type = scrapy.Field()
    data = scrapy.Field()
    pass
