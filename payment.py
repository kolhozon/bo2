from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from yookassa import Payment
import uuid
import os

YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_API_TOKEN = os.getenv("YOOKASSA_API_TOKEN")

Payment.configure(YOOKASSA_SHOP_ID, YOOKASSA_API_TOKEN)

def create_payment(user_id: int, amount=100):
    payment = Payment.create({
        "amount": {
            "value": f"{amount}.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/your_bot"  # можно кастомизировать
        },
        "description": f"Оплата доступа для пользователя {user_id}",
        "metadata": {"user_id": user_id}
    }, uuid.uuid4())
    return payment.confirmation.confirmation_url

def get_payment_keyboard(user_id: int):
    url = create_payment(user_id)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Перейти к оплате 💳", url=url)]
    ])
    return kb
