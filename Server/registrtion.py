from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from states import Reg
from aiogram.fsm.context import FSMContext
import database as db
import keyboard

router = Router()


@router.callback_query(F.data == 'reg')
async def start_reg(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Reg.fio)
    await callback.message.answer(text='Введите свое ФИО')


@router.message(Reg.fio)
async def set_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(Reg.sex)
    await msg.answer('Выберите ваш пол')


@router.message(Reg.sex)
async def set_name(msg: Message, state: FSMContext):
    await state.update_data(sex=msg.text)
    await state.set_state(Reg.born)
    await msg.answer('Введите вашу дату рождения')
