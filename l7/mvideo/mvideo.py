#2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')
goods_list=[]
car=driver.find_element_by_xpath('//div[contains(text(),"Хиты продаж")]/../../..')
ActionChains(driver).move_to_element(car).perform()

while True:
    time.sleep(3)
    hits=driver.find_element_by_class_name('sel-hits-block')
    goods=hits.find_elements_by_class_name('gallery-list-item')

    for good in goods:
        item={}
        item['name']=good.find_element_by_class_name('sel-product-tile-title').text
        item['price']=good.find_element_by_class_name('c-pdp-price__current').text
        if item['name']!='':
            goods_list.append(item)
        print(item)
    try:
        next=WebDriverWait(car, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, "sel-hits-button-next")))
        next.click()
    except:
        print('Done')
        break

print(goods_list)
print(len(goods_list))
