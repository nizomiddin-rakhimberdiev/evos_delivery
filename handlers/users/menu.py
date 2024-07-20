from loader import dp, db
from aiogram import types
from keyboards.default.keyboards import menu_btns, contact_request, back_button, menu


@dp.message_handler(text="🍴 Меню")
async def get_contact(message: types.Message):
    await message.answer("📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang", reply_markup=menu_btns)