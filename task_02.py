import requests
from datetime import date

main_link = 'https://currate.ru/api/'
pair = 'USDRUB'

today = date.today()
print(today)

params = {'get': 'rates',
          'pairs': pair,
          'date': today,
          'key': 'a0cdcbf3083828de17f355deb720d975'}

response = requests.get(main_link, params=params)

data = response.json()
print(data)

with open('currate.json', 'wb') as f:
    f.write(response.content)
