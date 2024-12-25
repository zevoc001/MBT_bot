import re

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove,
                           ReplyKeyboardMarkup, KeyboardButton)

import states


router = Router()

pass_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Пропустить')]
], resize_keyboard=True)


@router.message(states.StateRegEmployer.waiting_name)
async def set_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer('Из какой он организации?', reply_markup=pass_markup)
    await state.set_state(states.StateRegEmployer.waiting_company)


@router.message(states.StateRegEmployer.waiting_company)
async def set_company(msg: Message, state: FSMContext):
    if msg.text == 'Пропустить':
        await state.update_data(company_name=None)
    else:
        await state.update_data(company_name=msg.text)
    await msg.answer('Какой адрес организации?', reply_markup=pass_markup)
    await state.set_state(states.StateRegEmployer.waiting_address)


@router.message(states.StateRegEmployer.waiting_address)
async def set_address(msg: Message, state: FSMContext):
    if msg.text == 'Пропустить':
        await state.update_data(company_address=None)
    else:
        await state.update_data(company_address=msg.text)
    await msg.answer('Введите номер телефона заказчика (8ХХХХХХХХХХ)', reply_markup=ReplyKeyboardRemove())
    await state.set_state(states.StateRegEmployer.waiting_phone)


@router.message(states.StateRegEmployer.waiting_phone)
async def set_phone(msg: Message, state: FSMContext):
    pattern = r'\d{10,15}$'
    if not re.match(pattern, msg.text):
        await msg.answer('Неверный номер. Введите телефон в соответствии с форматом (8ХХХХХХХХХХ)',
                         reply_markup=ReplyKeyboardRemove())
    else:
        await state.update_data(phone=msg.text)
        await msg.answer('Введите дополнительную информацию о заказчике', reply_markup=pass_markup)
        await state.set_state(states.StateRegEmployer.waiting_comment)


@router.message(states.StateRegEmployer.waiting_comment)
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