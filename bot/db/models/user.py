from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.db.model_types import created_at, intpk

from .base import Base

if TYPE_CHECKING:
    from .wish import WishModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    telegram_id: Mapped[int] = mapped_column(unique=True)
    created_at: Mapped[created_at]

    wishes: Mapped["WishModel"] = relationship(back_populates="user")
