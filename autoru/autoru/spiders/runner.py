from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from autoru.spiders.auto_ru import AutoRuSpider
from autoru import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AutoRuSpider)
    process.start()
