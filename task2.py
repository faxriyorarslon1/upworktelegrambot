# 2. Write a aiogram bot that 
#will create and send a custom keyboard to the user when the user sends a list of beverages (Tea, Coffee, Beer, Pepsi, Cola).

import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.message import ContentTypes
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token='token')
dp = Dispatcher(bot)


@dp.message_handler(Text(equals=["Tea", "Coffee", "Beer", "Pepsi", "Cola"]))
async def handle_brands(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    kb1 = KeyboardButton('Option 1')
    kb2 = KeyboardButton('Option 2')
    keyboard.add(kb1, kb2)
    keyboard.add(KeyboardButton('Option 3'))
    keyboard.add(KeyboardButton('Option 4'))
    await bot.send_message(chat_id=message.chat.id, text="Choose an option:",
                            reply_markup=keyboard)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)