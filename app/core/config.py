from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./websites.db"
    # HTTP_TIMEOUT: int = 5
    CHECK_CONCURRENCY: int = 10
    GLOBAL_CHECK_INTERVAL: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
