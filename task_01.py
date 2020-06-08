from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'Accept': '*/*'}


def hh_ru(main_link, cnt_ctr):
    main_link = main_link  # 'https://www.hh.ru'
    params = {'area': 1,
              'st': 'searchVacancy',
              'text': 'Python',
              'fromSearch': 'true',
              'from': 'suggest_post',
              'page': ''}
    i = 0
    vacancies = []
    for el in range(cnt_ctr):
        response = requests.get(main_link + '/search/vacancy/', params=params, headers=headers)
        soup = bs(response.text, 'lxml')
        next_button = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        vacancy_block = soup.find('div', {'class': 'vacancy-serp'})
        vacancy_list = vacancy_block.findChildren(recursive=False)

        for vacancy in vacancy_list:
            try:
                vacancy_data = {}
                tag_link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})
                link = tag_link['href']
                name = tag_link.text
                salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).findChild()
                if not salary:
                    salary_min = None
                    salary_max = None
                    cur = None
                else:
                    salary = salary.getText().replace(u'\xa0', u'')
                    salaries = salary.split('-')
                    print(salaries)
                    cur_list = re.findall(r'\w+', salaries[0])
                    cur = cur_list[-1]
                    salary_min = int(re.sub(r'[^0-9]', '', salaries[0]))
                    if len(salaries) > 1:

                        cur_list = re.findall(r'\w+', salaries[1])
                        cur = cur_list[-1]
                        salary_max = int(re.sub(r'[^0-9]', '', salaries[1]))
                    else:
                        salary_max = None
                vacancy_data['name'] = name
                vacancy_data['link'] = link
                vacancy_data['salary_min'] = salary_min
                vacancy_data['salary_max'] = salary_max
                vacancy_data['salary_currency'] = cur
                vacancies.append(vacancy_data)
            except:
                continue

        pprint(vacancies)
        if not next_button:
            break
        i += 1
        next_str = {'page': i}
        params.update(next_str)
    with open('database.csv', 'w', encoding='utf-8') as file:
        for i, record in enumerate(vacancies):
            for key, value in record.items():
                print(f'{key}: {value}', file=file)

            if i < len(vacancies) - 1:
                print(file=file)


hh_ru('https://www.hh.ru', 50)
