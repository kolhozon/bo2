import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os

from payment import get_payment_keyboard

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS = [int(x) for x in os.getenv("ADMINS", "").split(",")]

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Кнопки меню
menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Оплатить доступ", callback_data="pay")],
    [InlineKeyboardButton(text="📊 Статистика", callback_data="stats")],
])

@dp.message(F.text, F.text.in_({"/start", "start"}))
async def start_handler(message: Message):
    await message.answer("Добро пожаловать! 👋", reply_markup=menu_kb)

@dp.callback_query(F.data == "pay")
async def pay_handler(callback_query):
    await callback_query.message.answer("Выберите способ оплаты:", reply_markup=get_payment_keyboard(callback_query.from_user.id))

@dp.callback_query(F.data == "stats")
async def stats_handler(callback_query):
    if callback_query.from_user.id in ADMINS:
        await callback_query.message.answer("📊 Статистика пока заглушка.")
    else:
        await callback_query.message.answer("У тебя нет доступа, брат.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
