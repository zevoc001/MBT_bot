from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поиск клиента', callback_data='find_user'),
     InlineKeyboardButton(text='Активные заказы', callback_data='get_active_orders')],
    [InlineKeyboardButton(text='Выложить заказ', callback_data='create_order'),
     InlineKeyboardButton(text='Отправить сообщение', callback_data='send_mess')],
    [InlineKeyboardButton(text='Добавить заказчика', callback_data='add_employer')]
])

main_menu_manager = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Профиль соискателя', callback_data='profile'),
     InlineKeyboardButton(text='Активные вакансии', callback_data='offers')],
    [InlineKeyboardButton(text='Выложить вакансию', callback_data='create_offer'),
     InlineKeyboardButton(text='Отправить сообщение', callback_data='send_mess')]
])

main_menu_leader = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Профиль', callback_data='profile'),
     InlineKeyboardButton(text='Мои заказы', callback_data='offers')],
    [InlineKeyboardButton(text='Все заказы', callback_data='create_offer'),
     InlineKeyboardButton(text='Написать бригаде', callback_data='send_mess')],
    [InlineKeyboardButton(text='Написать в поддержку', callback_data='create_offer')]
])

# User
main_menu_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Профиль', callback_data='profile'),
     InlineKeyboardButton(text='Мои заказы', callback_data='my_orders')],
    [InlineKeyboardButton(text='Посмотреть заказы', callback_data='show_orders'),
     InlineKeyboardButton(text='Написать в поддержку', callback_data='help')],
])

profile_menu_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Редактировать', callback_data='edit_profile'),
     InlineKeyboardButton(text='Удалить', callback_data='delete_profile')],
    [InlineKeyboardButton(text='Главное меню', callback_data='go_main_menu')],
])
