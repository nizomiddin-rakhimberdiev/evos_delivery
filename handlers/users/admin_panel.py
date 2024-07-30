
from loader import dp, db, bot
from data.config import ADMINS
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from keyboards.default.keyboards import admin_menu
from states.all_states import AddCategoryState, AddProductState, GetProductsState
from aiogram.dispatcher import FSMContext
from keyboards.inline.inline_keyboards import get_catedories_btn


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


# @dp.message_handler(commands=['categories'])
# async def get_categories(message: types.Message):
#     await message.answer("Kategoriyalar jadvali:", reply_markup=await get_catedories_btn())


@dp.message_handler(AdminFilter(), text="Add product")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer("Product nomini kiriting:")
    await AddProductState.name.set()

@dp.message_handler(state=AddProductState.name)
async def process_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Product narxini kiriting:")
    await AddProductState.price.set()

@dp.message_handler(state=AddProductState.price)
async def process_product_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer("Product tavsifini kiriting:")
    await AddProductState.description.set()

@dp.message_handler(state=AddProductState.description)
async def process_product_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer("Product rasmini kiriting (URL):")
    await AddProductState.image.set()

@dp.message_handler(content_types=['photo'], state=AddProductState.image)
async def process_product_image(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['image'] = message.photo[0].file_id
    await message.answer("Product kategoriyasini tanlang:", reply_markup=await get_catedories_btn())
    await AddProductState.category.set()


@dp.callback_query_handler(lambda c: c.data.startswith('category_'),state=AddProductState.category)
async def process_product_category(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        category_id = call.data.split('_')[1]
        data['category_id'] = category_id
        name = data['name']
        price = data['price']
        description = data['description']
        image = data['image']
        category_id = data['category_id']
        db.add_product(name, price, description, image, category_id)
        await call.message.answer(f"Product {name} qo'shildi")
        await state.finish()
    


@dp.message_handler(text="Get products")
async def get_products(message: types.Message):
    await message.answer('Categoriyalardan birini tanlang', reply_markup=await get_catedories_btn())
    await GetProductsState.category.set()



@dp.callback_query_handler(lambda c: c.data.startswith('category_'), state=GetProductsState.category)
async def get_catedories_btn(call: types.CallbackQuery, state: FSMContext):
    category_id = call.data.split('_')[1]
    products = db.get_products(category_id)
    for product in products:
        btn = types.InlineKeyboardButton(text=product['name'], callback_data=f'product_{product["id"]}')

    await call.message.answer('Productlar:', reply_markup=reply_markup)