from pprint import pprint
from lxml import html
import requests
from datetime import date
from pymongo import MongoClient
client= MongoClient('localhost',27017)
db=client['News']
lenta=db.lenta
yandex=db.yandex
newsmail=db.newsmail

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
def request_to_lenta():
        try:

            response = requests.get('https://lenta.ru/', headers=header)
            root = html.fromstring(response.text)
            new_block = root.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']")
            for block in new_block:
                dict={}
                dict['text'] = block.xpath("./a/child::text()")[0].replace('\xa0', ' ')
                dict['link'] = 'https://lenta.ru/' + block.xpath("./a/@href")[0]
                dict['date'] = block.xpath("./a/time/@datetime")
                dict['source']='Nan'

                lenta.insert_one(dict)

            return True
        except:
            print('Error')


def request_to_yandex():
    try:

        response = requests.get('https://yandex.ru/news/', headers=header)
        root = html.fromstring(response.text)
        news = root.xpath("//div[@class='stories-set stories-set_main_no stories-set_pos_1']//tr/td")
        for elem in news:
            dict = {}
            dict['text'] = elem.xpath('.//h2/a/child::text()')[0]
            dict['link'] = 'https://yandex.ru' + elem.xpath('.//h2/a/@href')[0]
            dict['date'] = elem.xpath('.//div[@class="story__date"]/child::text()')[0][-5:] + ' ' + str(date.today())
            dict['source'] = elem.xpath('.//div[@class="story__date"]/child::text()')[0][:-5]
            yandex.insert_one(dict)

        return True
    except:
        print('Error')

def request_to_mail():
    try:
        mail = {}
        response = requests.get('https://news.mail.ru/', headers=header)
        root = html.fromstring(response.text)
        link = 'https://news.mail.ru' + root.xpath("//a[@class='photo photo_full photo_scale js-topnews__item']/@href")[
            0]
        mail['link']=link
        mail['text'] = root.xpath("//a[@class='photo photo_full photo_scale js-topnews__item']/span/span/child::text()")[
            0].replace('\xa0', ' ')
        response = requests.get(link, headers=header)
        root = html.fromstring(response.text)
        mail['source'] = root.xpath("//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']/child::text()")
        news_time = root.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]
        mail['time'] = news_time[:10] + ' ' + news_time[11:16]
        newsmail.insert_one(mail)
        response = requests.get('https://news.mail.ru/', headers=header)
        root = html.fromstring(response.text)
        news = root.xpath("//td[@class='daynews__items']/div")
        for elems in news:
            mail={}
            rawlink = elems.xpath(".//a/@href")[0]
            link = rawlink if 'mail' in rawlink else "https://news.mail.ru" + rawlink
            mail['link']=link
            mail['text'] = elems.xpath(".//a/span/span/child::text()")[0]
            response = requests.get(link, headers=header)
            root = html.fromstring(response.text)
            mail['source'] = root.xpath("//a[@class='link color_gray breadcrumbs__link']//span[@class='link__text']/child::text()")[0]
            news_time = root.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]
            mail['time'] = news_time[:10] + ' ' + news_time[11:16]
            newsmail.insert_one(mail)
        return True
    except:
        print('Error')


request_to_mail()
request_to_yandex()
request_to_lenta()




