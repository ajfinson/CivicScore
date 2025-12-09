"""Env-based app config loader"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str
    openai_api_key: str
    openai_base_url: str = "https://api.openai.com/v1"
    log_level: str = "INFO"
    environment: str = "development"
    
    class Config:
        env_file = ".env"


settings = Settings()
