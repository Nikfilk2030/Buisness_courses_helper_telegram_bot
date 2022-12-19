from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message(commands=["help"])
async def cmd_help(message: Message):
    await message.answer(
        "<b>Я умею</b> \n\n"
        "1. Приветсвовать новеньких в чате\n"
        "2. Чтобы задать приветствие, используйте /set_welcome\n"
        "3. Чтобы узнать приветствие, используйте /get_welcome\n"
        "4. Чтобы удалить приветствие, используйте /del_welcome\n"
        "5. Используй меня в инлайн режиме, с помощью\n"
        "@i_love_nikita_sha_bot\n"
        "6. Посмотри, насколько ты везуч, используя /play\n"
        "7. Гайд по игре /play_help\n",
        parse_mode="HTML"
    )


@router.message(commands=["play_help"])
async def cmd_help(message: Message):
    await message.answer(
        "<b>Игра Орёл или Решка</b> \n\n"
        "В личном чате с ботом, или в любом другом чате, где я есть,"
        " используйте команду /play\n"
        "После этого я выведу вам кнопки, с помощью которых вы сможете сыграть в игру\n"
        "Позвав меня инлайн\n"
        "@i_love_nikita_sha_bot\n "
        "Я покажу вам ваши результаты\n",
        parse_mode="HTML"
    )
