import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from sqlalchemy import insert, select

from bot.config import settings
from bot.db.core import session_factory
from bot.db.models import UserModel

# To see INFO aiogram logs in the console.
logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.bot.token)
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    async with session_factory() as session:
        query = select(UserModel).filter_by(telegram_id=message.from_user.id)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()
        if not existing_user:
            stmt = insert(UserModel).values(telegram_id=message.from_user.id)
            await session.execute(stmt)
            await session.commit()

    await message.answer(f"Hello, {message.from_user.full_name}!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
