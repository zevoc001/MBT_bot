# -*- coding: utf-8 -*-
import sys, re, os
import telebot
from pathlib import Path
from dotenv import load_dotenv
import datetime
from telebot import types

dotenv_path = os.path.join(Path().absolute(), 'example.env')
load_dotenv(dotenv_path)
from DataBase import Telegram_DB

bot = telebot.TeleBot(os.getenv('BOT_TOKEN')) # Создаем бота
temp_user_data = {}
hide_board = types.ReplyKeyboardRemove() # Удаление панели
command_list = ['/start', '/profile']


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if db.user_is_exist(user_id):
        info = db.get_user_info(user_id)
        fio = info[2]
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn = types.InlineKeyboardButton('Да', callback_data='finding_job')
        markup.add(btn)
        bot.send_message(user_id, 'Здравствуйте, {0}. Хотите начать поиск работы?'.format(fio), reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton('Да')
        markup.add(btn)
        mess = bot.send_message(user_id, 'Здравствуйте. Мы общественная организация, которая поможет Вам найти основную работу или подработку. Предлагаем Вам заполнить небольную анкету', reply_markup=markup)
        bot.register_next_step_handler(mess, start_reg)

def start_reg(message):
    user_id = message.from_user.id
    temp_user_data[user_id] = {'user_id': user_id}
    mess = bot.send_message(user_id, 'Хорошо, приступим!\nОтправьте пожалуйста Ваше фото', reply_markup=hide_board)
    bot.register_next_step_handler(mess, process_photo_step)

def process_photo_step(message):
    user_id = message.from_user.id
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        photo = bot.download_file(file_info.file_path)
        temp_user_data[user_id]['photo'] = photo
        mess = bot.send_message(user_id, 'Введите пожалуйста Вашу фамилию, имя и отчество', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_fio_step)
    except:
        mess = bot.send_message(user_id, 'Ошибка загрузки! Попробуйте отправить другую фотографию', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_photo_step)

def process_fio_step(message):
    user_id = message.from_user.id
    if bool(re.match(r'^[а-яА-Я\s]+$', message.text)):
        temp_user_data[user_id]['fio'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_male = types.KeyboardButton('Мужской')
        btn_female = types.KeyboardButton('Женский')
        markup.add(btn_male, btn_female)
        mess = bot.send_message(user_id, 'Выберите Ваш пол', reply_markup=markup)
        bot.register_next_step_handler(mess, process_sex_step)
    else:
        mess = bot.send_message(user_id, ' Пожалуйста, попробуйте ввести ФИО иначе.')
        bot.register_next_step_handler(mess, process_fio_step)

def process_sex_step(message):
    user_id = message.from_user.id
    if message.text in ['Мужской', 'Женский']:
        temp_user_data[user_id]['sex'] = message.text
        mess = bot.send_message(user_id, 'Напишите Вашу дату рождения в формате дд.мм.гггг', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_born_step)
    else:
        mess = bot.send_message(user_id, 'Некорректный ввод. Пожалуйста, выберите один из представленных вариантов ответа')
        bot.register_next_step_handler(mess, process_sex_step)

def process_born_step(message):
    user_id = message.from_user.id
    try:
        datetime.datetime.strptime(message.text, '%d.%m.%Y')
        temp_user_data[user_id]['born'] = message.text
        mess = bot.send_message(user_id, 'Введите Ваш контактный номер телефона (формат 89995550011)', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_phone_step)
    except ValueError:
        mess = bot.send_message(user_id, 'Некорректный ввод. Пожалуйства введите дату в соответствии с шаблоном (дд.мм.гггг)')
        bot.register_next_step_handler(mess, process_born_step)

def process_phone_step(message):
    user_id = message.from_user.id
    if bool(re.match(r"^\d+$", message.text)):
        temp_user_data[user_id]['phone'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_school = types.KeyboardButton('Школа')
        btn_college = types.KeyboardButton('Среднее профессиональное')
        btn_high_school = types.KeyboardButton('Высшее')
        btn_student = types.KeyboardButton('Студент')
        markup.add(btn_school, btn_college, btn_high_school, btn_student)
        mess = bot.send_message(user_id, 'Выберите уровень Вашего образования', reply_markup=markup)
        bot.register_next_step_handler(mess, process_education_level_step)
    else:
        mess = bot.send_message(user_id, 'Неверный формат, пожалуйства введите номер в соответствии с шаблоном (формат: 85551116699)')
        bot.register_next_step_handler(mess, process_phone_step)

def process_education_level_step(message):
    user_id = message.from_user.id
    if message.text in ['Среднее профессиональное', 'Высшее']:
        temp_user_data[user_id]['education_level'] = message.text
        mess = bot.send_message(user_id, 'Введите специальность и место обучения', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_profession_step)
    elif message.text == 'Студент':
        temp_user_data[user_id]['education_level'] = message.text
        mess = bot.send_message(user_id, 'Введите номер курса обучения', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_course_step)
    elif message.text == 'Школа':
        temp_user_data[user_id]['education_level'] = message.text
        mess = bot.send_message(user_id, 'За какую сумму в час Вы готовы работать?\nНапишите числом', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_min_salary_step)
    else:
        mess = bot.send_message(user_id, 'Пожалуйста, выберите один из представленных вариантов ответов')
        bot.register_next_step_handler(mess, process_education_level_step)

def process_course_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['course'] = message.text
    mess = bot.send_message(user_id, 'Введите специальность и место обучения', reply_markup=hide_board)
    bot.register_next_step_handler(mess, process_profession_step)

def process_profession_step(message):
    user_id = message.from_user.id
    if message.text not in command_list:
        temp_user_data[user_id]['profession'] = message.text
        mess = bot.send_message(user_id, 'За какую сумму в час Вы готовы работать?\nНапишите числом', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_min_salary_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Попробуйте снова')
        bot.register_next_step_handler(mess, process_profession_step)

def process_min_salary_step(message):
    user_id = message.from_user.id
    if bool(re.match(r"^\d+$", message.text)):
        temp_user_data[user_id]['min_salary'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_yes = types.KeyboardButton('Да')
        btn_no = types.KeyboardButton('Нет')
        markup.add(btn_yes, btn_no)
        mess = bot.send_message(user_id, 'Готовы ли Вы выполнять тяжелую работу (копать, ломать, строить, быть грузчиком)?', reply_markup=markup)
        bot.register_next_step_handler(mess, process_hardwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Введите пожалуйста числом')
        bot.register_next_step_handler(mess, process_min_salary_step)

def process_hardwork_step(message):
    user_id = message.from_user.id
    if message.text in ['Да', 'Нет']:
        temp_user_data[user_id]['hardwork'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_yes = types.KeyboardButton('Да')
        btn_no = types.KeyboardButton('Нет')
        markup.add(btn_yes, btn_no)
        mess = bot.send_message(user_id, 'Готовы ли Вы выполнять работу в сфере обслуживания (уборка, няня, выгул собак ...)?', reply_markup=markup)
        bot.register_next_step_handler(mess, process_midwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Выберите один из предложенных вариантов ответа')
        bot.register_next_step_handler(mess, process_hardwork_step)

def process_midwork_step(message):
    user_id = message.from_user.id
    if message.text in ['Да', 'Нет']:
        temp_user_data[user_id]['midwork'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_yes = types.KeyboardButton('Да')
        btn_no = types.KeyboardButton('Нет')
        markup.add(btn_yes, btn_no)
        mess = bot.send_message(user_id, 'Готовы ли Вы выполнять творческую работу (аниматорство, ведение соцсетей, фото/видеосъемка и.т.д.)?', reply_markup=markup)
        bot.register_next_step_handler(mess, process_artwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Выберите один из предложенных вариантов ответа')
        bot.register_next_step_handler(mess, process_midwork_step)

def process_artwork_step(message):
    user_id = message.from_user.id
    if message.text in ['Да', 'Нет']:
        temp_user_data[user_id]['artwork'] = message.text
        mess = bot.send_message(user_id, 'Напишите пожалуйста, какие специализированные виды работ или услуг Вы выполняли и какими навыками обладаете?', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_addwork_step)
    else:
        mess = bot.send_message(user_id, 'Неверный ввод. Выберите один из предложенных вариантов ответа')
        bot.register_next_step_handler(mess, process_artwork_step)

def process_addwork_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['addwork'] = message.text
    mess = bot.send_message(user_id, 'Какие инструменты, оборудование или аппаратура у Вас имеется (компьютер, дрель, фотоаппарат ...)?', reply_markup=hide_board)
    bot.register_next_step_handler(mess, process_car_step)

def process_car_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['tools'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_car = types.KeyboardButton('Машина')
    btn_mop = types.KeyboardButton('Мопед')
    btn_cycle = types.KeyboardButton('Велосипед')
    btn_esam = types.KeyboardButton('Электросамокат')
    btn_no = types.KeyboardButton('Нет')
    markup.add(btn_car, btn_mop, btn_cycle, btn_esam, btn_no)
    mess = bot.send_message(user_id, 'Выберите Ваше транспортное средство. При его отсутствии выберите Нет', reply_markup=markup)
    bot.register_next_step_handler(mess, process_tools_step)

def process_tools_step(message):
    user_id = message.from_user.id
    temp_user_data[user_id]['car'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_pass = types.KeyboardButton('Пропустить')
    markup.add(btn_pass)
    mess = bot.send_message(user_id, 'Почти закончили! Укажите пожалуйста Ваш адрес проживания (район, улица, дом). Это поможет нам быстрее найти работу поблизости', reply_markup=markup)
    bot.register_next_step_handler(mess, process_local_step)


def process_local_step(message):
    user_id = message.from_user.id
    if message.text != 'Пропустить':
        temp_user_data[user_id]['residence_place'] = message.text
    photo = temp_user_data[user_id]['photo']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_save = types.KeyboardButton('Сохранить')
    btn_restart = types.KeyboardButton('Заполнить заново')
    markup.add(btn_save, btn_restart)
    mess_data = 'Отлично, давайте еще раз проверим, все ли верно. Вот Ваши данные'
    for i in temp_user_data[user_id]:
        if i != 'photo':
            data = temp_user_data[user_id][i]
            mess_data += '\n{}: {}'.format(i, data)
    mess = bot.send_photo(user_id, photo, mess_data, reply_markup=markup)
    bot.register_next_step_handler(mess, process_save_step)

def process_save_step(message):
    user_id = message.from_user.id
    if message.text == 'Сохранить':
        temp_user_data[user_id]['data_reg'] = datetime.date.today()

        if db.user_is_exist(user_id):
            for i in temp_user_data[user_id]:
                if i != 'photo':
                    print(i, temp_user_data[user_id][i])

            db.edit_user(temp_user_data[user_id])
            mess = 'Отлично, данные обновлены'
            temp_user_data.pop(user_id)
            bot.send_message(user_id, mess, reply_markup=hide_board)
        else:
            db.add_user(**temp_user_data[user_id])
            mess = "Спасибо за регистрацию! Если возникли вопросы, можете обращаться\nПо адресу: г.Ставрополь, ул.Михаила Морозова, д.25\nПо телефону: 8-962-453-99-94 (WhatsApp, Telegram)\nПриглашайте друзей, мы будем рады видеть вас в нашей команде!\U0001F91D"
            temp_user_data.pop(user_id)
            bot.send_message(user_id, mess, reply_markup=hide_board)
            print('Зарегистрирован новый пользователь')

    elif message.text == "Заполнить заново":
        temp_user_data[user_id] = {'user_id': user_id}
        mess = bot.send_message(user_id, 'Хорошо, начнем сначала.\nОтправьте пожалуйста свое фото', reply_markup=hide_board)
        bot.register_next_step_handler(mess, process_photo_step)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_save = types.KeyboardButton('Сохранить')
        btn_restart = types.KeyboardButton('Заполнить заново')
        markup.add(btn_save, btn_restart)
        mess = bot.send_message(user_id, 'Пожалуйста, выберите один из предложенных вариантов (Сохранить, Заполнить заново)', reply_markup=markup)
        bot.register_next_step_handler(mess, process_save_step)

def get_job(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Функция еще находится в разработке')


@bot.message_handler(commands=['profile'])
def profile(message):
    user_id = message.from_user.id
    if db.user_is_exist(user_id): 
        columns = ['Дата регистрации', 'Фотография', 'ФИО', 'Пол', 'Дата рождения', 'Образование', 'Курс', 'Специальность', 'Минимальная оплата (в час)', 'Тяжелый труд', 'Труд средней сложности', 'Творческий труд', 'Иные работы', 'Инструменты в наличии', 'Телефон', 'Адрес проживания', 'Заработок', 'Заказы']
        user_info = db.get_user_info(user_id)
        mess = 'Данные Вашего профиля:'
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