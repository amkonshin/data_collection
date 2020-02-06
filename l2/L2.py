from bs4 import BeautifulSoup as bs
import requests,re,pprint
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
    html=bs(res.text, 'html.parser').find('div', {'class':'vacancy-serp vacancy-serp_xs-mode'})
    vacancies=html.findAll('div', {'class':'vacancy-serp-item'})

    for vacancy in vacancies:
        vacancy_info={}
        vacancy_info['name']=vacancy.find('a', {'class':'bloko-link HH-LinkModifier'}).getText()
        vacancy_info['link']=vacancy.find('a', {'class':'bloko-link HH-LinkModifier'})['href']
        vacancy_info['site']='hh.ru'

        salary=vacancy.find('div', {'class':'vacancy-serp-item__compensation'})

        if salary:
            min=[]
            max=[]
            salary=salary.getText().replace('\xa0','')
            min=re.findall('от\s(\d+)|(\d+)-\d+',salary)#кортеж из двух элементов, один из которых содержит min
            if min:#извлечение значения из кортежа
                if min[0][0]:
                    vacancy_info['min_salary'] = min[0][0]
                else:
                    vacancy_info['min_salary'] = min[0][1]
            max=re.findall('до\s(\d+)|\d+-(\d+)',salary)
            if max:
                if max[0][0]:
                    vacancy_info['max_salary'] = max[0][0]
                else:
                    vacancy_info['max_salary'] = max[0][1]
        print(vacancy_info)
        vacansies_list.append(vacancy_info)
    page_number +=1
    i+=1
    res = requests.get(f'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text={profession}&page={page_number}',
        headers=headers)
