# 블로그 하네스 Git 관리 가이드

이 폴더(`블로그 티스토리/`)는 2026-08-13에 로컬 git 저장소로 초기화됐고, 2026-09-13에 GitHub(`github.com/marcoaeolus/Marco`)와 SSH로 연결까지 끝났습니다. 이 문서는 앞으로 이 폴더를 git으로 관리할 때 쓰는 명령어와 주의사항을 정리한 것입니다.

## 기본 정보

- 원격 저장소: `github.com/marcoaeolus/Marco` (SSH 방식, `git@github.com:marcoaeolus/Marco.git`)
- 커밋 작성자: **반드시 `Marco <marcoaeolus@gmail.com>`** — 회사 계정(mjbak@nanali.net)이 아님. 이 폴더 안에서는 로컬 git config로 이미 고정되어 있어서 신경 안 써도 자동으로 이 이름으로 커밋됩니다.
- 로컬 브랜치명: `master` (GitHub 기본값인 `main`과 다름 — 당장 문제는 없고, 나중에 원하면 GitHub 웹 UI에서 이름만 바꿀 수 있음)
- 인증: SSH 키 등록 완료, passphrase 없는 키라 `git push`할 때 아무것도 안 물어보고 바로 됩니다.
- `.gitignore`에 `_to_delete/`와 `.DS_Store`는 제외되어 있어서, drafts 정리하다 생기는 임시 폴더는 git이 신경 안 씁니다.

## 평소에 쓰는 명령어 (이 4개면 충분)

터미널에서 이 폴더로 이동한 다음:

```
cd "/Users/marco/Documents/Claude/Projects/블로그 티스토리"
```

**1. 지금 뭐가 바뀌었는지 확인**
```
git status
```
빨간색으로 나오는 파일들이 "수정했지만 아직 커밋 안 한 것"들입니다.

**2. 바뀐 내용을 스냅샷으로 저장 (커밋)**
```
git add .
git commit -m "여기에 무슨 작업인지 한 줄로"
```
커밋 메시지는 거창할 필요 없이 "도쿄편 9편 발행", "카테고리 태그 규칙 수정"처럼 무슨 변화인지만 알아볼 수 있으면 충분합니다.

**3. GitHub에 올리기**
```
git push
```
이거 한 번이면 로컬에서 만든 커밋들이 전부 GitHub 저장소에 반영됩니다.

**4. 지금까지 커밋 기록 보기 (가끔 확인용)**
```
git log --oneline -10
```

### 하루 작업 흐름 예시

새 글 초안을 쓰거나 발행 상태를 캘린더에 반영했다면:

```
cd "/Users/marco/Documents/Claude/Projects/블로그 티스토리"
git add .
git commit -m "9/15 도쿄 2일차편 발행, 캘린더 상태 갱신"
git push
```

이 세 줄만 반복하면 됩니다. `add` → `commit` → `push` 순서는 항상 동일해요.

## 자주 나올 수 있는 상황

**"nothing to commit, working tree clean"이 뜬다** — 정상입니다. 아무것도 안 바뀌었다는 뜻이라 그냥 넘어가면 됩니다.

**`git push`가 아무것도 안 물어보고 바로 끝난다** — 정상입니다. SSH 키라 그렇습니다. 혹시 만에 하나 다시 `Username for 'https://github.com'` 같은 걸 물어보면, origin 주소가 다시 https로 바뀐 것이니 아래 명령어로 되돌리면 됩니다.
```
git remote set-url origin git@github.com:marcoaeolus/Marco.git
```

**`fatal: Unable to create '.../index.lock': File exists` 에러가 뜬다** — 이전 git 명령이 비정상 종료됐을 때 생기는 잠금 파일 문제입니다. 아래처럼 지우고 다시 시도하면 됩니다.
```
rm -f .git/index.lock
```
(만약 삭제 권한 에러가 나면, `mv .git/index.lock .git/index.lock.bak`처럼 이름만 바꿔서 치워도 됩니다.)

## 이 파일 자체도 git에 포함됨

이 가이드 파일도 저장소 안에 있는 일반 파일이라, 수정하고 싶으면 그냥 고친 다음 위 3줄(add·commit·push)을 실행하면 됩니다.
