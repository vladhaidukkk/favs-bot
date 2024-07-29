from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.model_types import created_at, intpk, updated_at

from .base import Base

if TYPE_CHECKING:
    from .user import UserModel


class WishModel(Base):
    __tablename__ = "wishes"

    id: Mapped[intpk]
    title: Mapped[str]
    description: Mapped[str | None]
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped["UserModel"] = relationship(back_populates="wishes")
