from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['mvideo']

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')

assert 'М.Видео' in driver.title

time.sleep(5)

a = driver.find_elements_by_xpath("//div[@class='h2 u-mb-0 u-ml-xs-20 u-font-normal']")

for el in a:
    if el.text == 'Хиты продаж':
        find_a = el.find_element_by_xpath("../../..//div[@class='carousel-paging']").find_elements_by_tag_name('a')
        button_count = len(find_a)
        button = el.find_element_by_xpath(f"../../..//div[@class='carousel-paging']/a[{button_count}]")
        button.click()
        time.sleep(5)
        block = el.find_element_by_xpath("../../..//div[@class='gallery-layout sel-hits-block ']")
        block_count = block.find_elements_by_tag_name('li')
        hits_info = {}
        for elem in block_count:
            hits = elem.find_element_by_tag_name('a')
            info = hits.get_attribute('data-product-info')
            link = hits.get_attribute('href')
            hits_info['product'] = info
            hits_info['link'] = link
            mvideo_hits = db.mvideo_hits
            mvideo_hits.replace_one(hits_info, hits_info, upsert=True)
