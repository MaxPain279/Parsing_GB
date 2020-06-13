from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacancies_hh']

vacancies = db.vacancy

user_input = int(input('Введите желаемую зарплату '))

for vacancy in vacancies.find({'$or': [{'salary_min': {'$gt': user_input}}, {'salary_max': {'$gt': user_input}}]}):
    pprint(vacancy)

vacancies.delete_many({})
