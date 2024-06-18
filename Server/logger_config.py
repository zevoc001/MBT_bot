import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Создаем директорию для логов, если она не существует
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Указываем путь к лог-файлу
log_file = os.path.join(log_dir, 'app.log')

# Настраиваем обработчик для ротации логов ежедневно
handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=30)
handler.suffix = "%Y-%m-%d"  # Суффикс для файлов логов

# Настраиваем форматер
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


# Создаем функцию для получения логгера
def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:  # Чтобы избежать добавления обработчика несколько раз
        logger.addHandler(handler)
    return logger
