from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['vacancies_lenta']

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

link = 'https://lenta.ru/'

responce = requests.get(link, headers=header)

dom = html.fromstring(responce.text)

page = dom.xpath(
    "//div[@class='titles'] | //div[@class='item']")
my_news = []
for news in page:
    item = {}
    name = news.xpath(".//a/text() | .//span/text()")
    for el in name:
        name = el.replace('\xa0', ' ')
    url = news.xpath(".//a/@href")
    for el in url:
        url = link + el
    time = news.xpath("..//span[@class='time']/text() | .//time/@datetime")
    item['name'] = name
    item['link'] = url
    item['time_add'] = time
    my_news.append(item)
    news = db.news
    news.replace_one(item, item, upsert=True)

pprint(my_news)
