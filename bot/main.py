import asyncio
import logging
from enum import Enum

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from sqlalchemy import insert, select

from bot.config import settings
from bot.db.core import session_factory
from bot.db.models import UserModel

# To see INFO aiogram logs in the console.
logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.bot.token)
dp = Dispatcher()


class ButtonText(Enum):
    ADD_WISH = "✨Add a Wish"


@dp.message(CommandStart())
async def handle_start(message: types.Message) -> None:
    async with session_factory() as session:
        query = select(UserModel).filter_by(telegram_id=message.from_user.id)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()
        if not existing_user:
            stmt = insert(UserModel).values(telegram_id=message.from_user.id)
            await session.execute(stmt)
            await session.commit()

    buttons = [KeyboardButton(text=ButtonText.ADD_WISH.value)]
    keyboard_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)
    await message.answer(
        text=f"Hello, {message.from_user.full_name}!",
        reply_markup=keyboard_markup,
    )


class AddWishForm(StatesGroup):
    title = State()
    description = State()


@dp.message(F.text == ButtonText.ADD_WISH.value)
async def handle_add_wish(message: types.Message, state: FSMContext) -> None:
    await state.set_state(AddWishForm.title)
    await message.answer(text="Enter the title of your wish:")


@dp.message(AddWishForm.title)
async def process_title(message: types.Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(AddWishForm.description)
    await message.answer("Enter the description of your wish:")


@dp.message(AddWishForm.description)
async def process_description(message: types.Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(f"Title: {data['title']}, Description: {data['description']}")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
