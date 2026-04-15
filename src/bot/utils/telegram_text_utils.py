"""Утилиты для текста с учетом ограничений Telegram."""

TELEGRAM_TEXT_LIMIT = 4096
TRUNCATION_SUFFIX = "\n\n[Ответ обрезан из-за ограничения Telegram]"


def trim_for_telegram(text: str, limit: int = TELEGRAM_TEXT_LIMIT) -> str:
    """Обрезает текст до лимита Telegram и добавляет пометку об обрезке."""
    if len(text) <= limit:
        return text

    if limit <= len(TRUNCATION_SUFFIX):
        return TRUNCATION_SUFFIX[:limit]

    effective_limit = limit - len(TRUNCATION_SUFFIX)
    return f"{text[:effective_limit]}{TRUNCATION_SUFFIX}"
