import os

from dotenv import load_dotenv

load_dotenv('../config.env')
# Токен бота Телеграм
TOKEN = os.getenv('TOKEN')

# URL адрес сервера базы данных
DB_URL = os.getenv('DB_URL')

# Токен доступа к БД
DB_ACCESS_TOKEN = os.getenv('DB_ACCESS_TOKEN')

# Ссылка на бота поддержки
HELP_BOT_LINK = os.getenv('HELP_BOT_LINK')

# Время до запрета отказа от заказа для пользователей
CANCEL_HOUR_ORDER = os.getenv('CANCEL_HOUR_ORDER')
