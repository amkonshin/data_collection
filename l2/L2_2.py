from bs4 import BeautifulSoup as bs
import requests,re,pprint
profession=input('Введите название профессии для поиска: ')
q=int(input('Введите количество страниц для поиска: '))
profession=profession.replace(' ','-')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
page_number=1
res = requests.get(f'https://www.superjob.ru/vacancy/search/?keywords={profession}&geo%5Bc%5D%5B0%5D=1&page={page_number}',
                   headers=headers)
vacansies_list=[]
i=0
while res.status_code==200 and i<q:
    html = bs(res.text, 'html.parser').find('div', {'class': '_1ID8B'})
    vacancies = html.findAll('div', {'class': '_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})

    for vacancy in vacancies:
        vacancy_info={}
        vacancy_info['name'] = vacancy.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()
        vacancy_info['link'] = 'www.superjob.ru' + vacancy.find('a', {'class': '_1QIBo'})['href']
        vacancy_info['site'] = 'superjob.ru'
        salary = vacancy.find('span', {'class': '_2Wp8I'}).getText().replace('\xa0', '')

        if salary=='По договорённости':
            vacancy_info['salary'] = 'По договорённости'
        else:
            min=[]
            max=[]

            min = re.findall('от(\d+)|(\d+)—\d+', salary)#кортеж из двух элементов, один из которых содержит min
            if min:#извлечение значения из кортежа
                if min[0][0]:
                    vacancy_info['min_salary'] = min[0][0]
                else:
                    vacancy_info['min_salary'] = min[0][1]
            max = re.findall('до(\d+)|\d+—(\d+)|^(\d+.)$', salary)
            if max:
                if max[0][0]:
                    vacancy_info['max_salary'] = max[0][0]
                elif max[0][1]:
                    vacancy_info['max_salary'] = max[0][1]
                else:
                    vacancy_info['max_salary'] = max[0][2]
        print(vacancy_info)
        vacansies_list.append(vacancy_info)
    page_number +=1
    i+=1
    res = requests.get(f'https://www.superjob.ru/vacancy/search/?keywords={profession}&geo%5Bc%5D%5B0%5D=1&page={page_number}',
                   headers=headers)
