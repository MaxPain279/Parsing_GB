from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['vacancies_hh']

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

link = 'https://news.mail.ru'

responce = requests.get(link, headers=header)

dom = html.fromstring(responce.text)

page = dom.xpath(
    "//span[@class = 'list__text'] | //span[@class='cell']")
my_news = []
for news in page:
    item = {}
    name = news.xpath(".//span[@class='link__text']/text() | .//span[@class='newsitem__title-inner']/text()")
    for el in name:
        name = el.replace('\xa0', ' ')
    url = news.xpath(".//a[contains(@class, 'link_flex')]/@href | .//a[contains(@class, 'link-holder')]/@href")
    for el in url:
        url = link + el
    if len(url) > 0:
        responce_2 = requests.get(url, headers=header)
        dom_2 = html.fromstring(responce_2.text)
        source = dom_2.xpath("//a[contains(@class, 'breadcrumbs__link')]/span/text()")
        time = dom_2.xpath("//span[@datetime]/@datetime")
    else:
        continue
    item['name'] = name
    item['link'] = url
    item['source'] = source
    item['time_add'] = time
    my_news.append(item)
    news = db.news
    news.replace_one(item, item, upsert=True)

pprint(my_news)
print(len(my_news))
