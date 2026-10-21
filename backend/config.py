import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "supersecretkeythatyoushouldchangeinproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    DATABASE_URL: str = "sqlite:///./fuelbuddy.db"
    OSRM_API_KEY: str | None = None
    OPEN_CHARGE_MAP_API_KEY: str | None = None
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    class Config:
        env_file = ".env"

settings = Settings()
