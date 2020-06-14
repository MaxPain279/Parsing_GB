from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['vacancies_yandex']

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

link = 'https://yandex.ru/news/'

responce = requests.get(link, headers=header)

dom = html.fromstring(responce.text)

page = dom.xpath(
    "//td[@class='stories-set__item'] | //div[@class='story__aside']")
my_news = []
for news in page:
    item = {}
    name = news.xpath("//h2/a/text()")
    for el in name:
        name = el.replace('\xa0', ' ')
    url = news.xpath(".//a[contains(@class,'link')]/@href")
    for el in url:
        url = link + el
    time_source = news.xpath(".//div[@class='story__date']/text()")
    for el in time_source:
        time_source = el.split()
    source_list = time_source[:-1]
    source = (' '.join((str(i) for i in source_list)))
    item['name'] = name
    item['link'] = url
    item['time_add'] = time_source[-1]
    item['source'] = source

    my_news.append(item)
    news = db.news
    news.replace_one(item, item, upsert=True)

pprint(my_news)
