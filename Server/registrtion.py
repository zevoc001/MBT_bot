
class send_message:
    def send_mess_sex(bot, message, next_func):
        user_id = message.from_user.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_male = types.KeyboardButton('Мужской')
        button_female = types.KeyboardButton('Женский')
        markup.add(button_male, button_female)
        mess = bot.send_message(user_id, 'Выберите ваш пол', reply_markup=markup)
        bot.register_next_step_handler(mess, next_func)
        return 0

class Save_data:
    def save_temp_fio(message, user) -> bool:
        user_id = message.from_user.id
        if bool(re.match(r'^[а-яА-Я\s]+$', message.text)):
            temp_user_data[user_id]['fio'] = message.text
            return True
        else: 
            return False