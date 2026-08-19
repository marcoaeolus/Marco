# Codex 자동화 하네스

Codex에서 Marco's Tistory Blog 작업을 이어갈 때 사용하는 실행 가이드입니다.
`AGENTS.md`는 기본 행동 규칙이고, 이 문서는 실제 명령과 작업 흐름을 정리합니다.

## 1. 하네스가 맡는 일

| 요청 | Codex 처리 |
|---|---|
| 글감 추천 | `idea_bank.md`와 `content_calendar.md`를 보고 카테고리 균형 기준으로 제안 |
| 주말 일괄 작성 | 입력 양식 생성 → 3~7편 초안 작성 → 예약 슬롯 제안 |
| 맛집·카페·여행·IT 리뷰 작성 | 카테고리 템플릿 기반 초안 + `_FOR_TISTORY.md` 생성 |
| 발행 전 검수 | SEO, 태그, 사진 alt, 단점, 협찬 고지, 시그니처 검사 |
| 발행 후 기록 | `content_calendar.md` 결과 로그 업데이트 |

Codex는 티스토리에 직접 로그인하거나 발행하지 않습니다. 최종 발행은 사용자가 티스토리 화면에서 복붙·사진 업로드·메타 입력으로 처리합니다.

## 2. 파일 역할

| 파일/폴더 | 역할 |
|---|---|
| `AGENTS.md` | Codex 기본 행동 규칙 |
| `CLAUDE.md` | 기존 Claude 컨텍스트. Codex도 참고 가능 |
| `specs/blog_profile.md` | 블로그 정체성, 타겟, KPI |
| `guidelines/` | 톤, 구조, SEO, 수익화·이미지 정책 |
| `templates/` | 카테고리별 글 템플릿 |
| `workflow/weekend_routine.md` | 주말 일괄 작성 루틴 |
| `workflow/publishing_checklist.md` | 발행 전후 체크리스트 |
| `calendar/idea_bank.md` | 글감 저장소 |
| `calendar/content_calendar.md` | 예약·발행·성과 기록 |
| `scripts/tistory_harness.py` | 입력 양식 생성, 예약 슬롯 출력, 발행용 글 검수 |

## 3. 자주 쓰는 명령

### 발행용 파일 검수

```bash
python3 scripts/tistory_harness.py validate drafts/20260509_food_konkuk_goheungsoondae_FOR_TISTORY.md
```

선택적으로 메인 키워드를 명시할 수 있습니다.

```bash
python3 scripts/tistory_harness.py validate drafts/파일_FOR_TISTORY.md --keyword "건대 순대국 맛집"
```

### 주말 입력 양식 생성

```bash
python3 scripts/tistory_harness.py intake --date 20260509 --count 5
```

기본 출력 위치는 `drafts/_weekend_intake_YYYYMMDD.md`입니다.

### 예약 발행 슬롯 확인

```bash
python3 scripts/tistory_harness.py slots --from 2026-05-09 --count 8
```

예약 슬롯은 월 09:00, 화 18:00, 목 09:00, 금 18:00을 기준으로 출력합니다.

## 4. 새 글 작성 요청 처리

사용자가 "이 정보로 글 만들어줘"라고 하면 Codex는 다음 순서로 작업합니다.

1. `AGENTS.md`의 필수 참조 문서를 읽습니다.
2. 카테고리를 판별하고 해당 템플릿을 엽니다.
3. 사실 정보와 감상 정보를 분리합니다.
4. 누락된 가격, 영업시간, 주소, 스펙은 `확인 필요`로 표시합니다.
5. `drafts/YYYYMMDD_카테고리_영문슬러그.md`를 작성합니다.
6. 같은 내용에서 티스토리용 메타 박스와 본문만 추린 `_FOR_TISTORY.md`를 작성합니다.
7. `scripts/tistory_harness.py validate`를 실행합니다.
8. 오류가 있으면 수정하고, 경고는 사용자에게 남은 확인 항목으로 보고합니다.

## 5. `_FOR_TISTORY.md` 작성 기준

- 상단에는 티스토리 화면에 직접 입력할 메타 정보만 둡니다.
- `▼` 아래는 그대로 티스토리 마크다운 모드에 붙여넣을 본문입니다.
- 사진 업로드는 수기 작업으로 남기고, 본문에는 `[사진 N — 설명 / alt: ...]` 형식의 자리표시자를 둡니다.
- 본문에는 초안 메모나 발행 체크리스트를 남기지 않습니다.
- 마지막 줄은 항상 `— by Marco`입니다.

## 6. 검수 결과 해석

- `ERROR`: 발행용 파일로 쓰기 전에 수정해야 합니다.
- `WARN`: 발행은 가능하지만 사용자가 확인하면 좋은 항목입니다.
- `OK`: 하네스 기준 통과입니다.

검수 스크립트는 편집자를 대체하지 않습니다. 가격, 영업시간, 휴무일, 제품 스펙처럼 변동 가능한 정보는 최종 발행 전 한 번 더 사람이 확인합니다.

## 7. 사용자에게 보고할 때

완료 보고는 짧게 합니다.

- 생성한 파일 경로
- 검수 결과
- 남은 `확인 필요` 항목
- 티스토리에서 사용자가 직접 해야 할 작업: 본문 복붙, 사진 업로드, 태그·메타 입력, 예약 발행

## 8. 업데이트 원칙

- 잘 된 발행본이 나오면 `guidelines/02_post_structure.md` 또는 해당 템플릿에 패턴을 반영합니다.
- 반복되는 누락이 생기면 `scripts/tistory_harness.py`의 검수 규칙을 추가합니다.
- 하네스 변경 시 `AGENTS.md`와 이 문서의 날짜를 함께 갱신합니다.
