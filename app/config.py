from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Instagram Reels Automation")
    env: str = os.getenv("ENV", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    tts_model: str = os.getenv("TTS_MODEL", "gpt-4o-mini-tts")
    tts_voice_male: str = os.getenv("TTS_VOICE_MALE", "onyx")
    tts_voice_female: str = os.getenv("TTS_VOICE_FEMALE", "nova")

    instagram_access_token: str = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    instagram_business_account_id: str = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")
    instagram_api_version: str = os.getenv("INSTAGRAM_API_VERSION", "v20.0")

    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./reels.db")

    uploads_dir: Path = BASE_DIR / "uploads"
    generated_dir: Path = BASE_DIR / "generated"

    dry_run: bool = os.getenv("DRY_RUN", "true").lower() == "true"


settings = Settings()
