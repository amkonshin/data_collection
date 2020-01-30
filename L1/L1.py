#1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.
import requests
import json
from pprint import pprint

user='amkonshin'
r=requests.get(f'https://api.github.com/users/{user}/repos')
print('Task1')
print(f'Репозитории пользователя {user}:')
repos=[]
for repo in r.json():

    print(repo['html_url'])

with open("L1_T1.json", "w") as write_file:
    json.dump(r.json(), write_file)


#2. Изучить список открытых API.
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
api='281a8cdabe2075fbfb605a6e5a940ae4'
lastfm=requests.get(f'http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={api}&format=json')
print('Task2')
print('Самые популярные музыканты, LastFM')
print('|{: ^25}|{: ^45}|'.format('Имя','Кол-во прослушиваний'))
with open("L1_T2.json", "w") as write_file:
    json.dump(lastfm.json(), write_file)
for artist in lastfm.json()['artists']['artist']:
    print('|{: ^25}|{: ^45}|'.format(artist['name'], artist['playcount']))

