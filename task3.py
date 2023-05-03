# 3. Write down a sample bot code for a registration form that will collect user's Name, Age, Phone and Email.
# This should be using FSM feature in Aiogram. 
# There should be proper validation and error messages to the user if any entered values are not proper.
import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor


logging.basicConfig(level=logging.INFO)
bot = Bot(token='token')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Define registration form FSM states
class RegistrationForm(StatesGroup):
    name = State()
    age = State()
    phone = State()
    email = State()

@dp.message_handler(commands='start')
async def start_registration(message: types.Message):
    await RegistrationForm.name.set()
    await message.reply("Hi there! What's your name?")


# Define name message handler to collect name from user and move to next question
@dp.message_handler(state=RegistrationForm.name)
async def collect_name(message: types.Message, state: FSMContext):
    if not re.match("^[A-Za-z ]*$", message.text):
        await message.reply("Invalid name! Please enter a valid name containing only alphabets and spaces.")
        return
    
    async with state.proxy() as data:
        data['name'] = message.text
        await RegistrationForm.next()
        await message.reply("Great! What's your age?")


# Define age message handler to collect age from user and move to next question
@dp.message_handler(state=RegistrationForm.age)
async def collect_age(message: types.Message, state: FSMContext):
    # Validate age (should be a number between 18 and 99)
    if not message.text.isdigit() or int(message.text) < 18 or int(message.text) > 99:
        await message.reply("Invalid age! Please enter a valid age between 18 and 99.")
        return

    async with state.proxy() as data:
        data['age'] = message.text
        await RegistrationForm.next()
        await message.reply("Great! What's your phone number?")


# Define phone message handler to collect phone from user and move to next question
@dp.message_handler(state=RegistrationForm.phone)
async def collect_phone(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or len(message.text) != 12:
        await message.reply("Invalid phone number! Please enter a valid 12-digit phone number.")
        return

    async with state.proxy() as data:
        data['phone'] = message.text
        await RegistrationForm.next()
        await message.reply("Great! What's your email address?")


# Define email message handler to collect email from user and end registration form
@dp.message_handler(state=RegistrationForm.email)
async def collect_email(message: types.Message, state: FSMContext):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", message.text):
        await message.reply("Invalid email address! Please enter a valid email address")
        return
    
    async with state.proxy() as data:
        data['email'] = message.text
        await RegistrationForm.next()
        await message.reply("Thank You! This is your collected data")
        user_data = f"<b>Name:</b> {data['name']}\n"
        user_data += f"<b>Age:</b> {data['age']}\n"
        user_data += f"<b>Phone Number:</b> {data['phone']}\n"
        user_data += f"<b>Email:</b> {data['email']}"
        await bot.send_message(message.from_user.id, user_data, parse_mode="html")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
