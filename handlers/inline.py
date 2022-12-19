from contextlib import suppress

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
    results = [
        InlineQueryResultArticle(
            id="1",
            title="Узнать больше о мате",
            input_message_content=InputTextMessageContent(message_text=f"{user_data[query.from_user.id]}"),
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


async def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Укажите число: {new_value}",
            reply_markup=get_keyboard_fab()
        )


@router.message(commands=["numbers_fab"])
async def cmd_numbers_fab(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard_fab())


@router.callback_query(NumbersCallbackFactory.filter())
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory):
    # Текущее значение
    user_value = user_data.get(callback.from_user.id, 0)
    # Если число нужно изменить
    if callback_data.action == "change":
        user_data[callback.from_user.id] = user_value + callback_data.value
        await update_num_text_fab(callback.message, user_value + callback_data.value)
    # Если число нужно зафиксировать
    else:
        await callback.message.edit_text(f"Итого: {user_value}")
    await callback.answer()


# Нажатие на одну из кнопок: -2, -1, +1, +2
@router.callback_query(NumbersCallbackFactory.filter(F.action == "change"))
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory):
    # Текущее значение
    user_value = user_data.get(callback.from_user.id, 0)

    user_data[callback.from_user.id] = user_value + callback_data.value
    await update_num_text_fab(callback.message, user_value + callback_data.value)
    await callback.answer()


# Нажатие на кнопку "подтвердить"
@router.callback_query(NumbersCallbackFactory.filter(F.action == "finish"))
async def callbacks_num_finish_fab(callback: types.CallbackQuery):
    # Текущее значение
    user_value = user_data.get(callback.from_user.id, 0)

    await callback.message.edit_text(f"Итого: {user_value}")
    await callback.answer()
