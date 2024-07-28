from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.config import settings

engine = create_async_engine(
    url=settings.db.url.unicode_string(), echo=True, echo_pool=True
)
session_factory = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)
