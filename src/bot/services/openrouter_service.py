"""Сервис для запросов к OpenRouter."""

from __future__ import annotations

import asyncio
import json
from urllib import error, request


class OpenRouterService:
    """Отправляет пользовательские сообщения в OpenRouter и возвращает ответ модели."""

    _API_URL = "https://openrouter.ai/api/v1/chat/completions"
    _SYSTEM_PROMPT = "Ты полезный и вежливый ассистент. Отвечай на русском языке."
    _REALTIME_TEMPLATE = (
        "Я не вижу интернет и не получаю данные в реальном времени, "
        "поэтому не могу дать точную актуальную информацию по этому запросу.\n\n"
        "Что можно сделать:\n"
        "- Проверить профильный источник (погода/курсы/новости).\n"
        "- Я могу помочь сформулировать, что именно искать и как сравнить данные."
    )

    def __init__(self, api_key: str, model: str) -> None:
        self._api_key = api_key
        self._model = model

    async def ask(self, user_text: str) -> str:
        """Возвращает ответ LLM на пользовательский вопрос."""
        if self._is_realtime_query(user_text):
            return self._REALTIME_TEMPLATE
        return await asyncio.to_thread(self._ask_sync, user_text)

    def _is_realtime_query(self, user_text: str) -> bool:
        """Определяет запросы, где нужны актуальные данные из внешних источников."""
        lowered = user_text.lower()
        weather_markers = (
            "погод",
            "температур",
            "weather",
        )
        news_markers = (
            "новост",
            "news",
        )
        finance_markers = (
            "курс валют",
            "курс доллара",
            "курс евро",
            "exchange rate",
            "currency rate",
            "доллар",
            "евро",
            "биткоин",
            "btc",
            "rate",
            "rates",
        )
        time_markers = ("сегодня", "сейчас", "прямо сейчас", "на сегодня", "now", "today")
        educational_markers = (
            "план курса",
            "курс по",
            "урок",
            "уроки",
            "обучени",
            "программа",
        )

        if any(marker in lowered for marker in educational_markers):
            return False

        has_weather_or_news = any(marker in lowered for marker in weather_markers + news_markers)
        has_finance = any(marker in lowered for marker in finance_markers)
        has_time_context = any(marker in lowered for marker in time_markers)

        return has_weather_or_news or (has_finance and has_time_context)

    def _ask_sync(self, user_text: str) -> str:
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": self._SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
        }
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost",
            "X-Title": "echo-bot-chatgpt-mode",
        }
        req = request.Request(self._API_URL, data=body, headers=headers, method="POST")

        try:
            with request.urlopen(req, timeout=30) as response:
                response_body = response.read().decode("utf-8")
        except error.HTTPError as http_error:
            # Возвращаем мягкое сообщение, чтобы бот не падал и не раскрывал секреты.
            if http_error.code == 401:
                return "Не удалось обратиться к OpenRouter: проверьте API-ключ."
            return f"OpenRouter вернул ошибку HTTP {http_error.code}."
        except error.URLError:
            return "Не удалось подключиться к OpenRouter. Проверьте интернет и попробуйте снова."

        try:
            parsed = json.loads(response_body)
            return parsed["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError, json.JSONDecodeError):
            return "OpenRouter вернул неожиданный ответ. Попробуйте повторить вопрос."
