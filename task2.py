# 2. Write a aiogram bot that 
#will create and send a custom keyboard to the user when the user sends a list of beverages (Tea, Coffee, Beer, Pepsi, Cola).

import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Filter
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "token"

# All handlers should be attached to the Router (or Dispatcher)
router = Router()

@router.message(F.text == "Tea")
@router.message(F.text == "Coffee")
@router.message(F.text == "Beer")
@router.message(F.text == "Pepsi")
@router.message(F.text == "Cola")
async def handlefunc(message: types.Message):
    await message.answer(
        f"Nice to meet you,Did you like to write bots?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Yes"),
                    KeyboardButton(text="No"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(TOKEN, parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())