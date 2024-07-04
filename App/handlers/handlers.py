import datetime
from App.logger_config import get_logger

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from App import states
from App import database as db
from App import keyboard, text, config, utils
from App.config import CANCEL_HOUR_ORDER


logger = get_logger(__name__)

router = Router()


@router.message(Command('start'))
@router.message(Command('menu'))
async def start(msg: Message):
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


@router.callback_query(F.data == 'help')
async def help(callback: CallbackQuery):
    link = config.HELP_BOT_LINK
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Главное меню', callback_data='go_main_menu')]
    ])
    await callback.answer()
    await callback.message.edit_text('Для получения помощи напишите в наш бот: {}'.format(link), reply_markup=markup)


@router.callback_query(F.data == 'go_menu_admin')
async def go_main_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_main

    await callback.answer()
    await callback.message.edit_text('Главное меню', reply_markup=menu)


@router.callback_query(F.data == 'go_workers_menu')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_workers
    await callback.answer()
    await callback.message.edit_text(text='Рабочие', reply_markup=menu)


@router.callback_query(F.data == 'go_customers_menu')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_customers
    await callback.answer()
    await callback.message.edit_text(text='Работодатели', reply_markup=menu)


@router.callback_query(F.data == 'go_orders_menu')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_orders
    await callback.answer()
    await callback.message.edit_text(text='Заказы', reply_markup=menu)


@router.callback_query(F.data == 'go_others_menu')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_others
    await callback.answer()
    await callback.message.edit_text(text='Другое', reply_markup=menu)


@router.callback_query(F.data == 'go_menu_find_users')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_users
    await callback.answer()
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)


@router.callback_query(F.data == 'go_menu_find_customers')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_customers
    await callback.answer()
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)


@router.callback_query(F.data == 'go_menu_find_orders')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_orders
    await callback.answer()
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)


@router.callback_query(F.data == 'add_customers')
async def go_workers_menu(callback: CallbackQuery):
    menu = keyboard.admin_menu_find_customers
    await callback.answer()
    await callback.message.edit_text(text='Выберите фильтр поиска', reply_markup=menu)


@router.callback_query(F.data == 'find_users_by_name')
async def btn_find_user(callback: CallbackQuery, state: FSMContext):
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
        InlineKeyboardButton(text='🔍 Найти других', callback_data='find_user'),
        InlineKeyboardButton(text='📋 На главную', callback_data='go_main_menu')
    )
    users_keyboard.adjust(1)
    await msg.answer('Выберите пользователя', reply_markup=users_keyboard.as_markup())
    await state.set_state(states.FindingUser.waiting_choose)


@router.callback_query(F.data == 'find_users_by_sex')
async def btn_find_user(callback: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Мужской', callback_data='find_user_by_sex:Мужской'),
         InlineKeyboardButton(text='Женский', callback_data='find_user_by_sex:Женский'),]
    ])
    await callback.message.edit_text(text='Выберите пол', reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith('find_user_by_sex:'))
async def find_user(callback: CallbackQuery):
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
    await callback.message.answer('Выберите пользователя', reply_markup=users_keyboard.as_markup())


@router.callback_query(F.data == 'find_users_by_age')
async def btn_find_user(callback: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='18 и старше', callback_data='find_user_by_age:>18'),
         InlineKeyboardButton(text='Младше 18', callback_data='find_user_by_age:<18'),]
    ])
    await callback.message.edit_text(text='Выберите возрастную категорию', reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith('find_user_by_age:'))
async def find_user(callback: CallbackQuery):
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
    await callback.message.answer('Выберите пользователя', reply_markup=users_keyboard.as_markup())


@router.callback_query(F.data.startswith('show_user:'))
async def choose_user(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split(':')[1])
    user_data = await db.get_user(user_id)
    msg = 'Данные профиля:\n'
    for key in text.profile_data:
        column = text.profile_data[key]
        value = user_data[key]
        if value is not None:
            if value is True:
                value = 'Да'
            if value is False:
                value = 'Нет'
            msg += '\n{0}: {1}'.format(column, value)
    markup = InlineKeyboardBuilder()
    markup.button(text='🔙 Назад', callback_data='go_menu_find_users')
    if user_data['status'] != 'blocked':
        markup.button(text='Заблокировать', callback_data=f'block_user:{user_id}')
    else:
        markup.button(text='Разблокировать', callback_data=f'unblock_user:{user_id}')
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
    await callback.message.answer('Пользователь заблокирован')
    await go_main_menu(callback)


@router.callback_query(F.data.startswith('unblock_user:'))
async def block_user(callback: CallbackQuery):
    user_id = int(callback.data.split(':')[1])
    user = await db.get_user(user_id)
    user['status'] = ''
    await db.update_user(user)
    await callback.answer()
    await callback.message.answer('Пользователь разблокирован')
    await go_main_menu(callback)


@router.callback_query(F.data == 'show_active_orders')
async def get_active_orders(callback: CallbackQuery):
    orders = await db.get_orders_all()
    active_orders = list(filter(lambda order: order['status'] != 'Finished', orders))
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
        logger.error(f'Не удалось сохранить сообщение: {e}')
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Повторить отправку', callback_data='send_order'),
             InlineKeyboardButton(text='Заполнить заново', callback_data='btn_create_order')]
        ])
        await callback.message.answer(text='Ошибка отправки, повторите попытку позже или измените заявку',
                                      reply_markup=markup)
