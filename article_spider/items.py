# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    summary = scrapy.Field()
    plain_text = scrapy.Field()


class Video(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field()