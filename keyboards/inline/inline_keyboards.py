from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

vaqt = {
    'uz': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Hozir", callback_data='now_uz'), InlineKeyboardButton(text="Boshqa vaqtda", callback_data='other_uz')]
    ]),
    'ru': InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сейчас", callback_data='now_ru'), InlineKeyboardButton(text="В другое время", callback_data='now_ru')]
    ])
}