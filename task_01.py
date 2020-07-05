from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['mail_massages']

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mail.ru')

assert 'Mail.ru' in driver.title

elem = driver.find_element_by_id('mailbox:login')
elem.send_keys('study.ai_172@mail.ru')

button = driver.find_element_by_id('mailbox:submit')
button.click()

time.sleep(3)

elem = driver.find_element_by_id('mailbox:password')
elem.send_keys('NextPassword172')
elem.send_keys(Keys.RETURN)

time.sleep(5)

elem = driver.find_element_by_class_name('llc')

elem.send_keys(Keys.DOWN)
elem.send_keys(Keys.RETURN)

time.sleep(5)

while True:
    try:
        massages_my_mail = {}
        button = driver.find_element_by_class_name('ico_16-arrow-down')
        button.click()
        time.sleep(2)
        contact = driver.find_element_by_class_name('letter-contact')
        letter_contact = contact.get_attribute('title')
        letter_date = driver.find_element_by_class_name('letter__date').text
        title = driver.find_element_by_tag_name('h2').text
        massage = driver.find_element_by_class_name('js-readmsg-msg').text

        massages_my_mail['letter_contact'] = letter_contact
        massages_my_mail['letter_date'] = letter_date
        massages_my_mail['title'] = title
        massages_my_mail['massage'] = massage
        massage_link = db.massage_link
        massage_link.replace_one(massages_my_mail, massages_my_mail, upsert=True)
        pprint(massages_my_mail)
    except:
        break
