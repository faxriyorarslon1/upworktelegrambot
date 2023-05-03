# 1. Create a bot that will reply the user's first name for any messages sent to the bot.
import logging
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

token = 'token'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler()
async def handle_message(message: types.Message):
    await message.reply(f"Hello, {message.from_user.first_name}!")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)