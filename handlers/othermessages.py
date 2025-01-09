from aiogram import Router
from aiogram.types import Message

other = Router()


@other.message()
async def other_messages(message: Message):
    if message.chat.type != 'supergroup':
        await message.reply(f"Я еще маленький и не знаю таких команд, напиши /start, чтобы узнать что я могу)")
    else:
        return
