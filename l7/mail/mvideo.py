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
time.sleep(4)
car=driver.find_element_by_xpath('//div[contains(text(),"Хиты продаж")]/../../..')
ActionChains(driver).move_to_element(car).perform()

goods=driver.find_element_by_class_name('sel-product-tile-title').text
print(goods)
next=car.find_element_by_class_name('sel-hits-button-next')
next.click()



#hits=driver.find_element_by_class_name('gallery-title-wrapper')
# hits.click()
#actions = ActionChains(driver)
#actions.move_to_element(hits).perform()

# for i in range(5):
#     articles = driver.find_elements_by_tag_name('article')
#     actions = ActionChains(driver)
#     actions.move_to_element(articles[-1])
#     # actions.send_keys('asdasd')
#     # actions.click_and_hold()
#     actions.perform()