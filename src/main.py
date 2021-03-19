import os
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode, CallbackQuery

from keyboards import user_keyboard, admin_keyboard
from dialogs import msg


API_TOKEN = os.getenv("TOKEN_BOT")
ACCESS_ID = os.getenv('ADMIN_ID')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

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
        product_message = "Список товароа"
        await message.answer(product_message, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=user_keyboard)
    else:
        start_message = "@ Список товаров!"
        await message.answer(start_message, parse_mode=ParseMode.MARKDOWN,
                             reply_markup=admin_keyboard)


@dp.message_handler(lambda message: message.text == msg.add_product_m)
async def add_product(message: types.Message):
    dp.register_message_handler(message)
    await message.answer()


async def add_item_name(message: types.Message):
    global item_name
    item_name = message.text
    dp.poll_answer_handlers(message, add_item_description)
    await message.answer(message.chat.id, "📘 Введите название товара")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
