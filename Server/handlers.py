from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from states import Reg
from aiogram.fsm.context import FSMContext
import database as db
import keyboard

router = Router()


@router.message(Command('start'))
async def start_handler(msg: Message):
    user = await db.get_user_by_tg(msg.from_user.id)
    if not user:  # Пользователь не существует
        menu = [
            [InlineKeyboardButton(text='Да', callback_data='reg')]
        ]
        menu = InlineKeyboardMarkup(inline_keyboard=menu)
        await msg.answer(
            'Здравствуйте, для продолжения работы необходимо пройти регистрацию. \n **Начать регистрацию?**',
            reply_markup=menu)
    else:  # Пользователь существует
        user = user[0]
        if user['access'] == 'admin':
            menu = keyboard.main_menu_admin
        elif user['access'] == 'leader':
            menu = keyboard.main_menu_leader
        elif user['access'] == 'manager':
            menu = keyboard.main_menu_manager
        else:
            menu = keyboard.main_menu_leader
        await msg.answer('Меню', reply_markup=menu)



