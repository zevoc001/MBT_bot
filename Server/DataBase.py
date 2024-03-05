# -*- coding: utf-8 -*-
import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = os.path.join(Path().absolute(), 'example.env')
load_dotenv(dotenv_path)
print(os.getenv("DB_HOST"))


class Telegram_DB:
    def __init__(self):
        db_name='test'
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        host= os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        conn_string = "dbname='{0}' user='{1}' password='{2}' host='{3}' port='{4}'".format(db_name, user, password, host, port)
        self.conn = psycopg2.connect(conn_string)
    
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_data (
                id                  SERIAL PRIMARY KEY,
                "Телеграм_ID"       INTEGER NOT NULL,
                "Доступ"            TEXT NOT NULL DEFAULT 'Гость',
                "Дата регистрации"  DATE NOT NULL,
                "Статус"            TEXT,
                "Рейтинг"           INTEGER DEFAULT 0,
                "Заработок"         INTEGER DEFAULT 0,
                "Заказы"            INTEGER DEFAULT 0,
                "Комментарии"       TEXT,
                "Фотография"        BYTEA,
                "ФИО"               TEXT NOT NULL,
                "Пол"               TEXT NOT NULL CHECK ("Пол" = 'Мужской' OR "Пол" = 'Женский'),
                "Дата рождения"     TEXT NOT NULL,
                "Место жительства"  TEXT,
                "Образование"       TEXT NOT NULL,
                "Курс"              INTEGER,
                "Специальность"     TEXT,
                "Мин. ЗП"           INTEGER,
                "Тяжелый труд"      TEXT,
                "Средний труд"      TEXT,
                "Творческий труд"   TEXT,
                "Иные работы"       TEXT,
                "Рабочее время"     TEXT,
                "Инструменты"       TEXT,
                "Местный"           INTEGER,
                "Языки"             TEXT,
                "Телефон"           TEXT NOT NULL,
                "Водитель"          TEXT,
                "Машина"            TEXT,
                "Служил"            TEXT,
                "Доп. инф."         TEXT
            );
        ''')
        self.conn.commit()
    
    def add_user(self, user_id, data_reg, photo, fio, sex, born, education_level, course, profession, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place):
        self.cursor.execute('''
        INSERT INTO users_data ("Телеграм_ID", "Дата регистрации", "Фотография", "ФИО", "Пол", "Дата рождения", "Образование", "Курс", "Специальность", "Мин. ЗП", "Тяжелый труд", "Средний труд", "Творческий труд", "Иные работы", "Инструменты", Телефон, "Место жительства")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (user_id, data_reg, photo, fio, sex, born, education_level, course, profession, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place))
        self.conn.commit()
    
    def get_user_info(self, user_id):
        self.cursor.execute('''
        SELECT "Дата регистрации", "Фотография", "ФИО", "Пол", "Дата рождения", "Образование", "Курс", "Специальность", "Мин. ЗП", "Тяжелый труд", "Средний труд", "Творческий труд", "Иные работы", "Инструменты", "Телефон", "Место жительства", "Заработок", "Заказы" FROM users_data
        WHERE "Телеграм_ID" = %s
        ''', (user_id, ))
        result = self.cursor.fetchone()
        return result
    
    def user_is_exist(self, user_id):
        self.cursor.execute('''
        SELECT * FROM users_data
        WHERE "Телеграм_ID" = %s
        ''', (user_id, ))
        user = self.cursor.fetchone()
        if user is not None:
            return 1
        else:
            return 0
    
    def edit_user(self, user_id, data_reg, photo, fio, sex, born, education_level, course, profession, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place):
        self.cursor.execute('''
        UPDATE users_data
        SET "Дата регистрации" = %s, 
            "Фотография" = %s, 
            "ФИО" = %s, 
            "Пол" = %s, 
            "Дата рождения" = %s, 
            "Образование" = %s, 
            "Курс" = %s, 
            "Специальность" = %s, 
            "Мин. ЗП" = %s, 
            "Тяжелый труд" = %s, 
            "Средний труд" = %s, 
            "Творческий труд" = %s, 
            "Иные работы" = %s, 
            "Инструменты" = %s, 
            "Телефон" = %s, 
            "Место жительства" = %s
        WHERE "Телеграм_ID" = %s
        ''', (data_reg, photo, fio, sex, born, education_level, course, profession, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place, user_id))
        self.conn.commit()
        

    def close(self):
        self.conn.close()