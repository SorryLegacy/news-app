from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_port: int
    database_db: str
    database_host: str
    database_user: str
    database_password: str

    @property
    def database_uri(self) -> str:
        return f"postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_db}"


@lru_cache()
def get_settings() -> "Settings":
    return Settings()


settings = get_settings()
