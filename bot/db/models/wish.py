from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import UserModel


class WishModel(Base):
    __tablename__ = "wishes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    user_telegram_id: Mapped[int] = mapped_column(ForeignKey("users.telegram_id"))

    user: Mapped["UserModel"] = relationship(back_populates="wishes")
