from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Администратор
admin_menu_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👷 Рабочие', callback_data='go_workers_menu'),
     InlineKeyboardButton(text='🏢 Работодатели', callback_data='go_customers_menu')],
    [InlineKeyboardButton(text='📋 Заказы', callback_data='go_orders_menu'),
     InlineKeyboardButton(text='🔧 Другое', callback_data='go_others_menu')]
])

# Рабочие
admin_menu_workers = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔍Найти', callback_data='go_menu_find_users'),],
    [InlineKeyboardButton(text='🔙Назад', callback_data='go_menu_admin'),]
])

# Работодатели
admin_menu_customers = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔍Найти', callback_data='go_menu_find_customers'),
     InlineKeyboardButton(text='➕Добавить', callback_data='add_customer'),],
    [InlineKeyboardButton(text='🔙Назад', callback_data='go_menu_admin'),]
])

# Заказы
admin_menu_orders = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔍Найти', callback_data='go_menu_find_orders'),
     InlineKeyboardButton(text='➕Создать', callback_data='add_order'),],
    [InlineKeyboardButton(text='➕Активные заказы', callback_data='show_active_orders'),],
    [InlineKeyboardButton(text='🔙Назад', callback_data='go_menu_admin'),]
])

# Другое
admin_menu_others = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✉️ Отправить сообщение', callback_data='send_mess_to_all')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='go_menu_admin')]
])

# Рабочие -> Найти
admin_menu_find_users = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👤ФИО', callback_data='find_users_by_name'),
     InlineKeyboardButton(text='🚻Пол', callback_data='find_users_by_sex'),],
    [InlineKeyboardButton(text='🎂Возраст', callback_data='find_users_by_age'),
     InlineKeyboardButton(text='📞Телефон', callback_data='find_users_by_phone'),],
    [InlineKeyboardButton(text='🔙Назад', callback_data='go_workers_menu'),]
])

# Работодатели -> Найти
admin_menu_find_customers = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🆔ID', callback_data='find_customers_by_id'),
     InlineKeyboardButton(text='👤ФИО', callback_data='find_customers_by_name'),],
    [InlineKeyboardButton(text='🏠Адрес', callback_data='find_customers_by_address'),
     InlineKeyboardButton(text='📞Телефон', callback_data='find_customers_by_phone'),
     InlineKeyboardButton(text='💬Комментарий', callback_data='find_customers_by_comment'),],
    [InlineKeyboardButton(text='🔙Назад', callback_data='go_customers_menu'),]
])

# Заказы -> Найти
admin_menu_find_orders = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📋 Статус', callback_data='find_orders_by_status'),
     InlineKeyboardButton(text='🔢 Номер', callback_data='find_customers_by_id'),
     InlineKeyboardButton(text='📅 Дата выполнения', callback_data='find_customers_by_date')],
    [InlineKeyboardButton(text='👷 Бригадир', callback_data='find_customers_by_taskmaster'),
     InlineKeyboardButton(text='⏳ Продолжительность', callback_data='find_customers_by_phone'),
     InlineKeyboardButton(text='👤 Заказчик', callback_data='find_customers_by_employer')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='go_orders_menu')]
])

# Профиль рабочего
admin_user_profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✏️ Редактировать', callback_data='edit_user'),
     InlineKeyboardButton(text='🚫 Заблокировать', callback_data='block_user')],
    [InlineKeyboardButton(text='👷 Сделать бригадиром', callback_data='make_user_taskmanager')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='go_find_users_menu')]
])

# Профиль работодателя
admin_customer_profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✏️ Редактировать', callback_data='edit_customer'),
     InlineKeyboardButton(text='❌ Удалить', callback_data='remove_customer')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='go_menu_find_users')]
])


# Пользователи
user_menu_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👤️Профиль', callback_data='show_profile'),
     InlineKeyboardButton(text='📋Мои заказы', callback_data='get_users_orders')],
    [InlineKeyboardButton(text='📂Доступные заказы', callback_data='get_active_orders'),
     InlineKeyboardButton(text='🆘Написать в поддержку', callback_data='help')],
])

user_menu_profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✏️Редактировать', callback_data='edit_profile'),
     InlineKeyboardButton(text='❌Удалить аккаунт', callback_data='delete_profile')],
    [InlineKeyboardButton(text='🏠Главное меню', callback_data='menu')],
])
