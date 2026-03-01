from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    log_level: str
    app_env: str


def load_settings() -> Settings:
    """
    Load settings from environment variables.

    We call load_dotenv() so local development can use a .env file.
    In production, environment variables should be injected by the platform.
    """
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "Missing TELEGRAM_BOT_TOKEN. Add it to your .env (local) or environment variables (prod)."
        )

    return Settings(
        telegram_bot_token=token,
        log_level=os.getenv("LOG_LEVEL", "INFO").strip(),
        app_env=os.getenv("APP_ENV", "development").strip(),
    )