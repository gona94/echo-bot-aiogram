"""Точка совместимости для запуска бота из корня проекта."""

import asyncio

from src.bot.main import main


if __name__ == "__main__":
    # Оставлено для привычного запуска командой `python bot.py`.
    asyncio.run(main())
