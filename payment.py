# payment.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yookassa import Payment, Configuration
import uuid
import os

# Правильная инициализация
Configuration.account_id = os.getenv("YOOKASSA_SHOP_ID")
Configuration.secret_key = os.getenv("YOOKASSA_API_TOKEN")

def create_payment(user_id: int, amount=100):
    payment = Payment.create({
        "amount": {
            "value": f"{amount}.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/KolhozAnalytics_bot"
        },
        "description": f"Оплата доступа для пользователя {user_id}",
        "metadata": {"user_id": user_id}
    }, uuid.uuid4().hex)
    return payment.confirmation.confirmation_url

def get_payment_keyboard(user_id: int, amount=100):
    url = create_payment(user_id, amount)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к оплате 💳", url=url)]
    ])
    return kb