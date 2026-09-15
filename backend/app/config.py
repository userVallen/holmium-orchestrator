from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    database_url: str
    fast_model: str = "gemini-3.6-flash"
    reasoning_model: str = "gemini-3.6-pro"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
