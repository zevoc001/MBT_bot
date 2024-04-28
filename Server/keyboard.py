from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu_admin = [
    [InlineKeyboardButton(text='Профиль соискателя', callback_data='profile'),
     InlineKeyboardButton(text='Активные вакансии', callback_data='offers')],
    [InlineKeyboardButton(text='Выложить вакансию', callback_data='create_offer'),
     InlineKeyboardButton(text='Отправить сообщение', callback_data='send_mess')]
]
main_menu_admin = InlineKeyboardMarkup(inline_keyboard=main_menu_admin)

main_menu_manager = [
    [InlineKeyboardButton(text='Профиль соискателя', callback_data='profile'),
     InlineKeyboardButton(text='Активные вакансии', callback_data='offers')],
    [InlineKeyboardButton(text='Выложить вакансию', callback_data='create_offer'),
     InlineKeyboardButton(text='Отправить сообщение', callback_data='send_mess')]
]
main_menu_manager = InlineKeyboardMarkup(inline_keyboard=main_menu_manager)

main_menu_leader = [
    [InlineKeyboardButton(text='Профиль', callback_data='profile'),
     InlineKeyboardButton(text='Мои заказы', callback_data='offers')],
    [InlineKeyboardButton(text='Все заказы', callback_data='create_offer'),
     InlineKeyboardButton(text='Написать бригаде', callback_data='send_mess')],
    [InlineKeyboardButton(text='Написать в поддержку', callback_data='create_offer')]
]
main_menu_leader = InlineKeyboardMarkup(inline_keyboard=main_menu_leader)

main_menu_user = [
    [InlineKeyboardButton(text='Профиль', callback_data='profile'),
     InlineKeyboardButton(text='Мои заказы', callback_data='offers')],
    [InlineKeyboardButton(text='Все заказы', callback_data='create_offer'),
     InlineKeyboardButton(text='Написать в поддержку', callback_data='send_mess')],
]
main_menu_user = InlineKeyboardMarkup(inline_keyboard=main_menu_user)