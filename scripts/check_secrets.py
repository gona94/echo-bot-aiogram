"""Проверка staged-изменений на случайную утечку секретов."""

from __future__ import annotations

import re
import subprocess
import sys
from typing import Iterable


FORBIDDEN_FILE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(^|[\\/])\.env($|\.|[\\/])", re.IGNORECASE),
    re.compile(r"(^|[\\/])mcp\.json$", re.IGNORECASE),
)

SECRET_LINE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("Found BOT_TOKEN variable", re.compile(r"\bBOT_TOKEN\s*=")),
    ("Found CONTEXT7_API_KEY variable", re.compile(r"\bCONTEXT7_API_KEY\s*=")),
    ("Found Context7 API key", re.compile(r"ctx7sk-[A-Za-z0-9-]+")),
    (
        "Found a string similar to Telegram Bot Token",
        re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{20,}\b"),
    ),
)


def _run_git_command(args: list[str]) -> str:
    """Запускает git-команду и возвращает stdout как строку."""
    result = subprocess.run(
        ["git", *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        print("Failed to execute git command:", " ".join(args), file=sys.stderr)
        print(result.stderr.strip(), file=sys.stderr)
        raise SystemExit(2)
    return result.stdout


def _get_staged_files() -> list[str]:
    """Возвращает список файлов, добавленных в staged."""
    output = _run_git_command(["diff", "--cached", "--name-only", "--diff-filter=ACMR"])
    return [line.strip() for line in output.splitlines() if line.strip()]


def _iter_added_lines_from_diff() -> Iterable[str]:
    """Итерирует только добавленные строки из staged-diff."""
    diff_text = _run_git_command(["diff", "--cached", "--unified=0", "--no-color"])
    for line in diff_text.splitlines():
        if line.startswith("+++"):
            continue
        if line.startswith("+"):
            yield line[1:]


def main() -> int:
    """Точка входа скрипта проверки."""
    problems: list[str] = []

    for path in _get_staged_files():
        for pattern in FORBIDDEN_FILE_PATTERNS:
            if pattern.search(path):
                problems.append(f"Sensitive file found in staged changes: {path}")
                break

    for added_line in _iter_added_lines_from_diff():
        for message, pattern in SECRET_LINE_PATTERNS:
            if pattern.search(added_line):
                problems.append(f"{message}: `{added_line[:120]}`")

    if problems:
        print("\nERROR: secret check failed.\n")
        for item in problems:
            print(f"- {item}")
        print(
            "\nCommit blocked. Remove secrets from staged changes and retry commit.",
            file=sys.stderr,
        )
        return 1

    print("Secret check passed: no secrets found in staged changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
