"""Тесты для сервиса режима ChatGPT."""

from src.bot.services.chat_mode_service import ChatModeService


def test_chat_mode_is_disabled_by_default() -> None:
    """По умолчанию режим должен быть выключен."""
    service = ChatModeService()
    assert not service.is_enabled(1)


def test_chat_mode_enable_and_disable() -> None:
    """Сервис должен включать и выключать режим для пользователя."""
    service = ChatModeService()

    service.enable(42)
    assert service.is_enabled(42)

    service.disable(42)
    assert not service.is_enabled(42)
