# Marco's Tistory Blog Harness

티스토리 블로그 [marcoaeolus.tistory.com](https://marcoaeolus.tistory.com/) 운영을 위한 작업 환경(harness)입니다.
글을 새로 쓰거나 카테고리를 확장할 때 이 폴더의 가이드·템플릿·체크리스트를 따라가면 일관된 품질로 발행할 수 있도록 설계했습니다.

## 운영 컨셉 한 줄 요약

라이프스타일(여행·맛집·카페·사진) 중심에 게임/스튜디오 운영 인사이트를 더한 채널을 운영하며, 본업에 부담을 주지 않는 **주 2~3회** 페이스로 **검색 유입 + 애드센스/제휴 수익**을 만든다.

## 폴더 구조

```
블로그 티스토리/
├── README.md                       # 이 문서 (전체 지도)
├── CLAUDE.md                       # AI 어시스턴트가 항상 참고할 핵심 컨텍스트
├── AGENTS.md                       # Codex가 항상 참고할 운영 규칙
│
├── specs/
│   └── blog_profile.md             # 블로그 프로필·타겟·카테고리·KPI
│
├── guidelines/                     # "어떻게 쓸 것인가"
│   ├── 01_tone_and_manner.md       # 톤앤매너, 문체, 1인칭/2인칭 등
│   ├── 02_post_structure.md        # 포스트 표준 구조 (서론·본론·결론)
│   ├── 03_seo_checklist.md         # 제목·메타·키워드·내부링크 SEO 룰
│   └── 04_monetization_and_image.md# 애드센스·제휴·이미지·저작권 정책
│
├── templates/                      # 카테고리별 글 템플릿 (.md)
│   ├── travel_post.md              # 여행기
│   ├── food_post.md                # 맛집 리뷰
│   ├── cafe_dessert_post.md        # 카페·디저트
│   ├── it_review_post.md           # IT 제품 리뷰
│   └── photo_essay.md              # 사진/일상 에세이
│
├── workflow/
│   ├── publishing_checklist.md     # 기획→발행→사후점검 체크리스트
│   ├── weekend_routine.md          # 주말 일괄 작성 루틴
│   └── codex_harness.md            # Codex 자동화 사용법
│
├── scripts/
│   └── tistory_harness.py          # 입력 양식 생성·예약 슬롯 출력·발행용 글 검수
│
└── calendar/
    ├── content_calendar.md         # 월별/주별 발행 일정
    └── idea_bank.md                # 주제 아이디어 풀
```

## 새 글을 쓸 때 따라가는 순서

1. `calendar/idea_bank.md`에서 다음에 쓸 주제를 고른다.
2. `specs/blog_profile.md`에서 카테고리·타겟·키워드를 재확인한다.
3. `templates/`에서 해당 카테고리의 템플릿을 복사해 초안 파일을 만든다.
4. `guidelines/01_tone_and_manner.md` → `02_post_structure.md` 순서로 따라가며 본문을 채운다.
5. `guidelines/03_seo_checklist.md`로 제목·태그·메타 점검.
6. `workflow/publishing_checklist.md`의 발행 전·발행 후 항목을 모두 통과시킨다.
7. 발행 후 `calendar/content_calendar.md`에 결과(URL·키워드·초기 반응) 기록.

## 하네스 갱신 원칙

- **가이드라인은 분기마다 점검**: 트래픽 데이터로 SEO·톤 가이드를 갱신.
- **템플릿은 월 1회 점검**: 잘 된 글의 구조를 거꾸로 템플릿에 반영.
- **idea_bank는 상시 추가**: 떠오를 때마다 한 줄씩 던져두기.
- **Codex 검수 규칙은 누락이 반복될 때 추가**: `scripts/tistory_harness.py`에 체크를 늘리고 `workflow/codex_harness.md`에 사용법을 반영.
