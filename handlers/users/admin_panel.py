
from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from keyboards.default.keyboards import admin_menu
from states.all_states import AddCategoryState
from aiogram.dispatcher import FSMContext


class AdminFilter(BoundFilter):
    async def check(self, message: types.Message):
        return str(message.from_user.id) in ADMINS
    


@dp.message_handler(AdminFilter(), commands=['admin_panel'])
async def admin_panel(message: types.Message):
    await message.answer('Admin panel', reply_markup=admin_menu)


@dp.message_handler(AdminFilter(), text='Add category')
async def add_category(message: types.Message, state: FSMContext):
    await message.answer('Category nomini kiriting: ')
    await AddCategoryState.name.set()


@dp.message_handler(state=AddCategoryState.name)
async def get_category_name(message: types.Message, state: FSMContext):
    try:
        name = message.text
        db.add_category(name)
        await message.answer(f"Kategoriya jadvaliga {name} qo'shildi")
        await state.finish()
    except:
        await message.answer(f"Xatolik! Kategoriya qo'shishda xatolik yuz berdi. \nBu nom jadvalda mavjud, boshqa nom kiriting")
        # await state.reset_state()