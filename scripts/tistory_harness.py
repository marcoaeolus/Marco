#!/usr/bin/env python3
"""Small Codex harness for Marco's Tistory blog workflow."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


SLOTS = {
    0: "09:00",  # Monday
    1: "18:00",  # Tuesday
    3: "09:00",  # Thursday
    4: "18:00",  # Friday
}

CATEGORY_MIN_CHARS = {
    "국내여행": 1500,
    "해외여행": 1500,
    "여행": 1500,
    "맛집": 1200,
    "카페": 1200,
    "카페·디저트": 1200,
    "IT": 2000,
    "IT제품리뷰": 2000,
    "사진": 600,
    "사진/일상": 600,
    "쇼핑": 1000,
    "호텔리뷰": 1200,
    "스튜디오 운영 노트": 1000,
}

# 2026-07-19 확정: 카테고리별 필수 태그(연도·카메라 다음 순번). 값이 없는 카테고리는
# 아직 필수 태그 미정 상태(guidelines/03_seo_checklist.md E 참고).
CATEGORY_REQUIRED_TAGS = {
    "맛집": ("맛집", "사진"),
    "국내여행": ("국내여행", "사진"),
    "해외여행": ("해외여행", "사진"),
    "여행": ("여행", "사진"),
}


class Finding:
    def __init__(self, level: str, message: str) -> None:
        self.level = level
        self.message = message


def clean_text_len(text: str) -> int:
    text = re.sub(r"\[[^\]]+\]", "", text)
    text = re.sub(r"[#>*_`|\-:0-9\s]", "", text)
    return len(text)


def extract_meta_value(text: str, label: str) -> str:
    pattern = rf"▸\s*{re.escape(label)}[^\n]*\n(?P<value>.*?)(?=\n\s*▸|\n═|\Z)"
    match = re.search(pattern, text, re.S)
    if not match:
        return ""
    lines = [line.strip() for line in match.group("value").splitlines()]
    lines = [line for line in lines if line]
    return " ".join(lines).strip()


def split_body(text: str) -> tuple[str, str]:
    if "▼" not in text:
        return text, text
    meta, body = text.split("▼", 1)
    return meta, body.strip()


def parse_tags(tag_value: str) -> list[str]:
    tag_value = tag_value.replace("#", "")
    parts = re.split(r"[,，]", tag_value)
    return [part.strip() for part in parts if part.strip()]


def infer_min_chars(category: str) -> int:
    for key, value in CATEGORY_MIN_CHARS.items():
        if key in category:
            return value
    return 1200


def first_paragraph(body: str) -> str:
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if block and not block.startswith("[사진") and not block.startswith("##"):
            return block
    return ""


def bullet_count_after_heading(body: str, heading_words: tuple[str, ...]) -> int:
    lines = body.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.startswith("##") and any(word in line for word in heading_words):
            start = idx + 1
            break
    if start is None:
        return 0
    count = 0
    for line in lines[start:]:
        if line.startswith("##"):
            break
        if re.match(r"\s*[-*]\s+", line):
            count += 1
    return count


def validate(path: Path, keyword: str | None = None) -> int:
    text = path.read_text(encoding="utf-8")
    meta, body = split_body(text)
    findings: list[Finding] = []

    if "▼" not in text:
        findings.append(Finding("ERROR", "`▼` 구분자가 없습니다. 메타 박스와 본문을 분리하세요."))

    title = extract_meta_value(meta, "제목")
    category = extract_meta_value(meta, "카테고리")
    tags_value = extract_meta_value(meta, "태그")
    description = extract_meta_value(meta, "메타 디스크립션")

    for label, value in (
        ("제목", title),
        ("카테고리", category),
        ("태그", tags_value),
        ("메타 디스크립션", description),
    ):
        if not value:
            findings.append(Finding("ERROR", f"메타 정보의 `{label}` 값이 비어 있습니다."))

    if title:
        title_len = len(title)
        if title_len < 30 or title_len > 40:
            findings.append(Finding("WARN", f"제목 길이가 {title_len}자입니다. SEO 권장 범위는 30~40자입니다."))
        if re.search(r"충격|반전|절대|무조건|인생맛집|역대급", title):
            findings.append(Finding("WARN", "제목에 클릭베이트 또는 과장 표현이 있습니다."))

    tags = parse_tags(tags_value)
    if tags:
        if len(tags) > 12:
            findings.append(Finding("ERROR", f"태그가 {len(tags)}개입니다. 12개 이내로 줄이세요."))
        if not re.fullmatch(r"20\d{2}", tags[0]):
            findings.append(Finding("WARN", "첫 번째 태그는 작성 연도(예: 2026)를 권장합니다."))
        if len(tags) >= 2 and tags[1] in {"맛집", "여행", "카페", "IT", "리뷰"}:
            findings.append(Finding("WARN", "두 번째 태그는 가능한 카메라 태그를 권장합니다."))
        for key, required in CATEGORY_REQUIRED_TAGS.items():
            if key in category:
                missing = [tag for tag in required if tag not in tags]
                if missing:
                    findings.append(
                        Finding(
                            "WARN",
                            f"`{category}` 카테고리 필수 태그가 누락됐습니다: {', '.join(missing)} (guidelines/03_seo_checklist.md E 참고)",
                        )
                    )
                break

    if description:
        desc_len = len(description)
        if desc_len < 80 or desc_len > 160:
            findings.append(Finding("WARN", f"메타 디스크립션이 {desc_len}자입니다. 100~150자 안팎을 권장합니다."))

    if keyword:
        paragraph = first_paragraph(body)
        if keyword not in title:
            findings.append(Finding("WARN", f"메인 키워드 `{keyword}`가 제목에 없습니다."))
        if keyword not in paragraph:
            findings.append(Finding("WARN", f"메인 키워드 `{keyword}`가 첫 문단에 없습니다."))
        keyword_count = body.count(keyword)
        if keyword_count < 2:
            findings.append(Finding("WARN", f"본문의 메인 키워드 `{keyword}` 등장 횟수가 {keyword_count}회입니다."))

    if "— by Marco" not in body:
        findings.append(Finding("ERROR", "본문 마지막 시그니처 `— by Marco`가 없습니다."))
    else:
        non_empty_lines = [line.strip() for line in body.splitlines() if line.strip()]
        if non_empty_lines and non_empty_lines[-1] != "— by Marco":
            findings.append(Finding("WARN", "`— by Marco` 뒤에 다른 본문이 있습니다."))

    h2_count = len(re.findall(r"^##\s+", body, re.M))
    if h2_count < 2:
        findings.append(Finding("ERROR", f"H2 제목이 {h2_count}개입니다. 최소 2개 이상 필요합니다."))
    elif h2_count > 8:
        findings.append(Finding("WARN", f"H2 제목이 {h2_count}개입니다. 너무 잘게 쪼개졌는지 확인하세요."))

    image_lines = re.findall(r"^\[사진\s+\d+.*\]$", body, re.M)
    if not image_lines:
        findings.append(Finding("WARN", "사진 자리표시자가 없습니다. 이 블로그는 사진 리듬이 중요합니다."))
    for line in image_lines:
        if "alt:" not in line:
            findings.append(Finding("ERROR", f"alt 텍스트가 없는 사진 자리표시자: {line}"))

    concern_bullets = bullet_count_after_heading(body, ("아쉬웠던 점", "단점"))
    if concern_bullets == 0:
        findings.append(Finding("ERROR", "아쉬웠던 점 또는 단점 섹션에 bullet 항목이 없습니다."))
    if ("IT" in category or "제품" in category) and concern_bullets < 2:
        findings.append(Finding("WARN", "IT 리뷰는 단점 2개 이상을 권장합니다."))

    body_chars = clean_text_len(body)
    min_chars = infer_min_chars(category)
    if body_chars < min_chars:
        findings.append(Finding("WARN", f"본문 추정 글자 수가 {body_chars}자입니다. `{category or '기본'}` 최소 권장 {min_chars}자보다 짧습니다."))

    long_lines = [idx for idx, line in enumerate(body.splitlines(), 1) if len(line.strip()) > 120]
    if long_lines:
        sample = ", ".join(str(num) for num in long_lines[:5])
        findings.append(Finding("WARN", f"모바일에서 긴 줄이 있습니다: {sample}행. 문장을 나누는 것을 권장합니다."))

    if "확인 필요" in text or "확인필요" in text:
        findings.append(Finding("WARN", "`확인 필요` 항목이 남아 있습니다. 발행 전 확인하세요."))

    disclosure_terms = ("협찬", "제휴", "쿠팡", "파트너스", "유료광고")
    if any(term in text for term in disclosure_terms):
        if not re.search(r"유료광고|협찬|쿠팡 파트너스|수수료|제품을 제공", body):
            findings.append(Finding("ERROR", "협찬·제휴 관련 표현이 있지만 본문 고지가 명확하지 않습니다."))

    sensitive_terms = ("매출", "계약", "투자", "인사", "미공개", "직원 개인정보")
    if "스튜디오" in category and any(term in body for term in sensitive_terms):
        findings.append(Finding("WARN", "스튜디오 운영 글에 회사 민감정보 가능성이 있는 단어가 있습니다. 발행 전 재검토하세요."))

    errors = [finding for finding in findings if finding.level == "ERROR"]
    warnings = [finding for finding in findings if finding.level == "WARN"]

    print(f"검수 파일: {path}")
    print(f"제목: {title or '-'}")
    print(f"카테고리: {category or '-'}")
    print(f"태그 수: {len(tags)}")
    print(f"H2 수: {h2_count}")
    print(f"사진 자리표시자: {len(image_lines)}")
    print(f"본문 추정 글자 수: {body_chars}")
    print()

    if findings:
        for finding in findings:
            print(f"{finding.level}: {finding.message}")
    else:
        print("OK: 하네스 기준을 통과했습니다.")

    print()
    if errors:
        print(f"결과: FAIL ({len(errors)} error, {len(warnings)} warning)")
        return 1
    if warnings:
        print(f"결과: PASS WITH WARNINGS ({len(warnings)} warning)")
        return 0
    print("결과: PASS")
    return 0


def make_intake(date: str, count: int, output: Path | None) -> int:
    if not re.fullmatch(r"\d{8}", date):
        print("--date는 YYYYMMDD 형식이어야 합니다.", file=sys.stderr)
        return 2
    if count < 1 or count > 10:
        print("--count는 1~10 사이를 권장합니다.", file=sys.stderr)
        return 2

    if output is None:
        output = Path("drafts") / f"_weekend_intake_{date}.md"

    pretty_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
    sections = [
        f"# {pretty_date} 주말 글 작성 양식",
        "",
        "> 이번 주말 작성할 글 정보를 채워주세요.",
        "> 모르는 항목은 `확인 필요`로 두셔도 됩니다.",
        "> 다 채우면 Codex에게 \"양식 채웠어, 글 만들어줘\"라고 요청하세요.",
        "",
        "---",
        "",
    ]

    block = """## 글 {num}

- 카테고리:
- 장소·상호 또는 제품명:
- 정확 위치 또는 제품 모델:
- 방문일·사용 기간 + 시간대:
- 동행 또는 사용 맥락:
- 시킨 것·구매가·가격 (한 줄에 하나):
- 좋았던 점 1~3:
- 아쉬웠던 점 1~2 (필수):
- 재방문·재구매 의사 ★/5 + 한 줄:
- 사진 폴더 경로 또는 첨부:
- 협찬·제휴 여부:
- 꼭 넣고 싶은 개인 메모:

---

"""
    for num in range(1, count + 1):
        sections.append(block.format(num=num))

    sections.append("""## 발행 예약 슬롯 메모

(월 09:00 / 화 18:00 / 목 09:00 / 금 18:00 중 어느 슬롯에 어느 글을 배치할지)

- 슬롯 1:
- 슬롯 2:
- 슬롯 3:
""")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(sections), encoding="utf-8")
    print(f"입력 양식 생성 완료: {output}")
    return 0


def print_slots(from_date: str, count: int) -> int:
    try:
        day = dt.date.fromisoformat(from_date)
    except ValueError:
        print("--from은 YYYY-MM-DD 형식이어야 합니다.", file=sys.stderr)
        return 2

    if count < 1 or count > 60:
        print("--count는 1~60 사이를 권장합니다.", file=sys.stderr)
        return 2

    printed = 0
    cursor = day
    while printed < count:
        if cursor.weekday() in SLOTS:
            print(f"{cursor.isoformat()} {SLOTS[cursor.weekday()]}")
            printed += 1
        cursor += dt.timedelta(days=1)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Marco's Tistory Blog Codex harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate a _FOR_TISTORY.md file")
    validate_parser.add_argument("path", type=Path)
    validate_parser.add_argument("--keyword", help="Main keyword to check in title and first paragraph")

    intake_parser = subparsers.add_parser("intake", help="Create a weekend intake template")
    intake_parser.add_argument("--date", required=True, help="YYYYMMDD")
    intake_parser.add_argument("--count", type=int, default=5)
    intake_parser.add_argument("--output", type=Path)

    slots_parser = subparsers.add_parser("slots", help="Print publishing slots")
    slots_parser.add_argument("--from", dest="from_date", required=True, help="YYYY-MM-DD")
    slots_parser.add_argument("--count", type=int, default=8)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        if not args.path.exists():
            print(f"파일을 찾을 수 없습니다: {args.path}", file=sys.stderr)
            return 2
        return validate(args.path, args.keyword)
    if args.command == "intake":
        return make_intake(args.date, args.count, args.output)
    if args.command == "slots":
        return print_slots(args.from_date, args.count)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
