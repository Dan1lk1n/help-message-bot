from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


help_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Отправить", callback_data="send"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel"),
        ]
    ]
)
