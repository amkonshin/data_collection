# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongobase = client.vacansy_280

    def hh_salary(self, salary):
        salary = ''.join(salary).replace('\xa0','')

        min_salary='з/п не указана'
        max_salary = 'з/п не указана'
        min = []
        max = []
        min = re.findall('от\s(\d+)|(\d+)-\d+', salary)
        if min:
            if min[0][0]:
                min_salary = min[0][0]
            else:
                min_salary = min[0][1]
        max = re.findall('до\s(\d+)|\d+-(\d+)', salary)
        if max:
            if max[0][0]:
                max_salary = max[0][0]
            else:
                max_salary = max[0][1]

        return min_salary,max_salary
    def jobru_salary(self, salary):


        min_salary='з/п не указана'
        max_salary = 'з/п не указана'
        salary = ''.join(salary).replace('\xa0','')
        min_salary_key = 0
        max_salary_key = 0
        if salary == 'По договорённости':
            min_salary = 'По договорённости'
            max_salary = 'По договорённости'
        else:
            min = []
            max = []

            min = re.findall('от(\d+)|(\d+)—\d+', salary)  # кортеж из двух элементов, один из которых содержит min
            if min:  # извлечение значения из кортежа
                if min[0][0]:
                    min_salary_key = 1
                    min_salary = int(min[0][0])
                else:
                    min_salary_key = 1
                    min_salary = int(min[0][1])
            max = re.findall('до(\d+)|\d+—(\d+)|^(\d+.)$', salary)
            if max:
                if max[0][0]:
                    max_salary_key = 1
                    max_salary = int(max[0][0])
                elif max[0][1]:
                    max_salary_key = 1
                    max_salary = int(max[0][1])
                else:
                    max_salary_key = 1
                    max_salary = int(max[0][2][:-1])
        return min_salary,max_salary
    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        data={}


        data['name']=item['name']
        data['link'] = item['link']
        data['source'] = item['source']
        if spider.name=='hhru':
            data['min_salary'],data['max_salary']= self.hh_salary(item['salary'])
        elif spider.name=='jobru':
            data['min_salary'], data['max_salary'] = self.jobru_salary(item['salary'])
        print(data)
        collection.insert_one(data)


        return item


