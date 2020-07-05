# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst      #Подключаем обраотчики

def cleaner_params(value):
    return value.strip()

def int_price(price):
    try:
        return int(price.replace(" ", ""))
    except:
        return price


class LeroymerlinItem(scrapy.Item):

    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    params = scrapy.Field(input_processor=MapCompose(cleaner_params))
    price = scrapy.Field(input_processor=MapCompose(int_price))
    link = scrapy.Field()
