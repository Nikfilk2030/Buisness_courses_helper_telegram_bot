import asyncio
from aiogram import Bot, Dispatcher
from handlers import start, inline, help
from config_reader import config


# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_router(help.router)
    dp.include_router(inline.router)
    dp.include_router(start.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
