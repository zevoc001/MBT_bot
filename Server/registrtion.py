import datetime
import re
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, \
    KeyboardButton, ReplyKeyboardRemove
from states import StateReg
from aiogram.fsm.context import FSMContext
from text import profile_data
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = Router()


@router.callback_query(lambda c: c.data in ['reg', 'edit_profile'])
async def start_reg(callback: CallbackQuery, state: FSMContext):
    await state.set_data({})
    await state.set_state(StateReg.name)
    await callback.message.answer(text='Введите свое ФИО', reply_markup=ReplyKeyboardRemove())


@router.message(StateReg.name)
async def set_name(msg: Message, state: FSMContext):
    pattern = r'^[А-ЯЁа-яё]+ [А-ЯЁа-яё]+ [А-ЯЁа-яё]+$'
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
            await state.set_state(StateReg.residence)
            markup = ReplyKeyboardMarkup(keyboard=[
                [KeyboardButton(text='Пропустить')],
            ], resize_keyboard=True)
            await msg.answer('Введите место жительства', reply_markup=markup)
        except ValueError:
            await msg.answer('Некорректный ввод, попробуйте ввести иначе')


@router.message(StateReg.residence)
async def set_residence(msg: Message, state: FSMContext):
    if msg.text != 'Пропустить':
        await state.update_data(residence=msg.text)
    else:
        await state.update_data(residence=None)
    await state.set_state(StateReg.education)
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Высшее'),
         KeyboardButton(text='Среднее профессиональное')],
        [KeyboardButton(text='Среднее специальное'),
         KeyboardButton(text='Среднее полное')],
        [KeyboardButton(text='Студент')]
    ], resize_keyboard=True)
    await msg.answer('Какое у вас образование', reply_markup=markup)


@router.message(StateReg.education)
async def set_education(msg: Message, state: FSMContext):
    if msg.text in ['Высшее', 'Среднее профессиональное']:
        await state.update_data(education=msg.text)
        await state.set_state(StateReg.profession)
        await msg.answer('Введите вашу специальность', reply_markup=ReplyKeyboardRemove())
    elif msg.text in ['Среднее специальное', 'Среднее полное']:
        await state.update_data(education=msg.text)
        await state.set_state(StateReg.salary)
        await msg.answer('Введите минимальную желаемую оплату труда (рублей в час)', reply_markup=ReplyKeyboardRemove())
    elif msg.text == 'Студент':
        await state.update_data(education=msg.text)
        await state.set_state(StateReg.course)
        await msg.answer('На каком курсе вы учитесь', reply_markup=ReplyKeyboardRemove())
    else:
        await msg.answer('Выберите один из предложенных вариантов (дополнительная клавиатура)')


@router.message(StateReg.course)
async def set_course(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer(text='Некорректный ввод, введите только число без других символов', reply_markup=ReplyKeyboardRemove())
    else:
        await state.update_data(course=int(msg.text))
        await state.set_state(StateReg.profession)
        await msg.answer('Введите вашу специальность', reply_markup=ReplyKeyboardRemove())


@router.message(StateReg.profession)
async def set_profession(msg: Message, state: FSMContext):
    await state.update_data(profession=msg.text)
    await state.set_state(StateReg.salary)
    await msg.answer('Введите минимальную желаемую оплату труда (рублей в час)', reply_markup=ReplyKeyboardRemove())


@router.message(StateReg.salary)
async def set_salary(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer(text='Некорректный ввод, введите только число без других символов')
    else:
        await state.update_data(salary=int(msg.text))
        await state.set_state(StateReg.hard_work)
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Да'),
             KeyboardButton(text='Нет')],
        ], resize_keyboard=True)
        await msg.answer('Готовы ли вы выполнять тяжелую работу (копать, ломать, строить)', reply_markup=markup)


@router.message(StateReg.hard_work)
async def set_hard_work(msg: Message, state: FSMContext):
    if msg.text in ['Да', 'Нет']:
        if msg.text == 'Да':
            await state.update_data(hard_work=True)
        else:
            await state.update_data(hard_work=False)
        await state.set_state(StateReg.mid_work)
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Да'),
             KeyboardButton(text='Нет')],
        ], resize_keyboard=True)
        await msg.answer('Готовы ли вы выполнять сервисную работу (уборка помещений, прополка грядок и т.д.)',
                         reply_markup=markup)
    else:
        await msg.answer(text='Выберите один из предложенных вариантов (дополнительная клавиатура)')


@router.message(StateReg.mid_work)
async def set_mid_work(msg: Message, state: FSMContext):
    if msg.text in ['Да', 'Нет']:
        if msg.text == 'Да':
            await state.update_data(mid_work=True)
        else:
            await state.update_data(mid_work=False)
        await state.set_state(StateReg.art_work)
        await msg.answer('Готовы ли вы выполнять творческую работу (ведение соц.сетей, рисование и т.д.)')
    else:
        await msg.answer(text='Выберите один из предложенных вариантов (дополнительная клавиатура)')


@router.message(StateReg.art_work)
async def set_art_work(msg: Message, state: FSMContext):
    if msg.text in ['Да', 'Нет']:
        if msg.text == 'Да':
            await state.update_data(art_work=True)
        else:
            await state.update_data(art_work=False)
        await state.set_state(StateReg.other_work)
        markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='Пропустить')],
        ], resize_keyboard=True)
        await msg.answer('Введите иные работы, которые вы готовы выполнять', reply_markup=markup)
    else:
        await msg.answer(text='Выберите один из предложенных вариантов (дополнительная клавиатура)')


@router.message(StateReg.other_work)
async def set_other_work(msg: Message, state: FSMContext):
    if msg.text != 'Пропустить':
        await state.update_data(other_work=msg.text)
    else:
        await state.update_data(other_work=None)
    await state.set_state(StateReg.tools)
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Пропустить')],
    ], resize_keyboard=True)
    await msg.answer('Какие инструменты у вас есть в наличии (дрель, перфоратор, мотоблок)', reply_markup=markup)


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
    profile_msg = 'Ваши данные:\n\n'
    for key, value in data.items():
        if value is True:
            value = 'Да'
        if value is False:
            value = 'Нет'
        if value in ['Пропустить', None]:
            continue
        try:
            profile_msg += '{0}: {1}\n'.format(profile_data[key], value)
        except KeyError:
            continue
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Сохранить', callback_data='save_profile'),
             InlineKeyboardButton(text='Заполнить заново', callback_data='edit_profile')],
        ]
    )

    # Отправка сообщения с данными
    await msg.answer(profile_msg, reply_markup=markup)
