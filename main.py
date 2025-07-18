import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN, ADMINS

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# Главное меню
def get_main_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Купить", callback_data="buy")],
        [InlineKeyboardButton(text="ℹ️ О боте", callback_data="info")],
        [InlineKeyboardButton(text="💬 Поддержка", url="https://t.me/your_support_bot")]
    ])
    return kb

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в БОТИК 👋", reply_markup=get_main_keyboard())
    if message.from_user.id in ADMINS:
        await message.answer("Ты зашел как админ 👑")

@dp.callback_query(F.data == "buy")
async def handle_buy(callback: types.CallbackQuery):
    await callback.message.answer("💳 Оплата скоро будет подключена!")

@dp.callback_query(F.data == "info")
async def handle_info(callback: types.CallbackQuery):
    await callback.message.answer("БОТИК — универсальный телеграм-бот с кнопками, админкой и платёжкой.")

@dp.message(F.text == "/admin")
async def admin_cmd(message: types.Message):
    if message.from_user.id not in ADMINS:
        return await message.answer("⛔️ Доступ только для админов")
    await message.answer("Добро пожаловать в админку 🛠️")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())