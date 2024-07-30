import asyncio
import logging
import sys
from enum import Enum

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.utils import markdown
from sqlalchemy import insert, select

from bot.config import settings
from bot.db.core import session_factory
from bot.db.models import UserModel, WishModel

dp = Dispatcher()


class ButtonText(Enum):
    ADD_WISH = "✨Add a Wish"
    SHOW_ALL_WISHES = "📜 Show All Wishes"


@dp.message(CommandStart())
async def handle_start(message: Message) -> None:
    async with session_factory() as session:
        query = select(UserModel).filter_by(telegram_id=message.from_user.id)
        result = await session.execute(query)
        existing_user = result.scalar_one_or_none()
        if not existing_user:
            stmt = insert(UserModel).values(telegram_id=message.from_user.id)
            await session.execute(stmt)
            await session.commit()

    buttons = [
        KeyboardButton(text=ButtonText.ADD_WISH.value),
        KeyboardButton(text=ButtonText.SHOW_ALL_WISHES.value),
    ]
    keyboard_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)
    await message.answer(
        text=f"Hello, {message.from_user.full_name}!",
        reply_markup=keyboard_markup,
    )


class AddWishForm(StatesGroup):
    title = State()
    description = State()


@dp.message(F.text == ButtonText.ADD_WISH.value)
async def handle_add_wish(message: Message, state: FSMContext) -> None:
    await state.set_state(AddWishForm.title)
    await message.answer(text="Enter the title of your wish:")


@dp.message(AddWishForm.title)
async def process_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(AddWishForm.description)
    await message.answer("Enter the description of your wish:")


@dp.message(AddWishForm.description)
async def process_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    data = await state.get_data()
    await state.clear()

    async with session_factory() as session:
        new_wish = WishModel(
            title=data["title"],
            description=data["description"],
            user_telegram_id=message.from_user.id,
        )
        session.add(new_wish)
        await session.commit()

    await message.answer(f"New wish with ID: {new_wish.id} was created!")


@dp.message(F.text == ButtonText.SHOW_ALL_WISHES.value)
async def handle_show_all_wishes(message: Message) -> None:
    async with session_factory() as session:
        query = select(WishModel).filter_by(user_telegram_id=message.from_user.id)
        result = await session.execute(query)
        wishes = result.scalars().all()

    text = markdown.text(
        *(f"{idx}. {wish.title}" for idx, wish in enumerate(wishes, start=1)),
        sep="\n",
    )
    await message.answer(text=text, parse_mode=ParseMode.HTML)


async def main() -> None:
    bot = Bot(token=settings.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
