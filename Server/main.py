# -*- coding: utf-8 -*-
import sys, re, os
import telebot
from pathlib import Path
from dotenv import load_dotenv
import datetime
from telebot import types

dotenv_path = os.path.join(Path().absolute(), 'example.env')
load_dotenv(dotenv_path)
#sys.path.insert(0, os.getenv('DB_PATH'))
from DataBase import Telegram_DB

print(os.getenv('BOT_TOKEN'))
bot = telebot.TeleBot(os.getenv('BOT_TOKEN')) # Создаем бота
temp_user_data = {}
hide_board = types.ReplyKeyboardRemove() # Удаление панели
command_list = ['/start', '/profile']

def get_mess_photo(user_id):
    mess = bot.send_message(user_id, 'Отправьте пожалуйста ваше фото', reply_markup=hide_board)
    return mess

def get_mess_fio(user_id):
    mess = bot.send_message(user_id, 'Введите ваше ФИО (полностью)', reply_markup=hide_board)
    return mess

def get_mess_sex(user_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_male = types.KeyboardButton('Мужской')
        button_female = types.KeyboardButton('Женский')
        markup.add(button_male, button_female)
        mess = bot.send_message(user_id, 'Выберите ваш пол', reply_markup=markup)
        return mess

def get_mess_born(user_id):
    mess = bot.send_message(user_id, 'Напиши свою дату рождения в формате дд.мм.гггг', reply_markup=hide_board)
    return mess

def get_mess_education_level(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_school = types.KeyboardButton('Школа')
    button_college = types.KeyboardButton('Среднее профессиональное')
    button_high_school = types.KeyboardButton('Высшее')
    button_student = types.KeyboardButton('Студент')
    markup.add(button_school, button_college, button_high_school, button_student)
    mess = bot.send_message(user_id, 'Выберите уровень вашего образования', reply_markup=markup)
    return mess

def get_mess_course(user_id):
    mess = bot.send_message(user_id, 'Введите номер курса, на котором вы обучаетесь', reply_markup=hide_board)
    return mess

def get_mess_profission(user_id):
    mess = bot.send_message(user_id, 'Введите специальность и место обучения', reply_markup=hide_board)
    return mess

def get_mess_min_salary(user_id):
    mess = bot.send_message(user_id, 'За сколько рублей в час вы готовы работать?\nНапишите числом', reply_markup=hide_board)
    return mess

def get_mess_hardwork(user_id, sex):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.KeyboardButton('Да')
    btn_no = types.KeyboardButton('Нет')
    markup.add(btn_yes, btn_no)
    mess = bot.send_message(user_id, 'Готовы ли вы выполнять тяжелую работу (копать, ломать, строить)?', reply_markup=markup)
    return mess

def get_mess_midwork(user_id, sex):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.KeyboardButton('Да')
    btn_no = types.KeyboardButton('Нет')
    markup.add(btn_yes, btn_no)
    if sex == 'Мужской':
       mess = bot.send_message(user_id, 'Готовы ли вы выполнять работу средней сложности (уборка территорий, прочистка труб, и т.д.)?', reply_markup=markup)
       return mess
    else:
        mess = bot.send_message(user_id, 'Готовы ли вы ухаживать за детьми или пожилими людьми?', reply_markup=markup)
        return mess

def get_mess_artwork(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.KeyboardButton('Да')
    btn_no = types.KeyboardButton('Нет')
    markup.add(btn_yes, btn_no)
    mess = bot.send_message(user_id, 'Готовы ли вы выполнять творческую работу (аниматорство, ведение соцсетей, фото/видеосъемка и.т.д.)?', reply_markup=markup)
    return mess

def get_mess_addwork(user_id):
    mess = bot.send_message(user_id, 'Напишите, какие иные работы вы готовы выполнять (Если нет иных работ, напишите нет)', reply_markup=hide_board)
    return mess

def get_mess_phone(user_id):
    mess = bot.send_message(user_id, 'Введите ваш контактный номер телефона (формат 89995550011)', reply_markup=hide_board)
    return mess

def get_mess_tools(user_id):
    mess = bot.send_message(user_id, 'Какие инструменты для работы у вас есть (компьютер, дрель, электропила и т.д.)?', reply_markup=hide_board)
    return mess

def get_mess_local(user_id):
    mess = bot.send_message(user_id, 'Почти закончили. Осталось написать ваш адрес проживания (город, район, улица, дом)', reply_markup=hide_board)
    return mess

def get_mess_final(user_id):
    mess = 'Отлично, давайте еще раз проверим, все ли верно. Вот ваши данные'
    for i in temp_user_data[user_id]:
        if i != 'Фотография':
            data = temp_user_data[user_id][i]
            mess += '\n{}: {}'.format(i, data)
    return mess

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if db.user_is_exist(user_id):
        info = db.get_user_info(user_id)
        fio = info[2]
        markup = types.InlineKeyboardMarkup(row_width=1)
        button = types.InlineKeyboardButton('Да', callback_data='finding_job')
        markup.add(button)
        bot.send_message(user_id, 'Здравствуйте, {0}. Хотите начать поиск работы?'.format(fio), reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton('Да')
        markup.add(button)
        mess = bot.send_message(user_id, 'Здравствуйте. Мы компания, которая помогает найти работу. В данным момент мы работаем в тестовом режиме. Вы можете помочь нам, направляя рекомендации и пожелания на почту: ...,\nпо телефону: +7 962 453-99-94 (Telegram, WhatsApp),\n или при посещении нашего офиса по адресу: г. Ставрополь, ул.  Михаила морозова, д 25.\nСогласны ли вы продолжить работу в таком режиме?', reply_markup=markup)
        bot.register_next_step_handler(mess, start_reg)

def start_reg(message):
    user_id = message.from_user.id
    temp_user_data[user_id] = {}
    mess = bot.send_message(user_id, 'Хорошо, приступим! Для продолжения необходимо заполнить небольшую анкету.\nОтправьте пожалуйста свое фото', reply_markup=hide_board)
    bot.register_next_step_handler(mess, process_photo_step)

def process_photo_step(message):
    user_id = message.from_user.id
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        photo = bot.download_file(file_info.file_path)
        temp_user_data[user_id]['Фотография'] = photo
        mess = get_mess_fio(user_id)
        bot.register_next_step_handler(mess, process_fio_step)
    except:
        mess = bot.send_message(user_id, 'Ошибка загрузки! Попробуйте отправить другую фотографию', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_photo_step)

def process_fio_step(message):
    user_id = message.from_user.id
    if bool(re.match(r'^[а-яА-Я\s]+$', message.text)):
        temp_user_data[user_id]['ФИО'] = message.text
        mess = get_mess_sex(user_id)
        bot.register_next_step_handler(mess, process_sex_step)
    else:
        mess = bot.send_message(user_id, ' Пожалуйста, попробуйте ввести ФИО иначе.')
        bot.register_next_step_handler(mess, process_fio_step)

def process_sex_step(message):
    user_id = message.from_user.id
    if message.text in ['Мужской', 'Женский']:
        temp_user_data[user_id]['Пол'] = message.text
        mess = get_mess_born(user_id)
        bot.register_next_step_handler(mess, process_born_step)
    else:
        mess = bot.send_message(user_id, 'Некорректный ввод. Пожалуйста, выберите один из представленных вариантов ответа')
        bot.register_next_step_handler(mess, process_sex_step)

def process_born_step(message):
    user_id = message.from_user.id
    try:
        datetime.datetime.strptime(message.text, '%d.%m.%Y')
        temp_user_data[user_id]['Дата рождения'] = message.text
        mess = get_mess_education_level(user_id)
        bot.register_next_step_handler(mess, process_education_level_step)
    except ValueError:
        mess = bot.send_message(user_id, 'Некорректный ввод. Пожалуйства введите дату в соответствии с шаблоном (дд.мм.гггг)')
        bot.register_next_step_handler(mess, process_born_step)

def process_education_level_step(message):
    user_id = message.from_user.id
    if message.text in ['Среднее профессиональное', 'Высшее']:
        temp_user_data[user_id]['Образование'] = message.text
        mess = get_mess_profission(user_id)
        bot.register_next_step_handler(mess, process_profession_step)
    elif message.text == 'Студент':
        temp_user_data[user_id]['Образование'] = message.text
        mess = get_mess_course(user_id)
        bot.register_next_step_handler(mess, process_course_step)
    elif message.text == 'Школа':
        temp_user_data[user_id]['Образование'] = message.text
        mess = get_mess_min_salary(user_id)
        bot.register_next_step_handler(mess, process_min_salary_step)
    else:
        mess = bot.send_message(user_id, 'Пожалуйста, выберите один из представленных вариантов ответов')
        bot.register_next_step_handler(mess, process_education_level_step)

def process_course_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['Курс'] = message.text
    mess = get_mess_profission(user_id)
    bot.register_next_step_handler(mess, process_profession_step)

def process_profession_step(message):
    user_id = message.from_user.id
    if message.text not in command_list:
        temp_user_data[user_id]['Специальность'] = message.text
        mess = get_mess_min_salary(user_id)
        bot.register_next_step_handler(mess, process_min_salary_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Попробуйте снова')
        bot.register_next_step_handler(mess, process_profession_step)

def process_min_salary_step(message):
    user_id = message.from_user.id
    if bool(re.match(r"^\d+$", message.text)):
        temp_user_data[user_id]['Минимальная оплата (в час)'] = message.text
        mess = get_mess_hardwork(user_id, temp_user_data[user_id]['Пол'])
        bot.register_next_step_handler(mess, process_hardwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Введите пожалуйста числом')
        bot.register_next_step_handler(mess, process_min_salary_step)

def process_hardwork_step(message):
    user_id = message.from_user.id
    if message.text in ['Да', 'Нет']:
        temp_user_data[user_id]['Тяжелая работа'] = message.text
        mess = get_mess_midwork(user_id,  temp_user_data[user_id]['Пол'])
        bot.register_next_step_handler(mess, process_midwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Выберите один из предложенных вариантов ответа')
        bot.register_next_step_handler(mess, process_hardwork_step)

def process_midwork_step(message):
    user_id = message.from_user.id
    if message.text in ['Да', 'Нет']:
        temp_user_data[user_id]['Работа средней сложности'] = message.text
        mess = get_mess_artwork(user_id)
        bot.register_next_step_handler(mess, process_artwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Выберите один из предложенных вариантов ответа')
        bot.register_next_step_handler(mess, process_midwork_step)

def process_artwork_step(message):
    user_id = message.from_user.id
    if message.text in ['Да', 'Нет']:
        temp_user_data[user_id]['Творческая работа'] = message.text
        mess = get_mess_addwork(user_id)
        bot.register_next_step_handler(mess, process_addwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Выберите один из предложенных вариантов ответа')
        bot.register_next_step_handler(mess, process_artwork_step)

def process_addwork_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['Иные работы'] = message.text
    mess = get_mess_tools(user_id)
    bot.register_next_step_handler(mess, process_tools_step)

def process_tools_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['Инструменты в наличии'] = message.text
    mess = get_mess_phone(user_id)
    bot.register_next_step_handler(mess, process_phone_step)

def process_phone_step(message):
    user_id = message.from_user.id
    if bool(re.match(r"^\d+$", message.text)):
        temp_user_data[user_id]['Телефон'] = message.text
        mess = get_mess_local(user_id)
        bot.register_next_step_handler(mess, process_local_step)
    else:
        mess = bot.send_message(user_id, 'Неверный формат, пожалуйства введите номер в соответствии с шаблоном (формат: 85551116699)')
        bot.register_next_step_handler(mess, process_phone_step)

def process_local_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['Адрес проживания'] = message.text
    photo = temp_user_data[user_id]['Фотография']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_save = types.KeyboardButton('Сохранить')
    btn_restart = types.KeyboardButton('Заполнить заново')
    markup.add(btn_save, btn_restart)
    mess = bot.send_photo(user_id, photo, get_mess_final(user_id), reply_markup=markup)
    bot.register_next_step_handler(mess, process_save_step)
    

def process_save_step(message):
    user_id = message.from_user.id
    if message.text == 'Сохранить':
        data_reg = datetime.date.today()
        photo = temp_user_data[user_id]['Фотография']
        fio = temp_user_data[user_id]['ФИО']
        sex = temp_user_data[user_id]['Пол']
        born = temp_user_data[user_id]['Дата рождения']
        education_level = temp_user_data[user_id]['Образование']
        min_salary = temp_user_data[user_id]['Минимальная оплата (в час)']
        hardwork = temp_user_data[user_id]['Тяжелая работа']
        midwork = temp_user_data[user_id]['Работа средней сложности']
        artwork = temp_user_data[user_id]['Творческая работа']
        addwork = temp_user_data[user_id]['Иные работы']
        tools = temp_user_data[user_id]['Инструменты в наличии']
        phone = temp_user_data[user_id]['Телефон']
        residence_place = temp_user_data[user_id]['Адрес проживания']
        if db.user_is_exist(user_id):
            if 'Курс' in temp_user_data[user_id]:
                course = temp_user_data[user_id]['Курс']
                if 'Специальность' in temp_user_data[user_id]:
                    profession = temp_user_data[user_id]['Специальность']
                    db.edit_user(user_id, data_reg, photo, fio, sex, born, education_level, course, profession, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place)
                    mess = 'Отлично, данные обновлены'
                else:
                    db.edit_user(user_id, data_reg, photo, fio, sex, born, education_level, course, None, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place)
                    mess = 'Отлично, данные обновлены'
            else:
                db.edit_user(user_id, data_reg, photo, fio, sex, born, education_level, None, None, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place)
                mess = 'Отлично, данные обновлены'
            temp_user_data.pop(user_id)
            bot.send_message(user_id, mess, reply_markup=hide_board)
        else:
            if 'Курс' in temp_user_data[user_id]:
                course = temp_user_data[user_id]['Курс']
                if 'Специальность' in temp_user_data[user_id]:
                    profession = temp_user_data[user_id]['Специальность']
                    db.add_user(user_id, data_reg, photo, fio, sex, born, education_level, course, profession, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place)
                else:
                    db.add_user(user_id, data_reg, photo, fio, sex, born, education_level, course, None, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place)
            else:
                db.add_user(user_id, data_reg, photo, fio, sex, born, education_level, None, None, min_salary, hardwork, midwork, artwork, addwork, tools, phone, residence_place)
            mess = 'Отлично, регистрация завершена'
            temp_user_data.pop(user_id)
            bot.send_message(user_id, mess, reply_markup=hide_board)
            print('Зарегистрирован новый пользователь')
    else:
        temp_user_data[user_id] = {}
        mess = bot.send_message(user_id, 'Хорошо, начнем сначала.\nОтправьте пожалуйста свое фото', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_photo_step)

def get_job(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Функция еще находится в разработке')


@bot.message_handler(commands=['profile'])
def profile(message):
    user_id = message.from_user.id
    if db.user_is_exist(user_id): 
        columns = ['Дата регистрации', 'Фотография', 'ФИО', 'Пол', 'Дата рождения', 'Образование', 'Курс', 'Специальность', 'Минимальная оплата (в час)', 'Тяжелый труд', 'Труд средней сложности', 'Творческий труд', 'Иные работы', 'Инструменты в наличии', 'Телефон', 'Адрес проживания', 'Заработок', 'Заказы']
        user_info = db.get_user_info(user_id)
        mess = 'Данные вашего профиля:'
        photo = user_info[1]
        for column, value in zip(columns, user_info):
            if (value != None and column != 'Фотография'):
                mess += '\n{0}: {1}'.format(column, value)
        markup = types.InlineKeyboardMarkup(row_width=3)
        btn_edit = types.InlineKeyboardButton('Заполнить заново', callback_data='restart')
        markup.add(btn_edit)
        bot.send_photo(user_id, photo, mess, reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('Да')
        markup.add(btn)
        mess = bot.send_message(user_id, 'Вы еще не зарегистрированы. Хотите пройти регистрацию?', reply_markup=markup )
        bot.register_next_step_handler(mess, start_reg)


@bot.callback_query_handler(func= lambda call: True)
def response(callback):
    user_id = callback.from_user.id
    if callback.data == 'restart':
        temp_user_data[user_id] = {}
        mess = bot.send_message(user_id, 'Хорошо, начнем! Отправьте свое фото', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_photo_step)
    
    if callback.data == 'finding_job':
        bot.send_message(user_id, 'Функция еще находится в разработке')
            

if __name__ == '__main__':
    db = Telegram_DB()
    bot.infinity_polling()