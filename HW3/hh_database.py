from bs4 import BeautifulSoup as bs
import requests,re,pprint
from pymongo import MongoClient
client= MongoClient('localhost',27017)
db=client['vacancies']
hh=db.hh
def search():
    number=int(input('Введите зарплату для поиска'))
    values=hh.find({'$or':[{'min_salary':{'$gt': number}},{'max_salary':{'$gt': number}}]})
    for value in values:
        print(value)

def parcer():
    profession=input('Введите название профессии для поиска: ')
    q=int(input('Введите количество страниц для поиска: '))
    profession=profession.replace(' ','+')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    page_number=0
    res = requests.get(f'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text={profession}&page={page_number}',
                       headers=headers)
    vacansies_list=[]
    i=0
    while res.status_code==200 and i<q:
        html = bs(res.text, 'html.parser').find('div', {'data-qa': 'vacancy-serp__results'})

        vacancies = html.findAll('div', {'class': 'vacancy-serp-item'})

        for vacancy in vacancies:
            vacancy_info={}
            vacancy_info['name']=vacancy.find('a', {'class':'bloko-link HH-LinkModifier'}).getText()
            vacancy_info['link']=vacancy.find('a', {'class':'bloko-link HH-LinkModifier'})['href']
            vacancy_info['site']='hh.ru'

            salary=vacancy.find('div', {'class':'vacancy-serp-item__compensation'})
            min_salary_key = 0
            max_salary_key = 0
            if salary:
                min=[]
                max=[]
                salary=salary.getText().replace('\xa0','')
                min=re.findall('от\s(\d+)|(\d+)-\d+',salary)#кортеж из двух элементов, один из которых содержит min

                if min:#извлечение значения из кортежа
                    if min[0][0]:
                        vacancy_info['min_salary'] = int(min[0][0])
                        min_salary_key=1
                    else:
                        vacancy_info['min_salary'] = int(min[0][1])
                        min_salary_key = 1
                max=re.findall('до\s(\d+)|\d+-(\d+)',salary)
                if max:
                    if max[0][0]:
                        vacancy_info['max_salary'] = int(max[0][0])
                        max_salary_key = 1
                    else:
                        vacancy_info['max_salary'] = int(max[0][1])
                        max_salary_key = 1
            if min_salary_key==1:
                if max_salary_key==1:
                    key = hh.find({'name': vacancy_info['name'], 'link': vacancy_info['link'],'site': vacancy_info['site'],
                                  'min_salary': vacancy_info['min_salary'],
                                  'max_salary': vacancy_info['max_salary']})
                else:
                    key = hh.find({'name': vacancy_info['name'], 'link': vacancy_info['link'],
                                  'site': vacancy_info['site'],
                                  'min_salary': vacancy_info['min_salary']})
            else:
                if max_salary_key==1:
                    key = hh.find({'name': vacancy_info['name'], 'link': vacancy_info['link'],
                                  'site': vacancy_info['site'],
                                  'max_salary': vacancy_info['max_salary']})
                else:
                    key = hh.find({'name': vacancy_info['name'], 'link': vacancy_info['link'],
                                  'site': vacancy_info['site']})

            valid=[]
            for elem in key:
                valid.append(elem)
            if not valid:
                hh.insert_one(vacancy_info)
            vacansies_list.append(vacancy_info)
        page_number +=1
        i+=1
        res = requests.get(f'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text={profession}&page={page_number}',
            headers=headers)
parcer()
