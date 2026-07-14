"""Application settings loaded from environment variables / .env file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_ENV: str = "development"
    APP_NAME: str = "realfarm"

    # URLs
    API_BASE_URL: str = "http://localhost:8000"
    WEB_BASE_URL: str = "http://localhost:5173"

    # Database Selection
    DB_TYPE: str = "sqlite"  # "postgres" or "sqlite"
    SQLITE_DB_PATH: str = "realfarm.db"

    # Database (PostgreSQL + TimescaleDB)
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "realfarm"
    POSTGRES_USER: str = "realfarm"
    POSTGRES_PASSWORD: str = "change_me"

    # JWT
    JWT_SECRET: str = "change_me_use_a_long_random_string_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Refresh Token
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # MQTT
    MQTT_HOST: str = "localhost"
    MQTT_PORT: int = 1883
    MQTT_USERNAME: str = "realfarm"
    MQTT_PASSWORD: str = "change_me"

    # AI Service
    AI_SERVICE_URL: str = "http://localhost:8100"

    # Optional integrations
    BLOCKCHAIN_ENABLED: bool = False
    MEDIA_STORAGE_PATH: str = "./data/media"

    @property
    def database_url(self) -> str:
        if self.DB_TYPE == "sqlite":
            return f"sqlite+aiosqlite:///{self.SQLITE_DB_PATH}"
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def database_url_sync(self) -> str:
        """Synchronous URL used by Alembic migrations."""
        if self.DB_TYPE == "sqlite":
            return f"sqlite:///{self.SQLITE_DB_PATH}"
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
