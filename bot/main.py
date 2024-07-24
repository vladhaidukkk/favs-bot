import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart

from bot.config import settings

# To see INFO aiogram logs in the console.
logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")


@dp.message(Command("help"))
async def handle_help(message: types.Message):
    text = "I'm a simple echo bot.\nSend me whatever you want and I will resend it."
    bold_name_entity = types.MessageEntity(type="bold", offset=len(text[:13]), length=4)
    await message.answer(text=text, entities=[bold_name_entity])


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
