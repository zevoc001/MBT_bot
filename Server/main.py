from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import aiohttp
import DataBase as DB

from config import TOKEN

ADMIN_ID = "1383046637"  # ID админа

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    # Проверяем, существует ли пользователь в базе данных через API
    user_exists = await DB.get_user_by_tg(user_id)
    if not user_exists:
        await message.answer("Привет! Для начала работы с ботом нужно зарегистрироваться.")
        await register_user(user_id)
    else:
        await message.answer("Добро пожаловать обратно!", reply_markup=main_menu(user_id == ADMIN_ID))

def main_menu(is_admin=False):
    buttons = [
        KeyboardButton("Поиск работы"),
        KeyboardButton("Профиль"),
        KeyboardButton("Написать в поддержку")
    ]
    if is_admin:
        buttons.append(KeyboardButton("Отправить сообщение всем"))
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard

async def register_user(user_id):
    # Добавьте код для регистрации пользователя через API
    pass

async def check_user_in_db(user_id):
    response = aiohttp.ClientResponse
    return False

if __name__ == '__main__':
    dp.start_polling(bot)
