from aiogram.utils.keyboard import InlineKeyboardBuilder

# Клавиатура для кнопки оплаты
def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Оплатить 💳", pay=True)
    return builder.as_markup()
