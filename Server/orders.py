import re
import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardRemove)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import get_employers_by_name
from states import StateCreateOrder, StateRegEmployer
from utils import time_is_valid, create_order_mess_full

router = Router()


pass_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Пропустить')]
], resize_keyboard=True)


@router.callback_query(F.data == 'show_orders')
async def show_orders(callback: CallbackQuery, state: FSMContext):
    pass


@router.callback_query(StateCreateOrder.waiting_employer, F.data == 'find_employer')
async def find_employer(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text='Введите название заказчика (часть или полностью)')


@router.message(StateCreateOrder.waiting_employer)
async def find_employer(msg: Message, state: FSMContext):
    employers = await get_employers_by_name(pattern=msg.text)
    employers_keyboard = InlineKeyboardBuilder()
    for employer in employers:
        employers_keyboard.button(text=f"{employer['name']}", callback_data=f"employer_{employer['id']}")
    employers_keyboard.add(
        InlineKeyboardButton(text='🔍 Найти других', callback_data='find_employer'),
        InlineKeyboardButton(text='📋 На главную', callback_data='go_main_menu')
    )
    employers_keyboard.adjust(1)
    await msg.answer('Выберите заказчика', reply_markup=employers_keyboard.as_markup())


@router.callback_query(StateCreateOrder.waiting_employer, lambda c: c.data.startswith('employer_'))
async def waiting_date_order(callback: CallbackQuery, state: FSMContext):
    employer_id = int(callback.data[9:])
    await state.update_data(employer_id=employer_id)
    await callback.message.edit_text('Введите дату выполнения заказа (дд.мм.гггг)')
    await state.set_state(StateCreateOrder.waiting_date_order)


@router.message(StateCreateOrder.waiting_date_order)
async def waiting_tasks(msg: Message, state: FSMContext):
    date_str = msg.text
    pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    if not re.match(pattern, date_str):
        await msg.answer('Неверный ввод. Введите согласно шаблону (дд.мм.гггг)')
    else:
        try:
            date = date_str.split('.')
            date = datetime.date(
                int(date[2]),
                int(date[1]),
                int(date[0])
            ).isoformat()
            await state.update_data(order_date=date)
            await msg.answer('Введите список задач, которые необходимо будет выполнять, через запятую',
                             reply_markup=ReplyKeyboardRemove())
            await state.set_state(StateCreateOrder.waiting_tasks)
        except Exception:
            await msg.answer('Некорректная дата, проверьте ее правильность')


@router.message(StateCreateOrder.waiting_tasks)
async def waiting_place(msg: Message, state: FSMContext):
    await state.update_data(tasks=msg.text)
    await msg.answer('Введите адрес выполнения работы')
    await state.set_state(StateCreateOrder.waiting_place)


@router.message(StateCreateOrder.waiting_place)
async def waiting_tools(msg: Message, state: FSMContext):
    await state.update_data(place=msg.text)
    await msg.answer('Введите необходимые инструменты через запятую', reply_markup=pass_markup)
    await state.set_state(StateCreateOrder.waiting_tools)


@router.message(StateCreateOrder.waiting_tools)
async def waiting_work_form(msg: Message, state: FSMContext):
    if msg.text == 'Пропустить':
        await state.update_data(tools=None)
    else:
        await state.update_data(tools=msg.text)
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Только разнорабочие'),
         KeyboardButton(text='С бригадиром'),
         KeyboardButton(text='Готовая услуга')]
    ], resize_keyboard=True)
    await msg.answer('Выберите тип сотрудничества', reply_markup=markup)
    await state.set_state(StateCreateOrder.waiting_work_form)


@router.message(StateCreateOrder.waiting_work_form)
async def waiting_work_form(msg: Message, state: FSMContext):
    if msg.text not in ['Только разнорабочие', 'С бригадиром', 'Готовая услуга']:
        await msg.answer('Неверный ввод, выберите один из предложенных вариантов')
    else:
        await state.update_data(work_form=msg.text)
        await msg.answer('Введите полную стоимость услуги (без единиц измерения, в рублях)',
                         reply_markup=pass_markup)
        await state.set_state(StateCreateOrder.waiting_price_full)


@router.message(StateCreateOrder.waiting_price_full)
async def waiting_price_full(msg: Message, state: FSMContext):
    if not (msg.text.isdigit() or msg.text == 'Пропустить'):
        await msg.answer('Неверный ввод. Введите только число, без дополнительных обозначений')
    else:
        if msg.text == 'Пропустить':
            await state.update_data(price_full=None)
        else:
            await state.update_data(price_full=int(msg.text))

        # Отправка сообщения
        await msg.answer('Введите стоимость за час работы (без единиц измерения, в рублях, на одного человека)',
                         reply_markup=pass_markup)
        await state.set_state(StateCreateOrder.waiting_price_hour)


@router.message(StateCreateOrder.waiting_price_hour)
async def waiting_price_hour(msg: Message, state: FSMContext):
    if not (msg.text.isdigit() or msg.text == 'Пропустить'):
        await msg.answer('Неверный ввод. Введите только число, без дополнительных обозначений')
    else:
        if msg.text == 'Пропустить':
            await state.update_data(price_hour=None)
        else:
            await state.update_data(price_hour=int(msg.text))

        # Отправка сообщения
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Наличные'),
             KeyboardButton(text='Переводом'),
             KeyboardButton(text='По реквизитам')]
        ], resize_keyboard=True)
        await msg.answer('Выберите форму оплаты', reply_markup=markup)
        await state.set_state(StateCreateOrder.waiting_payment_form)


@router.message(StateCreateOrder.waiting_payment_form)
async def waiting_payment_form(msg: Message, state: FSMContext):
    if msg.text not in ['Наличные', 'Переводом', 'По реквизитам']:
        await msg.answer('Неверный ввод, выберите один из предложенных вариантов')
    else:
        await state.update_data(payment_form=msg.text)
        await msg.answer('Сколько рабочих необходимо? Введите числом', reply_markup=ReplyKeyboardRemove())
        await state.set_state(StateCreateOrder.waiting_need_workers)


@router.message(StateCreateOrder.waiting_need_workers)
async def waiting_need_workers(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer('Неверный ввод. Введите только число, без дополнительных обозначений')
    else:
        await state.update_data(need_workers=msg.text)
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Самостоятельно'),
             KeyboardButton(text='МБТ'),
             KeyboardButton(text='Заказчик')]
        ], resize_keyboard=True)
        await msg.answer('Каким образом рабочие будут добираться?', reply_markup=markup)
        await state.set_state(StateCreateOrder.waiting_transfer_type)


@router.message(StateCreateOrder.waiting_transfer_type)
async def waiting_transfer_type(msg: Message, state: FSMContext):
    if msg.text not in ['Самостоятельно', 'МБТ', 'Заказчик']:
        await msg.answer('Неверный ввод, выберите один из предложенных вариантов')
    else:
        await state.update_data(transfer_type=msg.text)
        await msg.answer('Во сколько быть в точке сбора? (например 17:00)', reply_markup=ReplyKeyboardRemove())
        await state.set_state(StateCreateOrder.waiting_leave_time)


@router.message(StateCreateOrder.waiting_leave_time)
async def waiting_leave_time(msg: Message, state: FSMContext):
    if time_is_valid(msg.text):
        try:
            time_list = msg.text.split(':')
            time = datetime.time(
                hour=int(time_list[0]),
                minute=int(time_list[1]),
            ).isoformat()
            await state.update_data(leave_time=time)

        # Обработка ошибок
        except ValueError as e:
            if 'hour' in str(e):
                await msg.answer('Некорректный час, пожалуйста, введите корректный час (от 00 до 23)')
            elif 'minute' in str(e):
                await msg.answer('Некорректная минута, пожалуйста, введите корректную минуту (от 00 до 59)')
            else:
                await msg.answer('Некорректное время, проверьте его правильность')

    await msg.answer('Во сколько начало работы? (например 17:00)', reply_markup=ReplyKeyboardRemove())
    await state.set_state(StateCreateOrder.waiting_start_time)


@router.message(StateCreateOrder.waiting_start_time)
async def waiting_start_time(msg: Message, state: FSMContext):
    try:
        time_list = msg.text.split(':')
        time = datetime.time(
            hour=int(time_list[0]),
            minute=int(time_list[1]),
        ).isoformat()
        await state.update_data(start_time=time)
        await msg.answer('Во сколько окончание работы? (например 17:00)', reply_markup=ReplyKeyboardRemove())
        await state.set_state(StateCreateOrder.waiting_finish_time)
    except Exception:
        await msg.answer('Некорректное время, проверьте его правильность')


@router.message(StateCreateOrder.waiting_finish_time)
async def waiting_finish_time(msg: Message, state: FSMContext):
    try:
        time_list = msg.text.split(':')
        if len(time_list) != 2 or not all(x.isdigit() for x in time_list):
            raise ValueError("Неверный формат времени. Пожалуйста, используйте HH:MM формат")

        time = datetime.time(
            hour=int(time_list[0]),
            minute=int(time_list[1]),
        ).isoformat()

        await state.update_data(finish_time=time)
        await msg.answer('Во сколько возвращение? (например 17:00)', reply_markup=pass_markup)
        await state.set_state(StateCreateOrder.waiting_back_time)

    except ValueError as e:
        if 'hour' in str(e):
            await msg.answer('Некорректный час, пожалуйста, введите корректный час (от 00 до 23)')
        elif 'minute' in str(e):
            await msg.answer('Некорректная минута, пожалуйста, введите корректную минуту (от 00 до 59)')
        else:
            await msg.answer('Некорректное время, проверьте его правильность')


@router.message(StateCreateOrder.waiting_back_time)
async def waiting_back_time(msg: Message, state: FSMContext):
    if msg.text == 'Пропустить':
        await state.update_data(back_time=None)
    else:
        try:
            time_list = msg.text.split(':')
            time = datetime.time(
                hour=int(time_list[0]),
                minute=int(time_list[1]),
            ).isoformat()
            await state.update_data(back_time=time)
        except Exception:
            await msg.answer('Некорректное время, проверьте его правильность')

    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Да'),
         KeyboardButton(text='Нет')]
    ], resize_keyboard=True)
    await msg.answer('Кормят ли рабочих?', reply_markup=markup)
    await state.set_state(StateCreateOrder.waiting_is_feed)


@router.message(StateCreateOrder.waiting_is_feed)
async def waiting_is_feed(msg: Message, state: FSMContext):
    if msg.text not in ['Да', 'Нет']:
        await msg.answer('Неверный ввод, выберите один из предложенных вариантов')
    else:
        if msg.text == 'Да':
            await state.update_data(is_feed=True)
        if msg.text == 'Нет':
            await state.update_data(is_feed=False)
        await msg.answer('Сколько длится перерыв, минут', reply_markup=ReplyKeyboardRemove())
        await state.set_state(StateCreateOrder.waiting_break_duration)


@router.message(StateCreateOrder.waiting_break_duration)
async def waiting_break_duration(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer('Неверный ввод. Введите только число, без дополнительных обозначений')
    else:
        await state.update_data(break_time=int(msg.text))
        await msg.answer('Введите дополнительную информацию', reply_markup=pass_markup)
        await state.set_state(StateCreateOrder.waiting_add_info)


@router.message(StateCreateOrder.waiting_add_info)
async def waiting_add_info(msg: Message, state: FSMContext):
    if msg.text == 'Пропустить':
        await state.update_data(add_info=None)
    else:
        await state.update_data(add_info=msg.text)

    # Сборка сообщения
    info = await state.get_data()
    order_mess = await create_order_mess_full(**info)
    await state.update_data(order_mess=order_mess)
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отправить', callback_data='send_order'),
         InlineKeyboardButton(text='Заполнить заново', callback_data='btn_create_order')]
    ])
    await msg.answer(order_mess, reply_markup=markup)
