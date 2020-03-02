#1) Написать программу, которая собирает входящие письма из своего или тестового
# почтового ящика и сложить данные о письмах в базу данных (от кого, дата отправки,
# тема письма, текст письма)
from pymongo import MongoClient
client= MongoClient('localhost',27017)
db=client['Mails']

mail_db=db.mails

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests as re

driver = webdriver.Chrome()

import time

driver.get('https://e.mail.ru/')

mail = WebDriverWait(driver, 3).until( EC.element_to_be_clickable((By.NAME, "Login")))
mail.send_keys('study.ai_172')
mail.send_keys(Keys.ENTER)

password = WebDriverWait(driver, 3).until( EC.element_to_be_clickable((By.NAME, "Password")))
password.send_keys('NewPassword172')
password.send_keys(Keys.ENTER)

first_mail=WebDriverWait(driver, 3).until( EC.element_to_be_clickable((By.CLASS_NAME, "llc")))
first_mail.click()

while True:
    info={}
    time.sleep(1)
    info['body'] = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "letter__body"))).text
    info['theme']=WebDriverWait(driver, 3).until( EC.presence_of_element_located((By.CLASS_NAME, "thread__subject"))).text
    info['author']=WebDriverWait(driver, 3).until( EC.presence_of_element_located((By.CLASS_NAME, "letter-contact"))).text
    info['date']=WebDriverWait(driver, 3).until( EC.presence_of_element_located((By.CLASS_NAME, "letter__date"))).text
    mail_db.insert_one(info)
    print(info)
    try:
        next = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "ico_16-arrow-down")))
        next.click()
    except:
        print('End')
        break


driver.quit()