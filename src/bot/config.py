"""Конфигурация приложения."""

from dataclasses import dataclass

from dotenv import load_dotenv
import os


@dataclass(frozen=True)
class Config:
    """Настройки бота, загруженные из окружения."""

    bot_token: str
    openrouter_api_key: str
    openrouter_model: str


def load_config() -> Config:
    """Загружает .env и возвращает валидную конфигурацию."""
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    openrouter_model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini").strip()

    if not bot_token:
        raise ValueError(
            "Не задан BOT_TOKEN. Добавьте переменную BOT_TOKEN в файл .env."
        )

    if not openrouter_api_key:
        raise ValueError(
            "Не задан OPENROUTER_API_KEY. Добавьте переменную OPENROUTER_API_KEY в файл .env."
        )

    if not openrouter_model:
        raise ValueError(
            "Не задан OPENROUTER_MODEL. Добавьте переменную OPENROUTER_MODEL в файл .env."
        )

    return Config(
        bot_token=bot_token,
        openrouter_api_key=openrouter_api_key,
        openrouter_model=openrouter_model,
    )
