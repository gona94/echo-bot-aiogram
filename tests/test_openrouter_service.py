"""Тесты для OpenRouterService."""

from __future__ import annotations

import json
from urllib import error

from _pytest.monkeypatch import MonkeyPatch
from src.bot.services.openrouter_service import OpenRouterService


class _FakeResponse:
    """Простейший мок-ответ для urllib."""

    def __init__(self, payload: dict[str, object]) -> None:
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        return None


def test_ask_sync_returns_content_from_choices(monkeypatch: MonkeyPatch) -> None:
    """Сервис должен извлекать текст ответа из JSON OpenRouter."""
    service = OpenRouterService(api_key="test-key", model="openai/gpt-4o-mini")

    def fake_urlopen(req: object, timeout: int = 30) -> _FakeResponse:
        payload = {
            "choices": [
                {"message": {"content": "  Привет! Это ответ модели.  "}},
            ]
        }
        return _FakeResponse(payload)

    monkeypatch.setattr(
        "src.bot.services.openrouter_service.request.urlopen",
        fake_urlopen,
    )

    result = service._ask_sync("Как дела?")
    assert result == "Привет! Это ответ модели."


def test_ask_sync_returns_friendly_message_for_401(monkeypatch: MonkeyPatch) -> None:
    """При ошибке авторизации должен возвращаться понятный текст."""
    service = OpenRouterService(api_key="bad-key", model="openai/gpt-4o-mini")

    def fake_urlopen(req: object, timeout: int = 30) -> _FakeResponse:
        raise error.HTTPError(
            url="https://openrouter.ai/api/v1/chat/completions",
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=None,
        )

    monkeypatch.setattr(
        "src.bot.services.openrouter_service.request.urlopen",
        fake_urlopen,
    )

    result = service._ask_sync("Привет")
    assert result == "Не удалось обратиться к OpenRouter: проверьте API-ключ."


def test_ask_returns_realtime_template_for_weather_query() -> None:
    """Запросы про актуальные данные должны получать честный шаблон."""
    service = OpenRouterService(api_key="test-key", model="openai/gpt-4o-mini")

    result = service._is_realtime_query("Какая погода сегодня в Тель-Авиве?")
    assert result is True
