from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, PreCheckoutQuery,
    InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo,
    LabeledPrice
)
from aiogram.filters import CommandStart
import httpx
import os

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

WEBAPP_URL = os.getenv("WEBAPP_URL")
API_URL = "http://localhost:8000"

@dp.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="🎰 Открыть рулетку",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}/static/index.html")
        )
    ]])
    await message.answer(
        "Добро пожаловать в рулетку!\n\n"
        "💫 Каждый прокрут стоит 25 звёзд\n"
        "🎁 Выиграйте до 100 звёзд!\n\n"
        "Нажмите кнопку, чтобы начать:",
        reply_markup=keyboard
    )

@dp.message(F.text == "/spin")
async def cmd_spin(message: Message):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Прокрут рулетки 🎰",
        description="Стоимость: 25 звёзд. Выиграйте до 100 звёзд!",
        payload=f"spin_{message.from_user.id}",
        currency="XTR",
        prices=[LabeledPrice(label="Прокрут", amount=25)],
    )

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@dp.message(F.successful_payment)
async def on_payment(message: Message):
    payment = message.successful_payment
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/payment/success", params={
            "charge_id": payment.telegram_payment_charge_id,
            "user_id": message.from_user.id,
            "amount": payment.total_amount,
        })
    await message.answer("✅ Оплата прошла! Открой рулетку и крути!")