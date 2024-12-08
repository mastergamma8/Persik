from aiogram.types import LabeledPrice, PreCheckoutQuery
from payment_keyboard import payment_keyboard

# Провайдер токен для оплаты
PROVIDER_TOKEN = ""  # Замените на ваш реальный токен

# Отправка инвойса
async def send_invoice_handler(bot, user_id: int):
    prices = [LabeledPrice(label="100 Звёзд", amount=100)]  # Указываем 100 звезд без умножения
    await bot.send_invoice(
        chat_id=user_id,
        title="Пополнение звёзд",
        description="Пополните ваш баланс на 100 звёзд.",
        payload="recharge_100_stars",
        provider_token=PROVIDER_TOKEN,
        currency="XTR",  # Укажите нужную валюту
        prices=prices,
        need_email=False,
        reply_markup=payment_keyboard(),
    )

# Проверка перед оплатой
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)
