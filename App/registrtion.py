import datetime
import re
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove
from App.states import UserRegistration as StateReg
from aiogram.fsm.context import FSMContext
from App.logger_config import get_logger
from App.utils import create_profile_mess

logger = get_logger(__name__)

router = Router()


@router.callback_query(lambda c: c.data in ['reg', 'edit_profile'])
async def start_reg(callback: CallbackQuery, state: FSMContext):
    await state.set_data({})
    await state.set_state(StateReg.name)
    await callback.message.answer(text='Введите свое ФИО', reply_markup=ReplyKeyboardRemove())


@router.message(StateReg.name)
async def set_name(msg: Message, state: FSMContext):
    pattern = r'^[А-ЯЁа-яё]+(-[А-ЯЁа-яё]+)? [А-ЯЁа-яё]+(-[А-ЯЁа-яё]+)? [А-ЯЁа-яё]+(-[А-ЯЁа-яё]+)?$'
    if not re.match(pattern, msg.text):
        await msg.answer('Некорректный ввод, попробуйте ввести иначе')
    else:
        await state.update_data(name=msg.text)
        await state.set_state(StateReg.sex)
        markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Мужской'), KeyboardButton(text='Женский')]],
                                     resize_keyboard=True)
        await msg.answer('Выберите ваш пол', reply_markup=markup)


@router.message(StateReg.sex)
async def set_sex(msg: Message, state: FSMContext):
    await state.update_data(sex=msg.text)
    await state.set_state(StateReg.born)
    await msg.answer(text='Введите вашу дату рождения (формат: дд.мм.гггг)', reply_markup=ReplyKeyboardRemove())


@router.message(StateReg.born)
async def set_born(msg: Message, state: FSMContext):
    pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    if not re.match(pattern, msg.text):
        await msg.answer('Некорректный ввод, попробуйте ввести иначе (например 10.10.2010)')
    else:
        try:
            date = msg.text.split('.')
            born = datetime.date(int(date[2]), int(date[1]), int(date[0])).isoformat()
            await state.update_data(born_date=born)
            await state.set_state(StateReg.skills)
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='Пропустить')],
            ], resize_keyboard=True)
            await msg.answer('Какими навыками вы обладаете? (работа с бетоном, покраска стен и т.д.)',
                             reply_markup=markup)
        except ValueError:
            await msg.answer('Некорректный ввод, попробуйте ввести иначе')


@router.message(StateReg.skills)
async def set_art_work(msg: Message, state: FSMContext):
    if msg.text == 'Пропустить':
        await state.update_data(skills=None)
    else:
        await state.update_data(skills=msg.text)
    await state.set_state(StateReg.tools)
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Пропустить')],
    ], resize_keyboard=True)
    await msg.answer('Какие инструменты у вас есть в наличии? (дрель, мотоблок и т.д.)', reply_markup=markup)


@router.message(StateReg.tools)
async def set_tools(msg: Message, state: FSMContext):
    if msg.text != 'Пропустить':
        await state.update_data(tools=msg.text)
    else:
        await state.update_data(tools=None)
    await state.set_state(StateReg.phone)
    await msg.answer('Введите ваш номер телефона (8хххххххххх)', reply_markup=ReplyKeyboardRemove())


@router.message(StateReg.phone)
async def set_phone(msg: Message, state: FSMContext):
    pattern = r'^8\d{10}$'
    if not re.match(pattern, msg.text):
        await msg.answer(text='Введите телефон в соответствии с форматом (8хххххххххх)')
    else:
        await state.update_data(phone=msg.text)
        await state.set_state(StateReg.wallet)
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Пропустить')],
        ], resize_keyboard=True)
        await msg.answer('Введите номер карты, на которую удобно получать оплату и название банка', reply_markup=markup)


@router.message(StateReg.wallet)
async def set_wallet(msg: Message, state: FSMContext):
    if msg.text != 'Пропустить':
        await state.update_data(wallet=msg.text)
    else:
        await state.update_data(wallet=None)
    await state.set_state(StateReg.transport)
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Машина'), KeyboardButton(text='Велосипед'), KeyboardButton(text='Самокат')],
            [KeyboardButton(text='Другое'), KeyboardButton(text='Нет')]
        ], resize_keyboard=True)
    await msg.answer('Какой транспорт у вас имеется', reply_markup=markup)


@router.message(StateReg.transport)
async def set_transport(msg: Message, state: FSMContext):
    if msg.text not in ['Машина', 'Велосипед', 'Самокат', 'Другое', 'Нет']:
        await msg.answer('Ошибка. Выберите один из предложенных ниже вариантов '
                         '(Машина, Велосипед, Самокат, Другое, Нет)')
    else:
        await state.update_data(transport=msg.text)
        await state.set_state(StateReg.other_info)
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Пропустить')],
            ], resize_keyboard=True
        )
        await msg.answer('Напишите дополнительную информацию о себе, которую хотите сообщить', reply_markup=markup)


@router.message(StateReg.other_info)
async def set_other_info(msg: Message, state: FSMContext):
    if msg.text != 'Пропустить':
        await state.update_data(other_info=msg.text)
    else:
        await state.update_data(other_info=None)

    # Формирование сообщения
    data = await state.get_data()
    mess = await create_profile_mess(data)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Сохранить', callback_data='save_profile'),
             InlineKeyboardButton(text='Заполнить заново', callback_data='edit_profile')],
        ]
    )
    # Отправка сообщения с данными
    await msg.answer(mess, reply_markup=markup)
