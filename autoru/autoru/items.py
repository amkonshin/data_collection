# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import MapCompose, TakeFirst
import scrapy

def cleaner_photos(values):
    pos = values.find('//')
    link = 'http:' + values[pos:-2]

    return link
def price_clean(value):
    return int(value.replace(' ',''))
class AutoruItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photos))#input_processor=MapCompose(cleaner_photo)
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(price_clean) )
    pass
