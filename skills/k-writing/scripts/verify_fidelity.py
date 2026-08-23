#!/usr/bin/env python3
"""문체 수정 전후의 보호 항목을 비교합니다.

이 검사는 내용 편집을 마친 초안과 한국어 문체를 다듬은 최종본 사이에
수치, URL, 직접 인용, 인라인 코드와 제목이 바뀌었는지 확인합니다.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Callable


NUMBER_RE = re.compile(
    r"(?<![A-Za-z0-9_])[-+]?\d+(?:[.,:/-]\d+)*"
    r"(?:\s?(?:[A-Za-zµμ]{1,8}|%|％|원|달러|초|분|시간|일|주|개월|년|명|건|개|회|도|℃|°C|km|cm|mm|kg|페이지|쪽|배|m|s|g))?"
    r"(?![A-Za-z0-9_])"
)
URL_RE = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+")
QUOTE_RE = re.compile(r'["“](.*?)["”]', re.DOTALL)
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
OWNER_RE = re.compile(
    r"([가-힣A-Za-z][가-힣A-Za-z0-9_-]{0,30})(?:에게서|에게|은|는|이|가|의)"
    r"(?=\s|[가-힣]|$)"
)


def _extract(pattern: re.Pattern[str], text: str) -> list[str]:
    values: list[str] = []
    for match in pattern.finditer(text):
        values.append(match.group(1) if pattern.groups else match.group(0))
    return values


GENERIC_OWNER_WORDS = {"건수", "처리량", "수량", "값", "합계", "평균", "총계"}
CRITERION_OWNER_RE = re.compile(
    r"([가-힣A-Za-z][가-힣A-Za-z0-9_-]{0,30})\s+기준"
)


def _owner_candidates(segment: str) -> list[str]:
    normalized = " ".join(segment.split()).strip()
    found: list[tuple[int, str]] = []
    for match in OWNER_RE.finditer(normalized):
        found.append((match.start(), match.group(1)))
    for match in CRITERION_OWNER_RE.finditer(normalized):
        found.append((match.start(), match.group(1)))
    colon_owner = re.search(
        r"([가-힣A-Za-z][가-힣A-Za-z0-9_-]{0,30})\s*[:：]\s*$",
        normalized,
    )
    if colon_owner:
        found.append((colon_owner.start(), colon_owner.group(1)))
    return [
        owner
        for _, owner in sorted(found)
        if owner not in GENERIC_OWNER_WORDS
    ]


def _next_boundary(text: str, start: int, separators: str) -> int:
    positions = [text.find(char, start) for char in separators]
    valid = [position for position in positions if position >= 0]
    return min(valid) if valid else len(text)


def _owner_around(text: str, start: int, end: int) -> str | None:
    separators = "\n.!?;,"
    before_boundary = max(text.rfind(char, 0, start) for char in separators)
    after_boundary = _next_boundary(text, end, separators)
    before = _owner_candidates(text[before_boundary + 1 : start])
    after = _owner_candidates(text[end:after_boundary])
    if before:
        return before[-1]
    if after:
        return after[0]

    line_start = text.rfind("\n", 0, start)
    if line_start >= 0:
        previous_lines = [line for line in text[:line_start].splitlines() if line.strip()]
        if previous_lines:
            previous = previous_lines[-1]
            if re.search(r"(?:말|설명|밝|답|전달)(?:했|합니|하였)", previous):
                candidates = _owner_candidates(previous)
                if candidates:
                    return candidates[0]
    return None


def _contextual_extract(pattern: re.Pattern[str], text: str) -> list[str]:
    values: list[str] = []
    for match in pattern.finditer(text):
        owner = _owner_around(text, match.start(), match.end())
        if owner is None:
            continue
        token = match.group(1) if pattern.groups else match.group(0)
        values.append(f"{owner}→{token}")
    return values


def _extract_headings(text: str) -> list[str]:
    stack: list[tuple[int, str]] = []
    headings: list[str] = []
    for match in HEADING_RE.finditer(text):
        level = len(match.group(1))
        title = " ".join(match.group(2).split())
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_path = "/".join(parent for _, parent in stack)
        headings.append(f"{level}|{parent_path}|{title}")
        stack.append((level, title))
    return headings


def _difference(before: list[str], after: list[str]) -> dict[str, object]:
    before_counts = Counter(before)
    after_counts = Counter(after)
    return {
        "removed": sorted((before_counts - after_counts).elements()),
        "added": sorted((after_counts - before_counts).elements()),
    }


def _failure(
    code: str,
    label: str,
    before: list[str],
    after: list[str],
) -> dict[str, object] | None:
    if Counter(before) == Counter(after):
        return None
    difference = _difference(before, after)
    return {
        "code": code,
        "message": f"{label}의 값이나 귀속 관계가 변경됐습니다.",
        **difference,
    }


def _ordered_failure(
    code: str,
    label: str,
    before: list[str],
    after: list[str],
) -> dict[str, object] | None:
    if before == after:
        return None
    return {
        "code": code,
        "message": f"{label}의 값, 계층 또는 순서가 변경됐습니다.",
        **_difference(before, after),
        "order_changed": Counter(before) == Counter(after),
    }


def verify(before: str, after: str) -> list[dict[str, object]]:
    checks: tuple[tuple[str, str, Callable[[str], list[str]]], ...] = (
        ("NUMBER_CHANGED", "수치·날짜·단위", lambda text: _extract(NUMBER_RE, text)),
        (
            "NUMBER_CONTEXT_CHANGED",
            "수치의 주변 대상",
            lambda text: _contextual_extract(NUMBER_RE, text),
        ),
        ("URL_CHANGED", "URL", lambda text: _extract(URL_RE, text)),
        ("QUOTE_CHANGED", "직접 인용", lambda text: _extract(QUOTE_RE, text)),
        (
            "QUOTE_CONTEXT_CHANGED",
            "직접 인용의 화자·주변 대상",
            lambda text: _contextual_extract(QUOTE_RE, text),
        ),
        (
            "INLINE_CODE_CHANGED",
            "인라인 코드·식별자",
            lambda text: _extract(INLINE_CODE_RE, text),
        ),
    )
    failures: list[dict[str, object]] = []
    for code, label, extractor in checks:
        failure = _failure(code, label, extractor(before), extractor(after))
        if failure is not None:
            failures.append(failure)
    heading_failure = _ordered_failure(
        "HEADING_CHANGED",
        "마크다운 제목",
        _extract_headings(before),
        _extract_headings(after),
    )
    if heading_failure is not None:
        failures.append(heading_failure)
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="k-writing 내용 보존 검사")
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    failures = verify(
        args.before.read_text(encoding="utf-8"),
        args.after.read_text(encoding="utf-8"),
    )
    if args.json:
        print(json.dumps(failures, ensure_ascii=False, indent=2))
    else:
        for failure in failures:
            print(f"[{failure['code']}] {failure['message']}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
