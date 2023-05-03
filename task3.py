# 3. Write down a sample bot code for a registration form that will collect user's Name, Age, Phone and Email.
# This should be using FSM feature in Aiogram. 
# There should be proper validation and error messages to the user if any entered values are not proper.
import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import re

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "token"

# All handlers should be attached to the Router (or Dispatcher)
router = Router()


# Define registration form FSM states
class RegistrationForm(StatesGroup):
    name = State()
    age = State()
    phone = State()
    email = State()

@router.message(Command("start"))
async def command_start(message: types.Message, state: FSMContext) -> None:
    await state.set_state(RegistrationForm.name)
    await message.answer(
        "Hi there! What's your name?",
        reply_markup=types.ReplyKeyboardRemove(),
    )


# Define name message handler to collect name from user and move to next question
@router.message(RegistrationForm.name)
async def collect_name(message: types.Message, state: FSMContext):
    if not re.match("^[A-Za-z ]*$", message.text):
        await message.reply("Invalid name! Please enter a valid name containing only alphabets and spaces.")
        return
    
    data = await state.get_data()
    data['name'] = message.text
    data = await state.update_data(data)
    await state.set_state(RegistrationForm.age)
    await message.reply("Great! What's your age?")


# Define age message handler to collect age from user and move to next question
@router.message(RegistrationForm.age)
async def collect_age(message: types.Message, state: FSMContext):
    # Validate age (should be a number between 18 and 99)
    if not message.text.isdigit() or int(message.text) < 18 or int(message.text) > 99:
        await message.reply("Invalid age! Please enter a valid age between 18 and 99.")
        return
    data = await state.get_data()
    data['age'] = message.text
    data = await state.update_data(data)
    await state.set_state(RegistrationForm.phone)
    await message.reply("Great! What's your phone number?")


# Define phone message handler to collect phone from user and move to next question
@router.message(RegistrationForm.phone)
async def collect_phone(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or len(message.text) != 12:
        await message.reply("Invalid phone number! Please enter a valid 12-digit phone number.")
        return
    data = await state.get_data()
    data['phone'] = message.text
    data = await state.update_data(data)
    await state.set_state(RegistrationForm.email)
    await message.reply("Great! What's your email address?")


# Define email message handler to collect email from user and end registration form
@router.message(RegistrationForm.email)
async def collect_email(message: types.Message, state: FSMContext):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", message.text):
        await message.reply("Invalid email address! Please enter a valid email address")
        return
    data = await state.get_data()
    data['email'] = message.text
    await state.update_data(data)
    print(data)
    await message.reply("Thank You! This is your collected data")
    user_data = f"Name: {data['name']}\n"
    user_data += f"Age: {data['age']}\n"
    user_data += f"Phone Number:</b> {data['phone']}\n"
    user_data += f"Email: {data['email']}"
    await message.answer(message.from_user.id, user_data)



async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(TOKEN, parse_mode="HTML")
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())