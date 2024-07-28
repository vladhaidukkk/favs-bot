import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from bot.config import settings

# To see INFO aiogram logs in the console.
logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
