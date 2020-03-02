# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime

class BitcointalkItem(scrapy.Item):
    subject = scrapy.Field()
    replies = scrapy.Field()
    views = scrapy.Field()
    last_post = scrapy.Field()
    topic_url = scrapy.Field()
    topic_id = scrapy.Field()
