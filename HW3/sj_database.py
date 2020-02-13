from bs4 import BeautifulSoup as bs
import requests,re,pprint
from pymongo import MongoClient
client= MongoClient('localhost',27017)
db=client['vacancies']
sj=db.superjob
def search():
    number=int(input('Введите зарплату для поиска'))
    values=sj.find({'$or':[{'min_salary':{'$gt': number}},{'max_salary':{'$gt': number}}]})
    for value in values:
        print(value)

def parcer():
    profession = input('Введите название профессии для поиска: ')
    q = int(input('Введите количество страниц для поиска: '))
    profession = profession.replace(' ', '-')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
    page_number = 1
    res = requests.get(
        f'https://www.superjob.ru/vacancy/search/?keywords={profession}&geo%5Bc%5D%5B0%5D=1&page={page_number}',
        headers=headers)
    vacansies_list = []
    button = bs(res.text, 'html.parser').find('div', {'class': 'L1p51'}).findAll('span', {'class': '_3IDf-'})
    button = button[-2].getText()
    i = 0
    while i < int(button):
        html = bs(res.text, 'html.parser').find('div', {'class': '_1ID8B'})
        vacancies = html.findAll('div', {'class': '_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})

        for vacancy in vacancies:
            vacancy_info = {}
            vacancy_info['name'] = vacancy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()
            vacancy_info['link'] = 'www.superjob.ru' + vacancy.find('a', {'class': '_1QIBo'})['href']
            vacancy_info['site'] = 'superjob.ru'
            salary = vacancy.find('span', {'class': '_2Wp8I'}).getText().replace('\xa0', '')
            min_salary_key = 0
            max_salary_key = 0
            if salary == 'По договорённости':
                vacancy_info['min_salary'] = 'По договорённости'
                vacancy_info['max_salary'] = 'По договорённости'
            else:
                min = []
                max = []

                min = re.findall('от(\d+)|(\d+)—\d+', salary)  # кортеж из двух элементов, один из которых содержит min
                if min:  # извлечение значения из кортежа
                    if min[0][0]:
                        min_salary_key=1
                        vacancy_info['min_salary'] = int(min[0][0])
                    else:
                        min_salary_key = 1
                        vacancy_info['min_salary'] = int(min[0][1])
                max = re.findall('до(\d+)|\d+—(\d+)|^(\d+.)$', salary)
                if max:
                    if max[0][0]:
                        max_salary_key = 1
                        vacancy_info['max_salary'] = int(max[0][0])
                    elif max[0][1]:
                        max_salary_key = 1
                        vacancy_info['max_salary'] = int(max[0][1])
                    else:
                        max_salary_key = 1
                        vacancy_info['max_salary'] = int(max[0][2][:-1])
            if min_salary_key==1:
                if max_salary_key==1:
                    key = sj.find({'name': vacancy_info['name'], 'link': vacancy_info['link'],'site': vacancy_info['site'],
                                  'min_salary': vacancy_info['min_salary'],
                                  'max_salary': vacancy_info['max_salary']})
                else:
                    key = sj.find({'name': vacancy_info['name'], 'link': vacancy_info['link'],
                                  'site': vacancy_info['site'],
                                  'min_salary': vacancy_info['min_salary']})
            else:
                if max_salary_key==1:
                    key = sj.find({'name': vacancy_info['name'], 'link': vacancy_info['link'],
                                  'site': vacancy_info['site'],
                                  'max_salary': vacancy_info['max_salary']})
                else:
                    key = sj.find({'name': vacancy_info['name'], 'link': vacancy_info['link'],
                                  'site': vacancy_info['site']})

            valid=[]
            for elem in key:
                valid.append(elem)
            if not valid:
                sj.insert_one(vacancy_info)
            print(vacancy_info)
            vacansies_list.append(vacancy_info)
        page_number += 1
        i += 1
        res = requests.get(
            f'https://www.superjob.ru/vacancy/search/?keywords={profession}&geo%5Bc%5D%5B0%5D=1&page={page_number}',
            headers=headers)


