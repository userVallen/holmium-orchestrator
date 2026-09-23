from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    gemini_api_key: str
    database_url: str
    database_url_async: str
    database_url_sync: str
    fast_model: str = "gemini-3.5-flash-lite"
    reasoning_model: str = "gemini-3.6-pro"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
