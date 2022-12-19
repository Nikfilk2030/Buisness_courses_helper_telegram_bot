from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(content_types="text")
async def message_with_text(message: Message):
    if message.text[0] == "/":
        await message.answer("Это команда конечно, пиздатая наверное, но я не умею на неё отвечать")
    else:
        await message.answer(f"Попробуй /{message.text} или отъебись, ты неправильную команду написал")


@router.message(content_types="sticker")
async def message_with_sticker(message: Message):
    await message.answer("Классный стикер!")


@router.message(content_types="animation")
async def message_with_gif(message: Message):
    await message.answer("Классная GIF!")
