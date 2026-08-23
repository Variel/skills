import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "k-writing"


def load_module(filename: str):
    path = SKILL_DIR / "scripts" / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_linter():
    return load_module("lint_korean.py")


def test_k_writing_replaces_right_documentation_with_full_suite_layout():
    assert not (ROOT / "skills" / "right-documentation").exists()
    assert (SKILL_DIR / "SKILL.md").is_file()
    assert (SKILL_DIR / "references" / "korean-style-rules.md").is_file()
    assert (SKILL_DIR / "references" / "document-genre-formatting.md").is_file()
    assert (SKILL_DIR / "references" / "fidelity-checklist.md").is_file()
    assert (SKILL_DIR / "scripts" / "lint_korean.py").is_file()
    assert (SKILL_DIR / "scripts" / "verify_fidelity.py").is_file()

    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "name: k-writing" in skill
    assert "반드시 이 스킬을 사용" in skill
    assert "## When to Use" not in skill
    assert '${SKILL_DIR}/scripts/lint_korean.py' in skill
    assert '${SKILL_DIR}/scripts/verify_fidelity.py' in skill


def test_linter_detects_showy_and_literal_translation_patterns():
    linter = load_linter()
    text = """# 먼저 알아야 할 것
결론부터 말하면, 중요한 것은 속도가 아니라 방향입니다.
이 설정은 실패를 조용히 건너뜁니다.
A는 요청을 처리하는데 B는 결과를 검증합니다.
코드에 값을 박습니다. 이 변경은 격차를 닫습니다.
런타임 경계와 텍스트 위생을 실행 계약으로 관리합니다.
"""

    findings = linter.lint_text(text)
    codes = {finding["code"] for finding in findings}

    assert next(
        finding["line"] for finding in findings if finding["code"] == "CONCLUSION_FIRST"
    ) == 2
    assert {
        "HEADING_SEQUENCE_CUE",
        "CONCLUSION_FIRST",
        "A_NOT_B",
        "SILENTLY_LITERAL",
        "MECHANICAL_CONTRAST",
        "METAPHORIC_VERB",
        "CONTEXTUAL_JARGON",
    } <= codes


def test_format_lint_is_genre_aware_for_bullets_and_bold():
    linter = load_linter()
    text = """- **결정:** A를 적용합니다.
- **기한:** 금요일입니다.
- **담당:** 운영팀입니다.
- **상태:** 검토 중입니다.
- **위험:** 승인 지연입니다.
"""

    summary_codes = {finding["code"] for finding in linter.lint_text(text, "summary")}
    explanation_codes = {
        finding["code"] for finding in linter.lint_text(text, "explanation")
    }

    assert "EXCESSIVE_BULLETS" not in summary_codes
    assert "EXCESSIVE_BOLD" not in summary_codes
    assert "EXCESSIVE_BULLETS" in explanation_codes


def test_format_lint_ignores_bullets_and_bold_inside_code_blocks():
    linter = load_linter()
    text = """```markdown
- **하나**
- **둘**
- **셋**
- **넷**
- **다섯**
```
"""

    assert linter.lint_text(text, "explanation") == []


def test_linter_detects_common_translationese_without_flagging_quotes_or_code():
    linter = load_linter()
    text = """정책에 대해 논의하고, 시스템에 의해 생성되어진 결과를 확인합니다.
결론적으로 이는 시사하는 바가 큽니다.

> 중요한 것은 속도가 아니라 방향입니다.
앨리스는 "중요한 것은 속도가 아니라 방향입니다."라고 말했습니다.

```text
오류를 조용히 건너뜁니다.
```
"""

    codes = [finding["code"] for finding in linter.lint_text(text)]

    assert "TRANSLATIONESE" in codes
    assert "PASSIVE_TRANSLATION" in codes
    assert "AI_CLICHE" in codes
    assert "A_NOT_B" not in codes
    assert "SILENTLY_LITERAL" not in codes


def test_linter_detects_requested_style_variants():
    linter = load_linter()
    cases = {
        "속도가 아니라 안정성이 중요합니다.": "A_NOT_B",
        "먼저 말씀드리면 일정은 금요일입니다.": "SEQUENCE_CUE",
        "설정을 조용히 적용합니다.": "SILENTLY_LITERAL",
        "새로운 시대를 여는 판을 바꾸는 혁명입니다.": "SHOWY_MARKETING",
    }

    for text, expected_code in cases.items():
        codes = {finding["code"] for finding in linter.lint_text(text)}
        assert expected_code in codes, text


def test_linter_allows_natural_spatial_through_expression():
    linter = load_linter()

    for text in (
        "창문을 통해 바깥을 봅니다.",
        "데이터를 통해 사실을 확인합니다.",
    ):
        codes = {finding["code"] for finding in linter.lint_text(text)}
        assert "TRANSLATIONESE" not in codes


def test_linter_detects_broader_showy_marketing_phrases():
    linter = load_linter()

    codes = {
        finding["code"]
        for finding in linter.lint_text("업계를 뒤흔드는 혁신적인 솔루션입니다.")
    }

    assert "SHOWY_MARKETING" in codes


def test_fidelity_verifier_reports_changed_protected_items():
    verifier = load_module("verify_fidelity.py")
    before = """# 배포 조건
2026-08-25까지 1,200건을 처리합니다.
자세한 내용은 https://example.com/spec을 확인하세요.
담당자는 "승인 후 배포합니다"라고 말했습니다.
`release-v2`를 실행합니다.
"""
    after = """# 운영 조건
2026-08-26까지 1,500건을 처리합니다.
자세한 내용은 https://example.com/guide를 확인하세요.
담당자는 "검토 후 배포합니다"라고 말했습니다.
`release-v3`를 실행합니다.
"""

    codes = {failure["code"] for failure in verifier.verify(before, after)}

    assert {
        "NUMBER_CHANGED",
        "URL_CHANGED",
        "QUOTE_CHANGED",
        "INLINE_CODE_CHANGED",
        "HEADING_CHANGED",
    } <= codes


def test_fidelity_verifier_accepts_style_only_edits():
    verifier = load_module("verify_fidelity.py")
    before = "# 배포 조건\n정책에 대해 논의하고 2026-08-25에 `release-v2`를 실행합니다."
    after = "# 배포 조건\n정책을 논의한 뒤 2026-08-25에 `release-v2`를 실행합니다."

    assert verifier.verify(before, after) == []


def test_fidelity_verifier_detects_reordered_protected_items():
    verifier = load_module("verify_fidelity.py")
    before = '# 현황\n앨리스는 10건, 밥은 20건입니다.\n앨리스: "승인"\n밥: "거절"'
    after = '# 현황\n앨리스는 20건, 밥은 10건입니다.\n앨리스: "거절"\n밥: "승인"'

    codes = {failure["code"] for failure in verifier.verify(before, after)}

    assert "NUMBER_CONTEXT_CHANGED" in codes
    assert "QUOTE_CONTEXT_CHANGED" in codes


def test_fidelity_verifier_detects_units_and_signs():
    verifier = load_module("verify_fidelity.py")
    cases = (
        ("저장 용량은 10GB이고 온도는 -5도입니다.", "저장 용량은 10MB이고 온도는 +5도입니다."),
        ("메모리는 10GiB, 파일은 20MiB입니다.", "메모리는 10MiB, 파일은 20GiB입니다."),
    )

    for before, after in cases:
        codes = {failure["code"] for failure in verifier.verify(before, after)}
        assert "NUMBER_CHANGED" in codes


def test_fidelity_verifier_detects_changed_token_ownership():
    verifier = load_module("verify_fidelity.py")
    before = '앨리스는 10건, 밥은 20건입니다.\n앨리스: "승인"\n밥: "거절"'
    after = '밥은 10건, 앨리스는 20건입니다.\n밥: "승인"\n앨리스: "거절"'

    codes = {failure["code"] for failure in verifier.verify(before, after)}

    assert "NUMBER_CONTEXT_CHANGED" in codes
    assert "QUOTE_CONTEXT_CHANGED" in codes


def test_fidelity_verifier_detects_single_token_ownership_change():
    verifier = load_module("verify_fidelity.py")
    cases = (
        ("앨리스는 10건입니다.", "밥은 10건입니다.", "NUMBER_CONTEXT_CHANGED"),
        ('앨리스: "승인"', '밥: "승인"', "QUOTE_CONTEXT_CHANGED"),
        ("10건은 앨리스가 처리했습니다.", "10건은 밥이 처리했습니다.", "NUMBER_CONTEXT_CHANGED"),
        ("프로젝트는 앨리스가 10건을 처리했습니다.", "프로젝트는 밥이 10건을 처리했습니다.", "NUMBER_CONTEXT_CHANGED"),
        ('"승인합니다"라고 앨리스가 말했습니다.', '"승인합니다"라고 밥이 말했습니다.', "QUOTE_CONTEXT_CHANGED"),
        (
            '앨리스가 다음과 같이 말했습니다.\n"승인합니다"',
            '밥이 다음과 같이 말했습니다.\n"승인합니다"',
            "QUOTE_CONTEXT_CHANGED",
        ),
    )

    for before, after, expected_code in cases:
        codes = {failure["code"] for failure in verifier.verify(before, after)}
        assert expected_code in codes


def test_fidelity_verifier_allows_rephrasing_and_reordering_with_same_ownership():
    verifier = load_module("verify_fidelity.py")
    cases = (
        (
            "앨리스는 10건입니다. 밥은 20건입니다.",
            "밥의 처리량은 20건입니다. 앨리스가 처리한 건수는 10건입니다.",
        ),
        (
            "앨리스는 10건을 처리했습니다.",
            "처리한 건수는 앨리스 기준 10건입니다.",
        ),
    )

    for before, after in cases:
        assert verifier.verify(before, after) == []


def test_fidelity_verifier_allows_particle_edits_around_numbers():
    verifier = load_module("verify_fidelity.py")
    before = "앨리스는 10건, 밥은 20건입니다."
    after = "앨리스가 10건, 밥이 20건입니다."

    assert verifier.verify(before, after) == []


def test_fidelity_verifier_does_not_include_korean_particles_in_urls():
    verifier = load_module("verify_fidelity.py")
    before = "https://example.com/spec을 확인합니다."
    after = "https://example.com/spec를 확인합니다."

    assert verifier.verify(before, after) == []


def test_fidelity_verifier_detects_heading_hierarchy_changes():
    verifier = load_module("verify_fidelity.py")
    cases = (
        ("## 제한 사항\n내용", "### 제한 사항\n내용"),
        (
            "# 문서\n## A\na\n## B\nb",
            "# 문서\n## B\nb\n## A\na",
        ),
    )

    for before, after in cases:
        codes = {failure["code"] for failure in verifier.verify(before, after)}
        assert "HEADING_CHANGED" in codes


def test_documented_policy_covers_requested_korean_style_cases():
    style = (SKILL_DIR / "references" / "korean-style-rules.md").read_text(
        encoding="utf-8"
    )
    formatting = (
        SKILL_DIR / "references" / "document-genre-formatting.md"
    ).read_text(encoding="utf-8")

    for phrase in (
        "A한 것은 B가 아니라 C다",
        "먼저",
        "결론부터",
        "silently",
        "계약",
        "경계",
        "위생",
        "A는 ~하는데 B는 ~합니다",
        "닫는다",
        "박습니다",
        "사전에 등재됐다는 이유만으로",
        "비유",
        "마케팅 문구",
    ):
        assert phrase in style

    assert "불릿, 번호 목록, 표와 볼드는 AI 문체의 증거가 아닙니다" in formatting
    assert "요약" in formatting
    assert "브리핑" in formatting
