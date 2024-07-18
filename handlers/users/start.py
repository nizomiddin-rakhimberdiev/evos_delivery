from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.keyboards import menu

from loader import dp, db


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    if message.from_user.id not in db.all_chat_id():
        db.insert_user(message.from_user.id)
    await message.answer(text='Выберите одно из следующих', reply_markup=menu[db.get_lng(message.from_user.id)])



@dp.message_handler(text='⬅️ Назад', state='*')
async def back_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text='Выберите одно из следующих', reply_markup=menu[db.get_lng(message.from_user.id)])