# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnhuigovItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    source_url = scrapy.Field()
    context = scrapy.Field()
    source_publish_time = scrapy.Field()
    info_source = scrapy.Field()
