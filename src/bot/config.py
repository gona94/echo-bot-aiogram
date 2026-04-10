"""Конфигурация приложения."""

from dataclasses import dataclass

from dotenv import load_dotenv
import os


@dataclass(frozen=True)
class Config:
    """Настройки бота, загруженные из окружения."""

    bot_token: str


def load_config() -> Config:
    """Загружает .env и возвращает валидную конфигурацию."""
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN", "").strip()

    if not bot_token:
        raise ValueError(
            "Не задан BOT_TOKEN. Добавьте переменную BOT_TOKEN в файл .env."
        )

    return Config(bot_token=bot_token)
