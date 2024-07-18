from loader import dp, db, bot
from data.config import ADMINS
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default.keyboards import contact_request, back_button, menu
from states.all_states import FeedbackState


@dp.message_handler(Text(equals='✍️ Оставить отзыв'))
async def feedback(message: types.Message):
    if db.get_contact(message.from_user.id) is None:
        await message.answer("Поделитесь контактом для дальнейшего связи с Вами", reply_markup=contact_request)
        await FeedbackState.waiting_for_contact.set()
    else:
        await message.answer("Отправьте ваши отзывы", reply_markup=back_button)
        await FeedbackState.waiting_for_feedback.set()
        


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=FeedbackState.waiting_for_contact)
async def contact_handler(message: types.Message, state: FSMContext):
    contact = message.contact.phone_number
    chat_id = message.from_user.id
    db.update_user(chat_id, contact)
    await message.answer("Отправьте ваши отзывы", reply_markup=back_button)
    await FeedbackState.waiting_for_feedback.set()


@dp.message_handler(lambda m: m.text not in ['⬅️ Назад', '⬅️ Ortga'], state=FeedbackState.waiting_for_feedback)
async def process_feedback(message: types.Message, state: FSMContext):
    feedback = message.text
    for admin in ADMINS:
        await bot.send_message(admin, f"Отзыв от {message.from_user.full_name}: \n\n{feedback}")
    await message.answer("Спасибо за ваш отзыв!", reply_markup=menu[db.get_lng(message.from_user.id)])
    await state.finish()