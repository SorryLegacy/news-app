from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(), nullable=False
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False,
    )


class BaseNews(SQLModel):
    name: str
    text: str


class News(BaseModel, BaseNews, table=True): ...


class NewsCreate(BaseNews): ...


class NewsPatch(SQLModel):
    name: Optional[str] = Field(default=None)
    text: Optional[str] = Field(default=None)
