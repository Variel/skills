#!/usr/bin/env python3
"""한국어 문서에서 검토할 표현을 찾는 보조 검사기입니다.

검사 결과는 자동 수정 지시가 아니라 사람이 문맥을 확인할 후보입니다.
인용문과 코드 블록은 검사하지 않습니다.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import cast


@dataclass(frozen=True)
class Rule:
    code: str
    pattern: re.Pattern[str]
    message: str


RULES = (
    Rule(
        "TRANSLATIONESE",
        re.compile(r"에\s*대해(?:서)?|에\s*있어서|가지고\s*있"),
        "번역투일 수 있습니다. 조사나 구체적인 동사로 직접 연결할 수 있는지 확인하세요.",
    ),
    Rule(
        "PASSIVE_TRANSLATION",
        re.compile(r"에\s*의해[^.!?\n]{0,30}?(?:되|진|받)|되어진|보여진"),
        "영어식 피동이나 이중 피동일 수 있습니다. 행위자를 주어로 쓰거나 피동을 하나만 남기세요.",
    ),
    Rule(
        "AI_CLICHE",
        re.compile(r"결론적으로|시사하는\s*바가\s*(?:크|있)|주목할\s*만"),
        "상투적인 결산이나 의의 과장입니다. 구체적인 결론을 직접 쓸 수 있는지 확인하세요.",
    ),
    Rule(
        "HEADING_SEQUENCE_CUE",
        re.compile(r"^\s{0,3}#{1,6}\s*(?:먼저|결론부터)\b", re.MULTILINE),
        "제목이 읽는 순서를 연출합니다. 아래 내용을 직접 나타내는 제목인지 확인하세요.",
    ),
    Rule(
        "CONCLUSION_FIRST",
        re.compile(r"(?:^|[.!?]\s+|\n)\s*결론부터(?:\s+말하자면|\s+말하면)?\b"),
        "결론을 직접 쓰지 않고 도입구로 예고합니다. 도입구가 필요한지 확인하세요.",
    ),
    Rule(
        "SEQUENCE_CUE",
        re.compile(
            r"(?:^|[.!?]\s+|\n)\s*먼저\s+"
            r"(?:말씀드리면|말하면|살펴보면|알아보면|확인하면)"
        ),
        "읽는 순서를 연출하는 도입입니다. 일정이나 결론을 바로 쓸 수 있는지 확인하세요.",
    ),
    Rule(
        "A_NOT_B",
        re.compile(
            r"(?:중요한\s+것은|핵심은|본질은|문제는|목표는|\S+한\s+것은|\S+는)"
            r"[^.!?\n]{0,60}?(?:이|가|은|는)?\s*아니라\s+"
            r"|[가-힣A-Za-z0-9_]+(?:이|가|은|는)?\s+아니라\s+"
        ),
        "'A가 아니라 B' 대조가 강조를 위한 공식인지 확인하고, 필요 없으면 B를 직접 쓰세요.",
    ),
    Rule(
        "SILENTLY_LITERAL",
        re.compile(
            r"(?:실패|오류|예외|경고|항목|요청|설정|변경|업데이트|패치)[^.!?\n]{0,30}?조용히\s+"
            r"(?:실패|무시|건너|생략|처리|넘어|제거|삭제|바뀌|변경|진행|적용)"
            r"|조용히\s+(?:실패|무시|건너|생략)"
        ),
        "소리가 아니라 표시나 안내의 부재를 뜻하면 '조용히' 대신 실제 동작을 쓰세요.",
    ),
    Rule(
        "MECHANICAL_CONTRAST",
        re.compile(r"\b\S+는\s+[^.!?\n]{1,60}?(?:는데|지만)\s+\S+는\s+"),
        "두 절을 기계적으로 대칭시킨 문장인지 확인하고, 실제 비교 기준을 직접 쓰세요.",
    ),
    Rule(
        "METAPHORIC_VERB",
        re.compile(
            r"(?:격차|차이|갭)[^.!?\n]{0,15}?닫(?:는|습니다|다|아|고)"
            r"|코드[^.!?\n]{0,20}?박(?:는|습니다|다|아|고)"
        ),
        "영어식 또는 업계식 은유입니다. '줄인다', '명시한다'처럼 실제 동작을 쓰세요.",
    ),
    Rule(
        "SHOWY_MARKETING",
        re.compile(
            r"새로운\s+시대를\s+여는|판을\s+바꾸는|보이지\s+않는\s+혁명"
            r"|조용히\s+무너지는|게임\s*체인저|패러다임의\s+전환"
            r"|업계를\s+뒤흔드는|미래를\s+재정의하는"
            r"|(?:혁신적|획기적|압도적|전례\s+없는)(?:인|인\s+|\s+)"
        ),
        "정보보다 인상을 앞세운 마케팅 문구일 수 있습니다. 구체적인 대상과 변화를 쓰세요.",
    ),
    Rule(
        "CONTEXTUAL_JARGON",
        re.compile(
            r"(?:런타임|모듈|실행|책임)\s*경계"
            r"|텍스트\s*위생"
            r"|(?:실행|입출력|도구|에이전트)\s*계약"
        ),
        "전문적으로 보이게 만든 직역어일 수 있습니다. 해당 분야에서 통용되는지 확인하세요.",
    ),
)


FENCE_RE = re.compile(r"^\s*(```|~~~)")
QUOTE_LINE_RE = re.compile(r"^\s*>")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
DIRECT_QUOTE_RE = re.compile(r'"[^"\n]*"|“[^”\n]*”')
BULLET_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def _format_findings(text: str, genre: str) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    lines = text.splitlines()
    run_start = 0
    run_length = 0
    longest_start = 0
    longest_length = 0
    for index, line in enumerate(lines, start=1):
        if BULLET_RE.match(line):
            if run_length == 0:
                run_start = index
            run_length += 1
            if run_length > longest_length:
                longest_start, longest_length = run_start, run_length
        else:
            run_length = 0

    if genre in {"explanation", "report"} and longest_length >= 5:
        findings.append(
            {
                "code": "EXCESSIVE_BULLETS",
                "line": longest_start,
                "column": 1,
                "excerpt": f"연속 불릿 {longest_length}개",
                "message": "연속 설명을 목록으로 분해했는지 확인하고, 맥락이 이어지면 문단으로 합치세요.",
            }
        )

    bold_matches = list(BOLD_RE.finditer(text))
    visible_chars = len(re.sub(r"\s+", "", text))
    bold_chars = sum(len(re.sub(r"\s+", "", match.group(1))) for match in bold_matches)
    if len(bold_matches) >= 4 and visible_chars and bold_chars / visible_chars > 0.4:
        line, column = _position(text, bold_matches[0].start())
        findings.append(
            {
                "code": "EXCESSIVE_BOLD",
                "line": line,
                "column": column,
                "excerpt": f"볼드 구간 {len(bold_matches)}개",
                "message": "강조가 정보 위계를 드러내는지 확인하고, 장식적인 볼드는 줄이세요.",
            }
        )
    return findings


def _masked_text(text: str) -> str:
    """코드 블록·인용문·인라인 코드를 같은 길이의 공백으로 가립니다."""
    masked: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines(keepends=True):
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence, fence_marker = True, marker
            elif marker == fence_marker:
                in_fence, fence_marker = False, ""
            masked.append("".join("\n" if ch == "\n" else " " for ch in line))
            continue
        if in_fence or QUOTE_LINE_RE.match(line):
            masked.append("".join("\n" if ch == "\n" else " " for ch in line))
            continue
        without_quotes = DIRECT_QUOTE_RE.sub(lambda m: " " * len(m.group(0)), line)
        masked.append(INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), without_quotes))
    return "".join(masked)


def _position(text: str, offset: int) -> tuple[int, int]:
    line = text.count("\n", 0, offset) + 1
    line_start = text.rfind("\n", 0, offset) + 1
    return line, offset - line_start + 1


def _excerpt(text: str, start: int, end: int) -> str:
    value = " ".join(text[start:end].split())
    return value[:120]


def lint_text(text: str, genre: str = "explanation") -> list[dict[str, object]]:
    masked = _masked_text(text)
    findings = _format_findings(masked, genre)
    seen: set[tuple[str, int]] = set()
    for rule in RULES:
        for match in rule.pattern.finditer(masked):
            start = match.start()
            if rule.code in {"CONCLUSION_FIRST", "SEQUENCE_CUE"}:
                cue = "결론부터" if rule.code == "CONCLUSION_FIRST" else "먼저"
                cue_offset = match.group(0).find(cue)
                if cue_offset >= 0:
                    start += cue_offset
            line, column = _position(text, start)
            key = (rule.code, line)
            if key in seen:
                continue
            seen.add(key)
            findings.append(
                {
                    "code": rule.code,
                    "line": line,
                    "column": column,
                    "excerpt": _excerpt(text, start, match.end()),
                    "message": rule.message,
                }
            )
    return sorted(
        findings,
        key=lambda item: (
            cast(int, item["line"]),
            cast(int, item["column"]),
            cast(str, item["code"]),
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="k-writing 한국어 표현 검사")
    parser.add_argument("path", type=Path)
    parser.add_argument("--genre", default="explanation")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    findings = lint_text(args.path.read_text(encoding="utf-8"), args.genre)
    if args.json:
        print(json.dumps(findings, ensure_ascii=False, indent=2))
    else:
        for finding in findings:
            print(f"{finding['line']}:{finding['column']} [{finding['code']}] {finding['message']}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
