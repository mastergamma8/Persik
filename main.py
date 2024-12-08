from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, PreCheckoutQuery
from aiogram.fsm.storage.memory import MemoryStorage
from payment import send_invoice_handler, pre_checkout_handler
from payment_keyboard import payment_keyboard
import asyncio

TOKEN = "7876195830:AAGCWrMFWJ6fmB4q47flqPGq_7TcHOcSBwA"
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Хранилище баланса пользователей
user_balances = {}

# Команда /start
@dp.message(F.text == "/start")
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="📥 Скачать Premier Brawl", callback_data="download_game")]]
    )
    await message.answer(
        "Добро пожаловать! Чтобы скачать Premier Brawl, нажмите на кнопку ниже.", reply_markup=keyboard
    )

# Кнопка "Скачать"
@dp.callback_query(F.data == "download_game")
async def download_game_handler(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    balance = user_balances.get(user_id, 0)

    if balance >= 100:
        user_balances[user_id] = balance - 100  # Списание звёзд
        await callback.message.answer(
            "Оплата прошла успешно ✅\nПодготовка ссылки для скачивания..."
        )
        await asyncio.sleep(2)
        await callback.message.answer("Ссылка для скачивания: https://link.brawlstars.com/?action=voucher&code=8142f715-a879-4d19-9af3-fa49e72ef59a")
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="💳 Пополнить баланс", callback_data="recharge_balance")]]
        )
        await callback.message.answer(
            "Для скачивания необходимо 100 звёзд.\nПополните баланс, чтобы продолжить.",
            reply_markup=keyboard,
        )

# Пополнение баланса
@dp.callback_query(F.data == "recharge_balance")
async def recharge_balance_handler(callback: types.CallbackQuery):
    await send_invoice_handler(bot, callback.from_user.id)

# Проверка платежа
dp.pre_checkout_query.register(pre_checkout_handler)

# Обработчик успешной оплаты
@dp.message(F.successful_payment)
async def successful_payment_handler(message: types.Message):
    user_id = message.from_user.id
    user_balances[user_id] = user_balances.get(user_id, 0) + 100
    await message.answer("Оплата успешно прошла! Ваш баланс пополнен на 100 звёзд.")

# Запуск бота
async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
