import os
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, CallbackQuery

from c_logging import logger
from keyboards import user_keyboard, admin_keyboard
from dialogs import msg
from db import add_data, init_db, change_faq
from states import ProductState, QiwiState, FaqState

API_TOKEN = os.getenv("TOKEN_BOT")
ACCESS_ID = os.getenv('ADMIN_ID')


storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
# if message.from_user.id != int(ACCESS_ID):
#     await message.answer("ты не админ", parse_mode=ParseMode.MARKDOWN)
# else:


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение"""
    if message.from_user.id != int(ACCESS_ID):
        await message.answer(f"Привет, {message.from_user.first_name}",
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=user_keyboard)
    else:
        start_message = "Привет Администратор! Что будем делать?"
        await message.answer(start_message, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=admin_keyboard)


@dp.message_handler(lambda message: message.text == msg.product_m)
async def get_products(message: types.Message):
    if message.from_user.id != int(ACCESS_ID):
        product_message = "Список товаров"
        await message.answer(product_message, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=user_keyboard)
    else:
        start_message = "(admin) | Список товаров!"
        await message.answer(start_message, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=admin_keyboard)


@dp.message_handler(lambda message: message.text == msg.add_product_m,
                    state=None)
async def add_product(message: types.Message):
    await message.answer('Введите название товара')
    await ProductState.name_product.set()


@dp.message_handler(state=ProductState.name_product)
async def add_item_name(message: types.Message, state: FSMContext):
    global item_name
    item_name = message.text
    await state.update_data(answer1=item_name)
    await message.answer('Введите описание товара')
    await ProductState.description_product.set()


@dp.message_handler(state=ProductState.description_product)
async def add_item_description(message: types.Message, state: FSMContext):
    global item_description
    item_description = message.text
    await state.update_data(answer2=item_description)
    await message.answer('Введите цену товара')
    await ProductState.price_product.set()


@dp.message_handler(state=ProductState.price_product)
async def add_item_price(message: types.Message, state: FSMContext):
    global item_price
    item_price = message.text
    await state.update_data(answer2=int(item_price))
    await message.answer('Введите данные товара (название|артикул)')
    await ProductState.data_product.set()


@dp.message_handler(state=ProductState.data_product)
async def add_item_data(message: types.Message, state: FSMContext):
    global item_data
    item_data = message.text
    await state.update_data(answer2=item_data)
    try:
        init_db()
        add_data(item_name, item_description, item_price, item_data)
        logger.info('Product data added successfully')
        await message.answer(f'Данные успешно добавлены!'
                             f'\nНазвание - {item_name};'
                             f'\nОписание - {item_description};'
                             f'\nЦена - {item_price};'
                             f'\nДанные - {item_data}.')
    except Exception as e:
        logger.info('Product data added successfully' + str(e))
        await message.answer('Возникла ошибка при добавлении товара')
    await state.finish()


@dp.message_handler(lambda message: message.text == msg.change_faq_m,
                    state=None)
async def add_faq(message: types.Message):
    await message.answer('Введите описание магазина (FAQ)')
    await FaqState.upd_faq.set()


@dp.message_handler(state=FaqState.upd_faq)
async def update_faq(message: types.Message, state: FSMContext):
    about = message.text
    await state.update_data(answer2=about)
    try:
        change_faq(about)
        logger.info('FAQ has been successfully added')
        await message.answer('Описание (FAQ) было успешно добавлен/обновлен!')
    except Exception as e:
        logger.info('An error occurred while adding the FAQ' + str(e))
        await message.answer('При добавление/обновления FAQ, произошла ОШИБКА!')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
