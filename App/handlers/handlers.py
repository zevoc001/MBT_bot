import datetime
from App.logger_config import get_logger

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from App.states import StateUserMenu, StateDeleteUser
from App import database as db
from App import keyboard, text, config, utils
from App.config import CANCEL_HOUR_ORDER


logger = get_logger(__name__)

router = Router()


@router.message(Command('start'))
@router.message(Command('menu'))
async def start_handler(msg: Message):
    user = await db.get_user(msg.from_user.id)

    if not user:  # Пользователь не существует
        menu = [
            [InlineKeyboardButton(text='Приступим', callback_data='reg')]
        ]
        menu = InlineKeyboardMarkup(inline_keyboard=menu)

        await msg.answer(
            text='Здравствуйте, это Молодежная Биржа Труда. Мы помогаем людям найти работу и подработку. \n\nДавайте '
                 'познакомимся и заполним анкету.',
            reply_markup=menu)
    else:  # Пользователь существует
        if user['access'] == 'admin':
            menu = keyboard.admin_menu_main
        elif user['access'] == 'taskmaster':
            menu = keyboard.user_menu_main
        else:
            menu = keyboard.user_menu_main

        await msg.answer('Главное меню', reply_markup=menu)


@router.message(Command('help'))
@router.callback_query(F.data == 'help')
async def btn_help(callback: CallbackQuery):
    link = config.HELP_BOT_LINK
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Главное меню', callback_data='go_main_menu')]
    ])
    await callback.message.edit_text('Для получения помощи напишите в наш бот: {}'.format(link), reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == 'go_menu_main')
async def start_handler(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)

    if user['access'] == 'admin':
        menu = keyboard.admin_menu_main
    elif user['access'] == 'taskmaster':
        menu = keyboard.user_menu_main
    else:
        menu = keyboard.user_menu_main

    await callback.message.edit_text('Главное меню', reply_markup=menu)


@router.callback_query(F.data == 'go_workers_menu')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_workers
    await callback.message.edit_text(text='Рабочие', reply_markup=menu)


@router.callback_query(F.data == 'go_customers_menu')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_customers
    await callback.message.edit_text(text='Работодатели', reply_markup=menu)


@router.callback_query(F.data == 'go_orders_menu')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_orders
    await callback.message.edit_text(text='Заказы', reply_markup=menu)


@router.callback_query(F.data == 'go_others_menu')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_others
    await callback.message.edit_text(text='Другое', reply_markup=menu)


@router.callback_query(F.data == 'go_menu_find_users')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_users
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)


@router.callback_query(F.data == 'go_menu_find_customers')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_customers
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)


@router.callback_query(F.data == 'go_menu_find_orders')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_orders
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)


@router.callback_query(F.data == 'add_customers')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_customers
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)
