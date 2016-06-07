# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()

    link = scrapy.Field()
    review = scrapy.Field()

    # address = scrapy.Field()

    street_address = scrapy.Field()
    address_locality = scrapy.Field()
    address_region = scrapy.Field()
    postal_code = scrapy.Field()

    # email = scrapy.Field()
    phone = scrapy.Field()
    rank = scrapy.Field()

    # location_link = scrapy.Field()
    # state = scrapy.Field()

