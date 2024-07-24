import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.utils import markdown

from bot.config import settings

# To see INFO aiogram logs in the console.
logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2),
)
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")


@dp.message(Command("help"))
async def handle_help(message: types.Message):
    text = markdown.text(
        markdown.text(
            "I'm a simple",
            markdown.bold("echo"),
            markdown.markdown_decoration.quote("bot."),
        ),
        markdown.markdown_decoration.quote(
            "Send me whatever you want and I will resend it."
        ),
        sep="\n",
    )
    await message.answer(text=text)


@dp.message()
async def echo(message: types.Message):
    await message.copy_to(chat_id=message.chat.id)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
