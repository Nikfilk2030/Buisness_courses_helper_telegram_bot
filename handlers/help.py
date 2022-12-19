# # https://huelogia.com/?s=блять


from aiogram import Router
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from Buisness_courses_helper_telegram_bot.keyboards.for_start import get_start_kb

router = Router()


@router.message(commands=["help"])
async def cmd_help(message: Message):
    await message.answer(
        "Я умею:\n\n"
        "1. Приветсвовать новеньких в чате\n"
        "2. Чтобы задать приветствие, используйте /set_welcome\n"
        "3. Чтобы узнать приветствие, используйте /get_welcome\n"
        "4. Чтобы удалить приветствие, используйте /del_welcome\n"
        "5. Используй меня в инлайн режиме, с помощнью\n '@i_love_nikita_sha_bot ***'\n"
        "чтобы попасть на вики страницу этого мата\n"
    )
