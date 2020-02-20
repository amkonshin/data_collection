# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class JobruSpider(scrapy.Spider):
    name = 'jobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.xpath("//a[contains(@class, 'icMQ_ _1QIBo')]/@href").extract()
        print(vacansy)
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/child::text()").extract_first()
        salary = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']//child::text()").extract()
        link=response.url
        source='superjob.ru'
        print(name, salary)
        yield JobparserItem(name=name,salary=salary,link=link,source=source)


