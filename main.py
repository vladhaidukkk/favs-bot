import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types

# To see INFO aiogram logs in the console.
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.environ["BOT_TOKEN"]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def echo(message: types.Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("You've sent something strange 🙃")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
