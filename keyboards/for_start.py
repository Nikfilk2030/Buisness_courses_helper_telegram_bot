from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Задать приветствие")
    kb.button(text="Узнать приветствие")
    kb.button(text="Удалить приветствие")
    kb.button(text="Убрать клавиатуру")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
