from aiogram import Router, types
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from Buisness_courses_helper_telegram_bot.keyboards.for_start import get_start_kb

router = Router()


@router.message(commands=["start"])
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать в Гантон бота!\n"
        "Автор @pchelka_zh\n"
        "Чтобы узнать команды напишите /help\n"
        "Или воспользуйтесь кнопками ниже\n"
        "Также меня можно использовать в inline моде!\n",
        reply_markup=get_start_kb()
    )


chat_id_to_greeting = {}
default_greeting = "Салам алейкум, добро пожаловать в чат!"
waiting_for_new_greeting = False


@router.message(commands=["set_welcome"])
async def cmd_set_welcome(message: Message):
    global waiting_for_new_greeting
    waiting_for_new_greeting = True
    await message.answer("Ответь на это сообщение и это станет новым приветствием")


@router.message(Text(text="Задать приветствие", text_ignore_case=True))
async def set_greeting(message: Message):
    global waiting_for_new_greeting
    waiting_for_new_greeting = True
    await message.answer("Ответь на это сообщение и это станет новым приветствием")


@router.message(commands=["get_welcome"])
async def cmd_get_welcome(message: Message):
    if message.chat.id in chat_id_to_greeting:
        await message.answer(
            f"Приветствие: {chat_id_to_greeting[message.chat.id]}"
        )
    else:
        await message.answer(
            f"Приветствие не задано, использую дефолтное:\n"
            f"{default_greeting}"
        )


@router.message(Text(text="Узнать приветствие", text_ignore_case=True))
async def know_greeting(message: Message):
    if message.chat.id in chat_id_to_greeting:
        await message.answer(
            f"Приветствие: {chat_id_to_greeting[message.chat.id]}"
        )
    else:
        await message.answer(
            f"Приветствие не задано, использую дефолтное:\n"
            f"{default_greeting}"
        )


@router.message(commands=["del_welcome"])
async def cmd_del_welcome(message: Message):
    if message.chat.id in chat_id_to_greeting:
        del chat_id_to_greeting[message.chat.id]
        await message.answer(
            "Удалил приветствие!"
        )
    else:
        await message.answer(
            "Приветствие не задано, нечего мне удалять"
        )


@router.message(Text(text="Удалить приветствие", text_ignore_case=True))
async def delete_greeting(message: Message):
    if message.chat.id in chat_id_to_greeting:
        del chat_id_to_greeting[message.chat.id]
        await message.answer(
            "Удалил приветствие!"
        )
    else:
        await message.answer(
            "Приветствие не задано, нечего мне удалять"
        )


@router.message(Text(text="Убрать клавиатуру", text_ignore_case=True))
async def delete_keyboard(message: Message):
    await message.reply(
        "Ладно, не мешаюсь",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def somebody_added(message: types.Message):
    if message.chat.id in chat_id_to_greeting:
        for user in message.new_chat_members:
            await message.reply(f"{chat_id_to_greeting[message.chat.id]}, {user.full_name}")
    else:
        for user in message.new_chat_members:
            await message.reply(f"{default_greeting}, {user.full_name}")


@router.message(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def somebody_left(message: types.Message):
    await message.reply(f"Пока, {message.left_chat_member.full_name}")


@router.message(content_types="text")
async def set_new_greeting(message: Message):
    global waiting_for_new_greeting
    if waiting_for_new_greeting:
        chat_id_to_greeting[message.chat.id] = message.text
        waiting_for_new_greeting = False
        await message.answer(
            "Новое приветствие установлено!"
        )
