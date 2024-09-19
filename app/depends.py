from typing import AsyncGenerator

from database.base import async_session
from fastapi import Depends
from service.news import NewsCRUDService
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_news_service(
    session: AsyncSession = Depends(get_session),
) -> "NewsCRUDService":
    return NewsCRUDService(session=session)
