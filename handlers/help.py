from aiogram.enums import ParseMode

from keyboards.help_keyboard import help_keyboard
from bot import bot

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton)

import config

help_router = Router()


class Form(StatesGroup):
    question = State()
    confirmation = State()


@help_router.message(Command("help"))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.question)
    await state.update_data(editable_message=await message.answer(
        "Задай вопрос и я передам его организаторам\nС тобой свяжутся в ЛС и помогут решить вопрос",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="❌ Отмена", callback_data="cancel"),
                ]
            ]
        ),
    ))


@help_router.message(Form.question)
async def question_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    editable_message = data["editable_message"]
    await state.update_data(question=message.text)
    await state.set_state(Form.question)
    await bot.edit_message_text(chat_id=message.from_user.id,
                                message_id=editable_message.message_id,
                                text=f'Твой вопроc:\n\n<code>{message.text}</code>\n\nПодтверди отправку',
                                reply_markup=help_keyboard)
    await bot.delete_message(message.chat.id, message_id=message.message_id)


@help_router.callback_query(F.data == 'cancel')
async def on_enter_callback(callback_query: CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text="Действие отменено",
        reply_markup=None
    )


@help_router.callback_query(Form.confirmation)
@help_router.callback_query(F.data == 'send')
async def on_enter_callback(callback_query: CallbackQuery, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    data = await state.get_data()
    await state.clear()
    txt = f'Вопрос от @{callback_query.from_user.username}\n\n{data["question"]}'
    await bot.send_message(chat_id=config.ADMINS_HELP_CHAT, text=txt, reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Забрать вопрос", callback_data="claim")]]))
    await bot.edit_message_text(
        chat_id=callback_query.from_user.id,
        message_id=callback_query.message.message_id,
        text="Я передал твой запрос нашей команде. Скоро с тобой свяжутся в личном диалоге.",
        reply_markup=None
    )


@help_router.callback_query(F.data == 'claim')
async def on_enter_callback(callback_query: CallbackQuery, state: FSMContext) -> None:
    await bot.edit_message_text(
        chat_id=config.ADMINS_HELP_CHAT,
        message_id=callback_query.message.message_id,
        text=f'<s>{callback_query.message.text}</s>\n\n<b>Вопрос забран @{callback_query.from_user.username}</b>',
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )
