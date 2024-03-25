import psycopg2
import requests
import json
import logging


def get_hh_json(employers: list[str]) -> list[dict]:
    """
    Получает данные: информация о работодателях и их вакансиях. Формат json
    """
    data = []
    for e in employers:
        url = f'https://api.hh.ru/employers/{e}'
        company_data = requests.get(url).json()
        vacancy_data = requests.get(company_data['vacancies_url']).json()
        data.append({'employers': company_data, 'vacancies': vacancy_data['items']})
    return data


def create_db(db_name: str, params: dict) -> None:
    """
    Сoздаёт базу данных по вакансиям с сайта hh.ru
    """
    conn = psycopg2.connect(db_name='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
    cur.execute(f'CREATE DATABASE {db_name}')
    conn.close()

    conn = psycopg2.connect(db_name=db_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE employers (
            employer_id SERIAL PRIMARY KEY,
            employer_name VARCHAR UNIQUE,
            url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            employer_name text REFERENCES employers(employer_name),
            city VARCHAR(50),
            title VARCHAR(200),
            schedule TEXT,
            requirement TEXT,
            responsibility TEXT,
            salary INT,
            url VARCHAR(200),
            FOREIGN KEY(employer_name) REFERENCES employers(employer_name)
            )
        """)
    conn.commit()
    conn.close()
    logging.info("Таблицы 'employers' и 'vacancies' созданы.")


