import requests
from dotenv import load_dotenv
from datetime import datetime
from itertools import count
import os
from terminaltables import AsciiTable


def count_date_from_to():
    date_now = datetime.now()
    date_to = date_now.strftime("%Y-%m-%d")
    if date_now.month != 1:
        month, year = (date_now.month-1, date_now.year)
    else:
        month, year = (12, date_now.year-1)
    date_month = date_now.replace(day=1, month=month, year=year)
    date_from = date_month.strftime("%Y-%m-%d")
    return date_from, date_to


def get_hh_page(date_from, date_to, page, vacancy):
    hh_url = "https://api.hh.ru/vacancies"
    params = {
        "text": vacancy,
        "date_from": date_from,
        "date_to": date_to,
        "page": page,
        "per_page": 20,
        "describe_arguments": True,
    }
    response = requests.get(hh_url, params=params)
    response.raise_for_status()
    vacancies_response = response.json()
    return vacancies_response


def get_sj_page(date_from, date_to, vacancy, api_id, page):
    sj_url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": api_id,
    }
    params = {
        "keyword": vacancy,
        "date_published_from": date_from,
        "date_published_to ": date_to,
        "page": page,
        "count": 5,
        'town': 'Москва',
    }
    response = requests.get(sj_url, params=params, headers=headers)
    response.raise_for_status()
    vacancies_response = response.json()
    return vacancies_response


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to)/2
    elif salary_from and (salary_to is None or salary_to == 0):
        return salary_from * 1.2
    elif salary_to and (salary_from is None or salary_from == 0):
        return salary_to * 0.8


def predict_vacancy_hh(date_from, date_to):
    vacancies = ["Python", "JavaScript", "Ruby", "Java",
                 "PHP", "C++", "Go", "Swift"]
    predicted_vacancy = dict()
    vacancies_limit = 2000
    per_page = 20
    stop_page = vacancies_limit/per_page - 1
    for vacancy in vacancies:
        salary = []
        vacancies_data = {"vacancies_found": "", "vacancies_processed": "",
                          "average_salary": ""}
        for page in count():
            hh_vacancies_response = get_hh_page(
                date_from, date_to, page, vacancy)
            for item in hh_vacancies_response['items']:
                if item['salary'] and item['salary']['currency'] == 'RUR':
                    salary.append(predict_salary(item['salary']['from'],
                                                 item['salary']['to']))
            if page >= stop_page:
                break
        vacancies_data["average_salary"] = int(
            sum(salary)/len(salary))
        vacancies_data["vacancies_processed"] = len(salary)
        vacancies_data["vacancies_found"] = hh_vacancies_response["found"]
        predicted_vacancy[vacancy] = vacancies_data
    return predicted_vacancy


def predict_vacancy_sj(date_from, date_to, api_id):
    vacancies = ["Python", "JavaScript", "Ruby", "Java",
                 "PHP", "C++", "Go", "Swift"]
    predicted_vacancy = dict()
    vacancies_per_page = 5
    for vacancy in vacancies:
        salary = []
        vacancies_data = {"vacancies_found": "",
                          "vacancies_processed": "",
                          "average_salary": "",
                          }
        for page in count():
            sj_vacancies_response = get_sj_page(
                date_from, date_to, vacancy, api_id, page)
            for object in sj_vacancies_response['objects']:
                object_sum = object['payment_from'] + object['payment_to']
                if object_sum > 0 and object['currency'] == 'rub':
                    salary.append(int(predict_salary(object['payment_from'],
                                                     object['payment_to'])))
            if page >= sj_vacancies_response['total']//vacancies_per_page:
                break
        vacancies_data["average_salary"] = int(
            sum(salary)/len(salary))
        vacancies_data["vacancies_processed"] = len(salary)
        vacancies_data["vacancies_found"] = sj_vacancies_response['total']
        predicted_vacancy[vacancy] = vacancies_data
    return predicted_vacancy


def process_statistics(predict_vacancy, title):
    header = ['Язык программирования', 'Вакансий найдено',
              'Вакансий обработано', 'Средняя зарплата']
    vacancies_list = []
    for vacancy in predict_vacancy.items():
        vacancies_list.append(vacancy[0])
        vacancies_list.append(vacancy[1]['vacancies_found'])
        vacancies_list.append(vacancy[1]['vacancies_processed'])
        vacancies_list.append(vacancy[1]['average_salary'])
    chunk_size = 4
    chunked_list = [vacancies_list[item:item+chunk_size]
                    for item in range(0, len(vacancies_list), chunk_size)]
    chunked_list.append(header)
    chunked_list = chunked_list[::-1]
    hh_table_instance = AsciiTable(chunked_list, title)
    return hh_table_instance.table


def main():
    load_dotenv()
    sj_api_app_id = os.environ.get("SJ_API_ID")
    date_from, date_to = count_date_from_to()
    predicted_hh = predict_vacancy_hh(date_from, date_to)
    predicted_sj = predict_vacancy_sj(date_from, date_to, sj_api_app_id)
    title_hh = 'Head Hunter Moscow'
    title_sj = 'Super job Moscow'
    print(process_statistics(predicted_hh, title_hh))
    print(process_statistics(predicted_sj, title_sj))


if __name__ == '__main__':
    main()
