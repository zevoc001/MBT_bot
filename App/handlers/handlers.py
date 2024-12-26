import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext

import states
import database as db
import keyboard, config, utils
from database import UserNotFound
from config import CANCEL_HOUR_ORDER


router = Router()


@router.message(Command('start'))
@router.message(Command('go_main_menu'))
@router.message(Command('menu'))
async def start(msg: Message):
    try:
        user = await db.get_user(msg.from_user.id)
        if user['access'] == 'admin':
            menu = keyboard.admin_menu_main
        elif user['access'] == 'taskmaster':
            menu = keyboard.user_menu_main
        else:
            menu = keyboard.user_menu_main

        await msg.answer('Главное меню', reply_markup=menu)
    except Exception as e:  # Пользователь не существует
        menu = [
            [InlineKeyboardButton(text='Приступим', callback_data='reg')]
        ]
        menu = InlineKeyboardMarkup(inline_keyboard=menu)

        await msg.answer(
            text='Здравствуйте, это Молодежная Биржа Труда. Мы помогаем людям найти работу и подработку. \n\nДавайте '
                 'познакомимся и заполним анкету.',
            reply_markup=menu)


@router.callback_query(F.data == 'help')
async def go_help(callback: CallbackQuery):
    link = config.HELP_BOT_LINK
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Главное меню', callback_data='go_main_menu')]
    ])
    await callback.answer()
    await callback.message.edit_text('Для получения помощи напишите в наш бот: {}'.format(link), reply_markup=markup)


@router.callback_query(F.data == 'go_menu_admin')
async def go_menu_admin(callback: CallbackQuery):
    menu = keyboard.admin_menu_main

    await callback.answer()
    await callback.message.edit_text('Главное меню', reply_markup=menu)


@router.callback_query(F.data == 'go_workers_menu')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_workers
    await callback.answer()
    await callback.message.edit_text(text='Рабочие', reply_markup=menu)


@router.callback_query(F.data == 'go_customers_menu')
async def go_customers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_customers
    await callback.answer()
    await callback.message.edit_text(text='Работодатели', reply_markup=menu)


@router.callback_query(F.data == 'go_orders_menu')
async def go_orders_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_orders
    await callback.answer()
    await callback.message.edit_text(text='Заказы', reply_markup=menu)


@router.callback_query(F.data == 'go_others_menu')
async def go_others_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_others
    await callback.answer()
    await callback.message.edit_text(text='Другое', reply_markup=menu)


@router.callback_query(F.data == 'go_menu_find_users')
async def go_menu_find_users(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_users
    await callback.answer()
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)


@router.callback_query(F.data == 'go_menu_find_customers')
async def go_menu_find_customers(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_customers
    await callback.answer()
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)


@router.callback_query(F.data == 'go_menu_find_orders')
async def go_menu_find_orders(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_orders
    await callback.answer()
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)


@router.callback_query(F.data == 'add_customers')
async def add_customers(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_customers
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)
    await callback.answer()


@router.callback_query(F.data == 'find_users_by_name')
async def find_users_by_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Введите имя (часть или полностью)')
    await state.set_state(states.FindingUser.waiting_msg)
    await callback.answer()


@router.message(states.FindingUser.waiting_msg)
async def find_user(msg: Message, state: FSMContext):
    users = await db.get_users_by_name(pattern=msg.text)
    users_keyboard = InlineKeyboardBuilder()
    for user in users:
        users_keyboard.button(text=f"{user['name']}", callback_data=f"show_user:{user['id']}")
    users_keyboard.add(
        InlineKeyboardButton(text='🔍 Найти других', callback_data='go_menu_find_users'),
        InlineKeyboardButton(text='📋 На главную', callback_data='go_menu_admin')
    )
    users_keyboard.adjust(1)
    await msg.answer('Выберите пользователя', reply_markup=users_keyboard.as_markup())
    await state.set_state(states.FindingUser.waiting_choose)


@router.callback_query(F.data == 'find_users_by_sex')
async def find_users_by_sex(callback: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Мужской', callback_data='find_user_by_sex:Мужской'),
         InlineKeyboardButton(text='Женский', callback_data='find_user_by_sex:Женский'),]
    ])
    await callback.message.edit_text(text='Выберите пол', reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith('find_user_by_sex:'))
async def find_user_by_sex(callback: CallbackQuery):
    sex = callback.data.split(':')[1]
    users = await db.get_users_by_sex(sex=sex)
    users_keyboard = InlineKeyboardBuilder()
    for user in users:
        users_keyboard.button(text=f"{user['name']}", callback_data=f"show_user:{user['id']}")
    users_keyboard.add(
        InlineKeyboardButton(text='🔍 Найти других', callback_data='go_menu_find_users'),
        InlineKeyboardButton(text='📋 На главную', callback_data='go_menu_admin')
    )
    users_keyboard.adjust(1)
    await callback.answer()
    await callback.message.edit_text('Выберите пользователя', reply_markup=users_keyboard.as_markup())


@router.callback_query(F.data == 'find_users_by_age')
async def find_users_by_age(callback: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='18 и старше', callback_data='find_user_by_age:>18'),
         InlineKeyboardButton(text='Младше 18', callback_data='find_user_by_age:<18'),]
    ])
    await callback.message.edit_text(text='Выберите возрастную категорию', reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith('find_user_by_age:'))
async def find_user_by_age(callback: CallbackQuery):
    pattern = callback.data.split(':')[1]
    age = int(pattern[1:])
    sign = pattern[:1]
    users = await db.get_users_by_age(age=age, sign=sign)
    users_keyboard = InlineKeyboardBuilder()
    for user in users:
        today = datetime.date.today()
        born_date = datetime.date.fromisoformat(user['born_date'])
        age = int((today - born_date).total_seconds() / 31536000)
        users_keyboard.button(text=f"Возраст: {age}, {user['name']}", callback_data=f"show_user:{user['id']}")
    users_keyboard.add(
        InlineKeyboardButton(text='🔍 Найти других', callback_data='go_menu_find_users'),
        InlineKeyboardButton(text='📋 На главную', callback_data='go_menu_admin')
    )
    users_keyboard.adjust(1)
    await callback.answer()
    await callback.message.edit_text('Выберите пользователя', reply_markup=users_keyboard.as_markup())


@router.callback_query(F.data.startswith('show_user:'))
async def show_user(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(':')[1])
    user_data = await db.get_user(user_id)
    msg = await utils.create_profile_mess(user_data)

    markup = InlineKeyboardBuilder()

    markup.button(text='🔙 Назад', callback_data='go_menu_find_users')
    if user_data['status'] != 'blocked':
        markup.button(text='Заблокировать', callback_data=f'block_user:{user_id}')
    else:
        markup.button(text='Разблокировать', callback_data=f'unblock_user:{user_id}')

    if user_data['access'] != 'foreman':
        markup.button(text='Сделать бригадиром', callback_data=f'grow_up_to_foreman:{user_id}')
    if user_data['access'] != 'admin':
        markup.button(text='Сделать админом', callback_data=f'grow_up_to_admin:{user_id}')
    if user_data['access'] != 'user':
        markup.button(text='Сделать разнорабочим', callback_data=f'grow_up_to_worker:{user_id}')
    markup.adjust(2, repeat=True)
    await callback.answer()
    await callback.message.edit_text(text=msg, reply_markup=markup.as_markup())
    await state.clear()


@router.callback_query(F.data.startswith('block_user:'))
async def block_user(callback: CallbackQuery):
    user_id = int(callback.data.split(':')[1])
    user = await db.get_user(user_id)
    user['status'] = 'blocked'
    await db.update_user(user)
    await callback.answer()
    await callback.message.edit_text('Пользователь заблокирован')

    markup = keyboard.admin_menu_main
    await callback.message.answer('Главное меню', reply_markup=markup)


@router.callback_query(F.data.startswith('unblock_user:'))
async def unblock_user(callback: CallbackQuery):
    user_id = int(callback.data.split(':')[1])
    user = await db.get_user(user_id)
    user['status'] = ''
    await db.update_user(user)
    await callback.answer()
    await callback.message.edit_text('Пользователь разблокирован')

    markup = keyboard.admin_menu_main
    await callback.message.answer('Главное меню', reply_markup=markup)


@router.callback_query(F.data.startswith('grow_up_to_worker:'))
async def grow_up_to_foreman(callback: CallbackQuery):
    user_id = int(callback.data.split(':')[1])
    user = await db.get_user(user_id)
    user['access'] = 'worker'
    await db.update_user(user)
    await callback.answer()
    await callback.message.edit_text('Пользователь назначен администратором')

    markup = keyboard.admin_menu_main
    await callback.message.answer('Главное меню', reply_markup=markup)


@router.callback_query(F.data.startswith('grow_up_to_foreman:'))
async def grow_up_to_foreman(callback: CallbackQuery):
    user_id = int(callback.data.split(':')[1])
    user = await db.get_user(user_id)
    user['access'] = 'foreman'
    await db.update_user(user)
    await callback.answer()
    await callback.message.edit_text('Пользователь назначен бригадиром')

    markup = keyboard.admin_menu_main
    await callback.message.answer('Главное меню', reply_markup=markup)


@router.callback_query(F.data.startswith('grow_up_to_admin:'))
async def grow_up_to_foreman(callback: CallbackQuery):
    user_id = int(callback.data.split(':')[1])
    user = await db.get_user(user_id)
    user['access'] = 'foreman'
    await db.update_user(user)
    await callback.answer()
    await callback.message.edit_text('Пользователь назначен администратором')

    markup = keyboard.admin_menu_main
    await callback.message.answer('Главное меню', reply_markup=markup)


@router.callback_query(F.data == 'show_active_orders')
async def get_active_orders(callback: CallbackQuery):
    orders = await db.get_orders_all()
    active_orders = list(filter(lambda order_data: order_data['status'] != 'Finished', orders))
    if not active_orders:
        await callback.message.answer('В настоящее время нет активных заказов')

    # Отправка сообщения
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


@router.callback_query(F.data == 'add_order')
async def create_offer(callback: CallbackQuery, state: FSMContext):
    await state.set_data({})
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔍 Найти', callback_data='find_employer'),
         InlineKeyboardButton(text='➕ Добавить нового', callback_data='add_employer')],
    ])
    await callback.message.edit_text(text='Найти заказчика или добавить нового?', reply_markup=markup)
    await state.set_state(states.CreatingOrder.waiting_employer)


@router.callback_query(F.data == 'save_order')
async def save_order(callback: CallbackQuery, state: FSMContext):
    order_data = await state.get_data()

    # Добавление заказа
    request = {
        'status': 'saved',
        'reg_date': datetime.date.today().isoformat(),
        'manager_id': callback.from_user.id,
        'customer_id': order_data.get('customer_id'),
        'order_date': order_data.get('order_date'),
        'start_time': order_data.get('start_time'),
        'finish_time': order_data.get('finish_time'),
        'transfer_type': order_data.get('transfer_type'),
        'order_cost': order_data.get('order_cost'),
        'leave_place': order_data.get('leave_place'),
        'leave_time': order_data.get('leave_time'),
        'workers_price_hour': order_data.get('workers_price_hour'),
        'need_foreman': order_data.get('need_foreman'),
        'payment_form': order_data.get('payment_form'),
        'break_duration': order_data.get('break_duration'),
        'count_worker': order_data.get('count_worker'),
        'order_place': order_data.get('order_place'),
        'tasks': order_data.get('tasks'),
        'tools': order_data.get('tools'),
        'extra_info': order_data.get('extra_info'),
    }
    order_id = await db.add_order(request)

    await callback.message.edit_text(f'Заказ №{order_id} успешно сохранен')
    markup = keyboard.admin_menu_main
    await callback.message.answer('Главное меню', reply_markup=markup)


@router.callback_query(F.data == 'publish_order')
async def publish_order(callback: CallbackQuery, state: FSMContext):
    order_data = await state.get_data()

    # Сохранение заказа в БД
    request = {
        'status': 'published_for_foremen' if order_data.get('need_foreman') else 'published_for_workers',
        'reg_date': datetime.date.today().isoformat(),
        'manager_id': callback.from_user.id,
        'customer_id': order_data.get('customer_id'),
        'order_date': order_data.get('order_date'),
        'start_time': order_data.get('start_time'),
        'finish_time': order_data.get('finish_time'),
        'transfer_type': order_data.get('transfer_type'),
        'order_cost': order_data.get('order_cost'),
        'leave_place': order_data.get('leave_place'),
        'leave_time': order_data.get('leave_time'),
        'workers_price_hour': order_data.get('workers_price_hour'),
        'need_foreman': order_data.get('need_foreman'),
        'payment_form': order_data.get('payment_form'),
        'break_duration': order_data.get('break_duration'),
        'count_worker': order_data.get('count_worker'),
        'order_place': order_data.get('order_place'),
        'tasks': order_data.get('tasks'),
        'tools': order_data.get('tools'),
        'extra_info': order_data.get('extra_info'),
    }
    order_id = await db.add_order(request)

    # Создание сообщения пользователям
    request.update({'order_id': order_id})
    order_mess = await utils.create_order_mess_full(**request)

    # Отправка сообщения
    try:
        users = await db.get_users_all()
        mess = order_mess
        for user in users:
            user_id = user['id']
            await callback.bot.send_message(chat_id=user_id, text=mess)
        await state.clear()
        await callback.message.edit_text(text='Заказ успешно опубликован')
    except Exception as e:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Повторить отправку', callback_data='send_order'),
             InlineKeyboardButton(text='Заполнить заново', callback_data='add_order')]
        ])
        await callback.message.answer(text='Ошибка отправки, повторите попытку позже или измените заявку',
                                      reply_markup=markup)


@router.callback_query(F.data == 'save_profile')
async def save_profile(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await state.update_data(id=user_id)
    await state.update_data(reg_date=datetime.date.today().isoformat())
    await state.update_data(access='user')
    user_data = await state.get_data()
    print(user_data)

    # Попытка обновить текущего пользователя
    try:
        user = await db.update_user(user=user_data)
        if user['access'] == 'admin':
            menu = keyboard.admin_menu_main
        elif user['access'] == 'taskmaster':
            menu = keyboard.user_menu_main
        else:
            menu = keyboard.user_menu_main
        await callback.message.answer(text='Ваши данные успешно обновлены')
        await callback.message.edit_text(text='Главное меню', reply_markup=menu)

    # Создание нового пользователя
    except UserNotFound:
        await db.add_user(user=user_data)

        menu = keyboard.user_menu_main
        await state.clear()
        await callback.message.edit_text(
            text='Ваши данные успешно сохранены.\n\nПодписывайтесь на нас в соцсетях.\nVK: https://vk.com/id849751646\n',
            reply_markup=menu)

    # Ошибка сохранения или обновления
    except Exception as e:
        print(e)
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Повторить отправку', callback_data='save_profile'),
             InlineKeyboardButton(text='Заполнить заново', callback_data='edit_profile')]
        ])
        await callback.bot.send_message(chat_id=user_id, text='Ошибка сохранения,'
                                                              ' повторите попытку позже или изменить профиль',
                                        reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data == 'show_profile')
async def show_profile(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_data = await db.get_user(user_id)
    mess = await utils.create_profile_mess(user_data)
    markup = keyboard.user_menu_profile
    await callback.message.edit_text(text=mess, reply_markup=markup)


@router.callback_query(F.data == 'get_users_orders')
async def get_users_orders(callback: CallbackQuery):
    user_id = callback.from_user.id
    orders = await db.get_users_orders(user_id)

    for order in orders:
        mess = await utils.create_order_mess_full(**order)
        order_id = order['id']
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='❌ Отказаться', callback_data=f'cancel_order:{order_id}')]
        ])
        await callback.message.answer(text=mess)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('get_order:'))
async def get_order(callback: CallbackQuery, state: FSMContext):
    order_id = int(callback.data[10:])
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Принять', callback_data=f'agree_order:{order_id}'),
         InlineKeyboardButton(text='Отклонить', callback_data='go_main_menu')]
    ])
    await callback.message.answer(f'Вы собираетесь принять заказ №{order_id}. Подтвердите прием?', reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith('agree_order:'))
async def agree_order(callback: CallbackQuery, state: FSMContext):
    order_id = int(callback.data.split(':')[1])
    user_id = callback.from_user.id
    workers = await db.get_order_workers(order_id)
    # Закреплен ли пользователь уже за заказом
    if user_id in workers:
        await callback.message.edit_text('Вы уже закреплены за этим заказом')
        return

    # Если пользователь еще не закреплен
    order = await db.get_order(order_id)
    plan_workers = order['count_workers']
    if len(workers) < plan_workers:
        await db.order_add_worker(order_id, user_id)
        await callback.message.answer('Вы приняли заказ. В положенное время ждем вас на месте')
    else:
        await callback.message.answer('К сожалению, все места уже заняты')
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith('cancel_order:'))
async def cancel_order(callback: CallbackQuery):
    user_id = callback.from_user.id
    order_id = int(callback.data.split(':')[1])
    order = await db.get_order(order_id)
    try:
        # Разница в днях относительно начала заказа
        today = datetime.datetime.now()
        order_date = datetime.date.fromisoformat(order['order_date'])
        order_start_time = datetime.time.fromisoformat(order['start_time'])
        order_time = datetime.datetime.combine(order_date, order_start_time)
        left_hour = (order_time - today).total_seconds() / 3600
        # Если до начала осталось более установленного времени
        if left_hour >= CANCEL_HOUR_ORDER:
            await db.order_remove_worker(order_id, user_id)
            await callback.message.answer('Вы отказались от заказа')
        else:
            await callback.message.answer('Вы не можете отказаться от заказа менее чем за {} часа до его начала. '
                                          'Для отказа, звоните по номеру 8(8652)-222-007'.format(CANCEL_HOUR_ORDER))
    except Exception as e:
        await callback.message.answer('Не удалось отказаться от заказа, позвоните по номеру 8(8652)-222-007')
    await callback.answer()
