# 1. Create a bot that will reply the user's first name for any messages sent to the bot.
import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6231010696:AAHdx578ciB1_1OWILs2lFUhWP2hyQ4GQbs"

# All handlers should be attached to the Router (or Dispatcher)
router = Router()


@router.message()
async def handle_message(message: types.Message):
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>")


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())