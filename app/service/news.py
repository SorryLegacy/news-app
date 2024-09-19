import logging
from dataclasses import dataclass

from cachetools import LRUCache, cached
from database import News, NewsCreate, NewsPatch
from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

cache = LRUCache(maxsize=100)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class NewsCRUDService:
    session: AsyncSession

    async def list_all(self) -> list[News]:
        logger.info("Fetching all news")

        if "all_news" in cache:
            logger.info("Returning cached news")
            return cache["all_news"]

        query = select(News)
        result = await self.session.execute(statement=query)
        news = result.scalars().all()
        logger.info(f"Fetched {len(news)} news items")
        cache["all_news"] = news
        return news

    async def get_news(self, uuid: str) -> News:
        if f"{uuid}_news" in cache:
            logger.info("Returning cached news")
            return cache[f"{uuid}_news"]

        query = select(News).where(News.id == uuid)
        result = await self.session.execute(statement=query)
        news = result.scalar_one_or_none()

        if news is None:
            logger.error(f"News item with ID: {uuid} not found")
            raise HTTPException(status_code=404, detail="News not found")

        cache[f"{uuid}_news"] = news
        return news

    async def create(self, news: NewsCreate) -> News:
        logger.info("Creating new news item")
        new_news = News(**news.model_dump())
        self.session.add(new_news)

        await self.session.commit()
        await self.session.refresh(new_news)

        logger.info(f"Created news item with ID: {new_news.id}")
        cache.clear()
        return new_news

    async def delete(self, uuid: str) -> None:
        logger.info(f"Deleting news item with ID: {uuid}")
        query = delete(News).where(News.id == uuid)

        await self.session.execute(statement=query)
        await self.session.commit()

        cache.clear()
        logger.info("Deleted news item successfully")

    async def patch(self, uuid: str, update_news: NewsPatch) -> News:
        logger.info(f"Updating news item with ID: {uuid}")
        query = select(News).where(News.id == uuid)
        result = await self.session.execute(statement=query)
        news = result.scalar_one_or_none()

        if news is None:
            logger.error(f"News item with ID: {uuid} not found")
            raise HTTPException(status_code=404, detail="News not found")

        news_data = update_news.model_dump(exclude_unset=True)
        for key, value in news_data.items():
            logger.info(f"Updating '{key}' to '{value}'")
            setattr(news, key, value)

        self.session.add(news)
        await self.session.commit()
        await self.session.refresh(news)

        cache.clear()
        logger.info(f"Updated news item with ID: {news.id}")
        return news
