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
    if message.text:
        await message.answer(text=message.text)
    elif message.sticker:
        await message.answer_sticker(sticker=message.sticker.file_id)
    else:
        await message.answer("You've sent something strange 🙃")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
