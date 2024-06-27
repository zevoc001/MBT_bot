from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Администратор
main_menu_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Рабочие', callback_data='go_workers_menu'),
     InlineKeyboardButton(text='Работодатели', callback_data='go_customers_menu')],
    [InlineKeyboardButton(text='Заказы', callback_data='go_orders_menu'),
     InlineKeyboardButton(text='Другое', callback_data='go_other_menu'),]
])

# Рабочие
workers_menu_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти', callback_data='go_find_users_menu'),],
    [InlineKeyboardButton(text='Назад', callback_data='go_main_menu'),]
])

# Работодатели
customers_menu_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти', callback_data='go_find_customers_menu'),
     InlineKeyboardButton(text='Добавить', callback_data='add_customer'),],
    [InlineKeyboardButton(text='Назад', callback_data='go_main_menu'),]
])

# Заказы
orders_menu_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Найти', callback_data='go_find_orders_menu'),
     InlineKeyboardButton(text='Создать', callback_data='add_order'),],
    [InlineKeyboardButton(text='Назад', callback_data='go_main_menu'),]
])

# Другое
other_menu_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить сообщение', callback_data='send_mess_to_all'),],
    [InlineKeyboardButton(text='Назад', callback_data='go_main_menu'),]
])

# Рабочие -> Найти
find_users_menu_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ФИО', callback_data='find_users_by_name'),
     InlineKeyboardButton(text='Пол', callback_data='find_users_by_sex'),],
    [InlineKeyboardButton(text='Возраст', callback_data='find_users_by_age'),
     InlineKeyboardButton(text='Телефон', callback_data='find_users_by_phone'),
     InlineKeyboardButton(text='Должность', callback_data='find_users_by_access'),],
    [InlineKeyboardButton(text='Назад', callback_data='go_users_menu'),]
])

# Работодатели -> Найти
find_customers_menu_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ID', callback_data='find_customers_by_id'),
     InlineKeyboardButton(text='ФИО', callback_data='find_customers_by_name'),],
    [InlineKeyboardButton(text='Адрес', callback_data='find_customers_by_address'),
     InlineKeyboardButton(text='Телефон', callback_data='find_customers_by_phone'),
     InlineKeyboardButton(text='Комментарий', callback_data='find_customers_by_comment'),],
    [InlineKeyboardButton(text='Назад', callback_data='go_customers_menu'),]
])

# Заказы -> Найти
find_orders_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Статус', callback_data='find_orders_by_status'),
     InlineKeyboardButton(text='Номер', callback_data='find_customers_by_id'),
     InlineKeyboardButton(text='Дата выполнения', callback_data='find_customers_by_date'),],
    [InlineKeyboardButton(text='Бригадир', callback_data='find_customers_by_taskmaster'),
     InlineKeyboardButton(text='Продолжительность', callback_data='find_customers_by_phone'),
     InlineKeyboardButton(text='Заказчик', callback_data='find_customers_by_employer'),],
    [InlineKeyboardButton(text='Назад', callback_data='go_orders_menu'),]
])

# Профиль рабочего
profile_user_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Редактировать', callback_data='edit_user'),
     InlineKeyboardButton(text='Заблокировать', callback_data='block_user')],
    [InlineKeyboardButton(text='Сделать бригадиром', callback_data='make_user_taskmanager'),],
    [InlineKeyboardButton(text='Назад', callback_data='go_find_users_menu'),]
])





# Пользователи
main_menu_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Профиль', callback_data='to_user_profile'),
     InlineKeyboardButton(text='Мои заказы', callback_data='to_user_orders')],
    [InlineKeyboardButton(text='Доступные заказы', callback_data='get_active_orders'),
     InlineKeyboardButton(text='Написать в поддержку', callback_data='help')],
])

profile_menu_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Редактировать', callback_data='edit_profile'),
     InlineKeyboardButton(text='Удалить', callback_data='delete_profile')],
    [InlineKeyboardButton(text='Главное меню', callback_data='go_main_menu')],
])
