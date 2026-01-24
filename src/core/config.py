import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_SQLITE_URL = f"sqlite:///{ROOT_DIR / 'sqlite3.db'}"


@dataclass(frozen=True)
class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "ApiForHotelApp")
    DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)


settings = Settings()
