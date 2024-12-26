import datetime
import logging
import re

from jinja2 import Environment, FileSystemLoader
from aiogram import Router, F

from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove,
                           ReplyKeyboardMarkup, KeyboardButton)
from App.states import SendingMessage as StateMsg, FindingUser as StateFindUser, AddingEmployer as StateRegEmployer, CreatingOrder as StateCreateOrder
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database as db
import keyboard
import utils

router = Router()

pass_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Пропустить')]
], resize_keyboard=True)


@router.callback_query(F.data == 'find_user')
async def btn_find_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Введите имя (часть или полностью)')
    await state.set_state(StateFindUser.waiting_msg)
    await callback.answer()


@router.message(StateFindUser.waiting_msg)
async def find_user(msg: Message, state: FSMContext):
    users = await db.get_users_by_name(pattern=msg.text)
    users_keyboard = InlineKeyboardBuilder()
    for user in users:
        users_keyboard.button(text=f"{user['name']}", callback_data=f"user:{user['id']}")
    users_keyboard.add(
        InlineKeyboardButton(text='🔍 Найти других', callback_data='find_user'),
        InlineKeyboardButton(text='📋 На главную', callback_data='go_main_menu')
    )
    users_keyboard.adjust(1)
    await msg.answer('Выберите пользователя', reply_markup=users_keyboard.as_markup())
    await state.set_state(StateFindUser.waiting_choose)


@router.callback_query(F.data.startswith('user:'))
async def choose_user(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(':')[1])
    user_data = await db.get_user(user_id)
    msg = await 'Данные профиля:\n' + utils.create_profile_mess(user_data)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Главное меню', callback_data='go_main_menu'),
         InlineKeyboardButton(text='Заблокировать', callback_data=f'block_user:{user_id}')]
    ])
    await callback.answer()
    await callback.message.edit_text(text=msg, reply_markup=markup)
    await state.clear()


@router.callback_query(F.data == 'get_active_orders')
async def get_active_orders(callback: CallbackQuery):
    orders = await db.get_orders_all()
    active_orders = list(filter(lambda order: order['status'] != 'Finished', orders))
    if not active_orders:
        await callback.message.answer('В настоящее время нет активных заказов')

    # Отправка заказов
    for order in active_orders:
        # Добавление кнопок с рабочими
        workers = {column.split('_id_')[1]: user_id for column, user_id in order.items() if column.startswith(
            'worker_telegram_id_')}
        markup = InlineKeyboardBuilder()
        for worker_num, worker_id in workers.items():
            if worker_id is None:
                continue

            markup.add(InlineKeyboardButton(text=f'Рабочий {worker_num}', callback_data=f'user:{worker_id}'))

        # Отправка заказа
        markup.adjust(1)
        markup.add(InlineKeyboardButton(text='Завершить', callback_data=f"finish_order:{order['id']}"))
        order_mess = await utils.create_order_mess_admin(**order)
        await callback.message.answer(order_mess, reply_markup=markup.as_markup())
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('finish_order:'))
async def finish_order(callback: CallbackQuery):
    order_id = int(callback.data.split(':')[1])
    await db.finish_order(order_id)
    await callback.answer()
    await callback.message.answer(f'Заказ №{order_id} завершен')


@router.callback_query(F.data == 'send_order')
async def send_order(callback: CallbackQuery, state: FSMContext):
    order_data = await state.get_data()

    # Добавление заказа
    request = {
        'status': 'Active',
        'reg_date': datetime.date.today().isoformat(),
        'manager_id': callback.from_user.id,
        'employer_id': order_data['employer_id'],
        'order_date': order_data['order_date'],
        'tasks': order_data['tasks'],
        'place': order_data['place'],
        'work_form': order_data['work_form'],
        'price_full': order_data['price_full'],
        'payment_form': order_data['payment_form'],
        'need_workers': order_data['need_workers'],
        'tools': order_data['tools'],
        'transfer_type': order_data['transfer_type'],
        'leave_time': order_data['leave_time'],
        'start_time': order_data['start_time'],
        'finish_time': order_data['finish_time'],
        'back_time': order_data['back_time'],
        'is_feed': order_data['is_feed'],
        'clothes': None,
        'add_info': order_data['add_info'],
        'break_time': order_data['break_time'],
        'task_master': None,
        'worker_telegram_id_1': None,
        'worker_telegram_id_2': None,
        'worker_telegram_id_3': None,
        'worker_telegram_id_4': None,
        'worker_telegram_id_5': None,
        'worker_telegram_id_6': None,
        'worker_telegram_id_7': None,
        'worker_telegram_id_8': None,
        'worker_telegram_id_9': None,
        'worker_telegram_id_10': None,
    }

    order_id = await db.add_order(request)
    request.update(order_id)
    order_mess = await utils.create_order_mess_full(**request)

    # Обработка результата запроса сохранения
    await callback.message.edit_text(text='Заказ успешно опубликован')
    await callback.message.answer(text='Главное меню', reply_markup=keyboard.main_menu_admin)
    await state.clear()
    try:
        # Отправка сообщения
        users = await db.get_users_all()
        mess = order_mess
        for user in users:
            user_id = user['id']
            await callback.bot.send_message(chat_id=user_id, text=mess)
        await state.clear()
    except Exception as e:
        logging.error(f'Не удалось сохранить сообщение: {e}')
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Повторить отправку', callback_data='send_order'),
             InlineKeyboardButton(text='Заполнить заново', callback_data='btn_create_order')]
        ])
        await callback.message.answer(text='Ошибка отправки, повторите попытку позже или измените заявку',
                                      reply_markup=markup)


@router.callback_query(F.data == 'send_mess')
async def btn_send_mess(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Введите сообщение, которое хотите отправить')
    await state.set_state(StateMsg.waiting_msg)
    await callback.answer()


@router.message(StateMsg.waiting_msg)
async def send_mess(msg: Message, state: FSMContext):
    users = await db.get_users_all()
    for user in users:
        user_id = user['id']
        await msg.bot.send_message(chat_id=user_id, text=msg.text)
    await state.clear()
    await msg.answer(text='Сообщение отправлено', reply_markup=keyboard.main_menu_admin)


@router.callback_query(F.data == 'add_employer')
async def waiting_name(callback: CallbackQuery, state: FSMContext):
    await state.set_data({})
    await callback.message.answer('Как зовут заказчика (ФИО)?')
    await state.set_state(StateRegEmployer.waiting_name)


@router.message(StateRegEmployer.waiting_name)
async def set_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer('Из какой он организации?', reply_markup=pass_markup)
    await state.set_state(StateRegEmployer.waiting_company)


@router.message(StateRegEmployer.waiting_company)
async def set_company(msg: Message, state: FSMContext):
    if msg.text == 'Пропустить':
        await state.update_data(company_name=None)
    else:
        await state.update_data(company_name=msg.text)
    await msg.answer('Какой адрес организации?', reply_markup=pass_markup)
    await state.set_state(StateRegEmployer.waiting_address)


@router.message(StateRegEmployer.waiting_address)
async def set_address(msg: Message, state: FSMContext):
    if msg.text == 'Пропустить':
        await state.update_data(company_address=None)
    else:
        await state.update_data(company_address=msg.text)
    await msg.answer('Введите номер телефона заказчика (8ХХХХХХХХХХ)', reply_markup=ReplyKeyboardRemove())
    await state.set_state(StateRegEmployer.waiting_phone)


@router.message(StateRegEmployer.waiting_phone)
async def set_phone(msg: Message, state: FSMContext):
    pattern = r'\d{10,15}$'
    if not re.match(pattern, msg.text):
        await msg.answer('Неверный номер. Введите телефон в соответствии с форматом (8ХХХХХХХХХХ)',
                         reply_markup=ReplyKeyboardRemove())
    else:
        await state.update_data(phone=msg.text)
        await msg.answer('Введите дополнительную информацию о заказчике', reply_markup=pass_markup)
        await state.set_state(StateRegEmployer.waiting_comment)


@router.message(StateRegEmployer.waiting_comment)
async def set_comment(msg: Message, state: FSMContext):
    if msg.text == 'Пропустить':
        await state.update_data(comment=msg.text)
    else:
        await state.update_data(comment=None)

    employer_data = await state.get_data()
    employer = {
        'ФИО': employer_data['name'],
        'Название компании': employer_data['company_name'],
        'Адрес компании': employer_data['company_address'],
        'Телефон': employer_data['phone'],
        'Комментарии': employer_data['comment']
    }
    mess = 'Данные заказчика: \n\n'
    for param, value in employer.items():
        if value is None:
            continue
        mess += f'{param}: {value}\n'
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Сохранить', callback_data='save_employer'),
         InlineKeyboardButton(text='Заполнить заново', callback_data='add_employer')]
    ])
    await msg.answer(mess, reply_markup=markup)


@router.callback_query(F.data == 'add_order')
async def create_offer(callback: CallbackQuery, state: FSMContext):
    await state.set_data({})
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔍 Найти', callback_data='find_employer'),
         InlineKeyboardButton(text='➕ Добавить нового', callback_data='add_employer')],
    ])
    await callback.message.edit_text(text='Найти заказчика или добавить нового?', reply_markup=markup)
    await state.set_state(StateCreateOrder.waiting_employer)