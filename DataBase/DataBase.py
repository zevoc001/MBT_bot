# -*- coding: utf-8 -*-
import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = os.path.join(Path().absolute(), 'example.env')
load_dotenv(dotenv_path)
DB_path = os.getenv('DB_PATH') + 'mbt.db'



class Telegram_DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users_data (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                Телеграм_ID         INTEGER NOT NULL,
                Доступ              TEXT    NOT NULL
                                    DEFAULT "Гость",
                [Дата регистрации]  DATA    NOT NULL,
                Статус              TEXT,
                Рейтинг             INTEGER DEFAULT (0),
                Заработок           INTEGER DEFAULT (0),
                Заказы              INTEGER DEFAULT (0),
                Комментарии         TEXT,
                Фотография          BLOB,
                ФИО                 TEXT    NOT NULL,
                Пол                 TEXT    NOT NULL
                                    CHECK (Пол = "Мужской" OR Пол = "Женский"),
                [Дата рождения]     TEXT    NOT NULL,
                [Место жительства]  TEXT,
                Образование         TEXT    NOT NULL,
                Курс                INTEGER,
                Специальность       TEXT,
                [Мин. ЗП]           INTEGER,
                [Тяжелый труд]      INTEGER,
                [Средний труд]      INTEGER,
                [Творческий труд]   INTEGER,
                [Иные работы]       TEXT,
                [Рабочее время]     TEXT,
                Инструменты         ТEXT,
                Местный             INTEGER,
                Языки               TEXT,
                Телефон             TEXT    NOT NULL,
                Водитель            TEXT,
                Машина              INTEGER
                Служил              INTEGER,
                [Доп. инф.]         TEXT
            )
        ''')
        self.conn.commit()
    
    def add_user(self, user_id, data_reg, photo, fio, sex, born, education_level, course, profession, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place):
        self.cursor.execute('''
        INSERT INTO users_data (Телеграм_ID, [Дата регистрации], Фотография, ФИО, Пол, [Дата рождения], Образование, Курс, Специальность, [Мин. ЗП], [Тяжелый труд], [Средний труд], [Творческий труд], [Иные работы], Инструменты, Телефон, [Место жительства])
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, data_reg, photo, fio, sex, born, education_level, course, profession, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place))
        self.conn.commit()
    
    def get_user_info(self, user_id):
        result = self.cursor.execute('''
        SELECT [Дата регистрации], Фотография, ФИО, Пол, [Дата рождения], Образование, Курс, Специальность, [Мин. ЗП], [Тяжелый труд], [Средний труд], [Творческий труд], [Иные работы], Инструменты, Телефон, [Место жительства], Заработок, Заказы FROM users_data
        WHERE Телеграм_ID = ?
        ''', (user_id, )).fetchone()
        return result
    
    def user_is_exist(self, user_id):
        user = self.cursor.execute('''
        SELECT * FROM users_data
        WHERE Телеграм_ID = ?
        ''', (user_id, )).fetchone()
        if user is not None:
            return 1
        else:
            return 0
    
    def edit_user(self, user_id, data_reg, photo, fio, sex, born, education_level, course, profession, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place):
        self.cursor.execute('''
        UPDATE users_data
        SET [Дата регистрации] = ?, 
            Фотография = ?, 
            ФИО = ?, 
            Пол = ?, 
            [Дата рождения] = ?, 
            Образование = ?, 
            Курс = ?, 
            Специальность = ?, 
            [Мин. ЗП] = ?, 
            [Тяжелый труд] = ?, 
            [Средний труд] = ?, 
            [Творческий труд] = ?, 
            [Иные работы] = ?, 
            Инструменты = ?, 
            Телефон = ?, 
            [Место жительства] = ?
        WHERE Телеграм_ID = ?
        ''', (data_reg, photo, fio, sex, born, education_level, course, profession, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place, user_id))
        self.conn.commit()
        

    def close(self):
        self.conn.close()


class Companies_DB:
    def __init__(self):
        self.conn = sqlite3.connect('mbt.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        # Создаем таблицу, если ее нет
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_state TEXT,
                first_name TEXT,
                last_name TEXT,
                age INTEGER
            )
        ''')
        self.conn.commit()
    
    def add_user(self, user_id, user_state, first_name, last_name, age):
        self.cursor.execute('''
        INSERT INTO telegram_data (user_id, user_state, first_name, last_name, age)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, user_state, first_name, last_name, age))
        self.conn.commit()
        return True
    
    def get_user_data(self, user_id):
        result = self.cursor.execute('''
        SELECT * FROM telegram_data
        WHERE user_id = ?
        ''', (user_id, )).fetchone()
        return result
    
    def close(self):
        self.conn.close()