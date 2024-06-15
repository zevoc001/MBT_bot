import datetime
import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from states import StateUserMenu, StateDeleteUser
import database as db
import keyboard, text, config, utils

router = Router()


async def get_menu(access: str) -> InlineKeyboardMarkup:
    if access == 'admin':
        menu = keyboard.main_menu_admin
    elif access == 'leader':
        menu = keyboard.main_menu_leader
    elif access == 'manager':
        menu = keyboard.main_menu_manager
    else:
        menu = keyboard.main_menu_user
    return menu


@router.message(Command('start'))
@router.message(Command('menu'))
async def start_handler(msg: Message, state: FSMContext):
    user = await db.get_user(msg.from_user.id)
    if not user:  # Пользователь не существует
        menu = [
            [InlineKeyboardButton(text='Приступим', callback_data='reg')]
        ]
        menu = InlineKeyboardMarkup(inline_keyboard=menu)
        await msg.answer(
            text='Здравствуйте, это Молодежная Биржа Труда. Мы помогаем людям найти работу и подработку. \n\nДавайте '
                 'немного познакомимся и заполним анкету.',
            reply_markup=menu)
    else:  # Пользователь не существует
        menu = await get_menu(user['access'])
        await msg.answer('Меню', reply_markup=menu)
        await state.set_state(StateUserMenu.main)


@router.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery):
    user_data = await db.get_user(callback.from_user.id)
    msg = 'Ваш профиль:\n'
    for key in text.profile_data:
        column = text.profile_data[key]
        value = user_data[key]
        if value is not None:
            if value is True:
                value = 'Да'
            if value is False:
                value = 'Нет'
            msg += '\n{0}: {1}'.format(column, value)
    menu = keyboard.profile_menu_user
    await callback.message.edit_text(text=msg, reply_markup=menu)
    await callback.answer()


@router.callback_query(F.data == 'save_profile')
async def save_profile(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.update_data(id=user_id)
    await state.update_data(reg_date=datetime.date.today().isoformat())
    user_data = await state.get_data()
    old_user = await db.get_user(user_id)

    # Добавление пользователя или обновление данных
    if old_user:
        new_user = await db.update_user(user=user_data)
    else:
        new_user = await db.add_user(user=user_data)

    # Обработка результата запроса сохранения
    if new_user:
        menu = await get_menu(new_user['access'])
        await callback.message.edit_text(text='Ваши данные успешно сохранены', reply_markup=menu)
        await state.clear()
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Повторить отправку', callback_data='save_profile'),
             InlineKeyboardButton(text='Заполнить заново', callback_data='edit_profile')]
        ])
        await callback.bot.send_message(chat_id=user_id, text='Ошибка сохранения,'
                                                              ' повторите попытку позже или изменить профиль',
                                        reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == 'save_employer')
async def save_employer(callback: CallbackQuery, state: FSMContext):
    employer_data = await state.get_data()

    # Добавление пользователя или обновление данных
    result = await db.add_employer(employer_data)

    # Обработка результата запроса сохранения
    if result:
        menu = keyboard.main_menu_admin
        await callback.message.answer(text='Пользователь успешно добавлен')
        await callback.message.edit_text(text='Главное меню', reply_markup=menu)
        await state.clear()
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Повторить отправку', callback_data='save_profile'),
             InlineKeyboardButton(text='Заполнить заново', callback_data='edit_profile')]
        ])
        await callback.message.answer(text='Ошибка сохранения повторите попытку позже или изменить профиль',
                                      reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == 'delete_profile')
async def delete_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Внимание, при удалении аккаунта, удалятся все данные без возможности '
                                          'восстановления. Для продолжения, введите УДАЛИТЬ АККАУНТ')
    await state.set_state(StateDeleteUser.waiting_delete_text)
    await callback.answer()


@router.message(StateDeleteUser.waiting_delete_text)
async def waiting_delete_text(msg: Message, state: FSMContext):
    if msg.text == 'УДАЛИТЬ АККАУНТ':
        await db.delete_user(msg.from_user.id)
        await msg.answer('Ваш аккаунт удален', reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await msg.answer(text='Неверный ввод. Удаление отменено')
        user = await db.get_user(msg.from_user.id)
        menu = await get_menu(user['access'])
        await msg.answer(text='Главное меню', reply_markup=menu)


@router.callback_query(F.data == 'go_main_menu')
async def backward(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    menu = await get_menu(user['access'])
    await callback.message.edit_text(text='Главное меню', reply_markup=menu)
    await callback.answer()


@router.callback_query(F.data == 'show_orders')
async def show_orders(callback: CallbackQuery):
    orders = await db.get_orders_all()
    for order in orders:
        if order['status'] == 'Active':
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Принять', callback_data=f'get_order_{order["id"]}'), ]
            ])
            order_mess = await utils.create_order_mess_full(**order)
            await callback.message.answer(order_mess, reply_markup=markup)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('get_order_'))
async def get_order(callback: CallbackQuery, state: FSMContext):
    order_id = int(callback.data[10:])
    await state.update_data(order=order_id)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Принять', callback_data='agree_order'),
         InlineKeyboardButton(text='Отклонить', callback_data='go_main_menu')]
    ])
    await callback.message.answer(f'Вы собираетесь принять заказ №{order_id}. Подтвердите прием?', reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == 'my_orders')
async def my_orders(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    orders = await db.get_users_orders(user_id)
    if orders is False:
        await callback.message.answer('У вас нет активных заказов')
        return
    for order in orders:
        if order['status'] == 'Finished':
            continue
        else:
            mess = await utils.create_order_mess_full(**order)
            order_id = order['id']
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Отказаться', callback_data=f'cancel_order:{order_id}')]
            ])
            await callback.message.answer(mess, reply_markup=markup)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('cancel_order:'))
async def my_orders(callback: CallbackQuery):
    user_id = callback.from_user.id
    order_id = int(callback.data.split(':')[1])
    try:
        await db.order_remove_worker(order_id, user_id)
        await callback.message.answer('Вы отказались от заказа')
    except Exception as e:
        logging.error(e)


@router.callback_query(F.data == 'agree_order')
async def agree_order(callback: CallbackQuery, state: FSMContext):
    order = await state.get_data()
    order_id = order['order']
    worker_id = callback.from_user.id
    try:
        await db.order_add_worker(order_id, worker_id)
        await callback.message.answer('Вы приняли заказ. В положенное время ждем вас на месте')
        await state.set_data({})
    except KeyError:
        await callback.message.answer('Вы уже взяли этот заказ')
        await state.set_data({})
    except IndexError:
        await callback.message.answer('К сожалению, все места уже заняты')
    await callback.answer()


@router.callback_query(F.data == 'help')
async def btn_help(callback: CallbackQuery):
    link = config.HELP_BOT_LINK
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Главное меню', callback_data='go_main_menu')]
    ])
    await callback.answer()
    await callback.message.edit_text('Для получения помощи напишите в наш бот: {}'.format(link), reply_markup=markup)


