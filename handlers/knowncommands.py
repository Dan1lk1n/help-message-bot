from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

commands = Router()

@commands.message(CommandStart())
async def start(message: Message):
    await message.answer(
        text="Привет, задай вопрос организатору /help",
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

@commands.message(Command('chat_id'))
async def myid(message: Message):
    await message.reply(f"chat_id: {message.chat.id}")



@commands.message(Command('program'))
async def program(message: Message):
    media_group = MediaGroupBuilder()
    media_group.add_photo(type="photo", media='')
    media_group.add_photo(type="photo", media='')
    await message.answer_media_group(media=media_group.build())