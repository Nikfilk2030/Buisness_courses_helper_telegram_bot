import random
from contextlib import suppress
from time import sleep

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from aiogram import Router, F, types
from aiogram.dispatcher.filters.callback_data import CallbackData
from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

user_data = {}
user_count = {}


@router.inline_query()
async def inline_query(query):
    if query.from_user.id not in user_data:
        user_data[query.from_user.id] = 0
        user_count[query.from_user.id] = 0
        results = [
            InlineQueryResultArticle(
                id="1",
                title="Узнать свою статистику",
                input_message_content=InputTextMessageContent(message_text=f"Я ещё не принял участие в игре\n"
                                                                           f"Воспользуюсь командой /play\n"
                                                                           f"(в чате, где бот есть)"),
            )
        ]
    else:
        data = user_data[query.from_user.id]
        count = user_count[query.from_user.id]
        if count == 0:
            count = 1
        results = [
            InlineQueryResultArticle(
                id="1",
                title="Узнать свою статистику",
                input_message_content=InputTextMessageContent(
                    message_text=f"Моя точность: "
                                 f"{data / count * 100}%\n"
                                 f"Игр сыграно: {count}\n"
                                 f"Побед: {data}\n"
                                 f"Поражений: {count - data}\n")
            )
        ]
    await query.answer(results, cache_time=1)


class NumbersCallbackFactory(CallbackData, prefix="fabnum"):
    action: str
    value: Optional[int]


def get_keyboard_fab():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="орёл", callback_data=NumbersCallbackFactory(action="change", value=1)
    )
    builder.button(
        text="решка", callback_data=NumbersCallbackFactory(action="change", value=2)
    )
    builder.button(
        text="Подтвердить", callback_data=NumbersCallbackFactory(action="finish")
    )
    builder.adjust(2)
    return builder.as_markup()


# async def update_num_text_fab(message: types.Message, new_value: int):


@router.message(commands=["play"])
async def cmd_numbers_fab(message: types.Message):
    if message.from_user.id not in user_data:
        user_data[message.from_user.id] = 0
        user_count[message.from_user.id] = 0
    await message.answer("Выбери:", reply_markup=get_keyboard_fab())


@router.callback_query(NumbersCallbackFactory.filter())
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory):
    if callback.from_user.id not in user_data:
        await callback.answer("Ты ещё не играл")
        return

    # Текущее значение
    user_value = callback_data.value
    right_value = random.randint(1, 2)

    # Ловушка для Гантона
    if callback.from_user.username == "postironix":
        right_value = random.randint(1, 5)
    # Если число нужно изменить
    if callback_data.action == "change":

        user_count[callback.from_user.id] += 1

        if user_value == right_value:
            user_data[callback.from_user.id] += 1

            with suppress(TelegramBadRequest):
                await callback.message.edit_text(f"{callback.from_user.username}, ты угадал!\n"
                                                 f"Твой счёт: {user_data[callback.from_user.id]}\n"
                                                 f"За {user_count[callback.from_user.id]} игр\n")
        else:
            with suppress(TelegramBadRequest):
                await callback.message.edit_text(f"{callback.from_user.username}, ты не угадал(\n"
                                                 f"Твой счёт: {user_data[callback.from_user.id]}\n"
                                                 f"За {user_count[callback.from_user.id]} игр\n")

        sleep(1.5)
        with suppress(TelegramBadRequest):
            await callback.message.edit_text("Выбери:", reply_markup=get_keyboard_fab())

    # Если число нужно зафиксировать
    else:
        with suppress(TelegramBadRequest):
            data = user_data[callback.from_user.id]
            count = user_count[callback.from_user.id]
            await callback.message.edit_text(f"{callback.from_user.username}, твоя точность: "
                                             f"{data / count * 100}%\n"
                                             f"Игр сыграно: {count}\n"
                                             f"Побед: {data}\n"
                                             f"Поражений: {count - data}\n")
    await callback.answer()
