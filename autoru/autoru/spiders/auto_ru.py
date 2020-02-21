# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from autoru.items import AutoruItem
from scrapy.loader import ItemLoader

class AutoRuSpider(scrapy.Spider):
    name = 'auto_ru'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva/avtomobili/genesis?radius=0&q=audi+q3']
#https://auto.ru/moskva/cars/genesis/all/?query=gene&from=searchline
    def parse(self, response: HtmlResponse):
        ads_links = response.xpath("//a[@class='snippet-link']/@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AutoruItem(), response=response)
        loader.add_xpath('name', "//span[@class='title-info-title-text']/child::text()")
        loader.add_xpath('price', "//span[@class='js-item-price']/child::text()")
        loader.add_xpath('photos', "//span[@class='gallery-list-item-link']/@style")
        yield loader.load_item()
        # name = response.xpath("//span[@class='title-info-title-text']/child::text()").extract_first()
        # price=response.xpath("//span[@class='js-item-price']/child::text()").extract_first()
        # photos=response.xpath("//span[@class='gallery-list-item-link']/@style").extract()
        # photos = response.xpath('//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url').extract()
        # price = response.xpath('//span[@class="js-item-price"][1]/text()').extract_first()
        #yield AvitoparserItem(name=name, photos = photos, price = price)
        #print(name)
        #print(price)
