import os
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode, CallbackQuery

from keyboards import user_keyboard, admin_keyboard
from dialogs import msg


API_TOKEN = os.getenv("TOKEN_BOT")
ACCESS_ID = os.getenv('ADMIN_ID')


storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# if message.from_user.id != int(ACCESS_ID):
#     await message.answer("ты не админ", parse_mode=ParseMode.MARKDOWN)
# else:


class CellarImport(StatesGroup):
    item = State()
    volume = State()
    count = State()


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
        product_message = "Список товароа"
        await message.answer(product_message, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=user_keyboard)
    else:
        start_message = "@ Список товаров!"
        await message.answer(start_message, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=admin_keyboard)


@dp.message_handler(commands=['add'], state=None)
async def enter_item(message: types.Message):
    await message.answer('Как назовёте позицию?')
    await CellarImport.item.set()


@dp.message_handler(state=CellarImport.item)
async def enter_volume(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await message.answer('Объём?')
    await CellarImport.volume.set()


@dp.message_handler(state=CellarImport.volume)
async def enter_volume(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await message.answer('Количество?')
    await CellarImport.count.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
