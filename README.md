# 🧠 심리테스트 자동화 시스템 — 설치 가이드

> **버튼 한 번으로** 유행 심리테스트 검색 → Google Sheets 기록 → HTML 생성 → GitHub Pages 발행

---

## 📁 파일 구조

```
your-repo/
├── .github/
│   └── workflows/
│       └── psychology-test.yml   ← GitHub Actions 워크플로우
├── scripts/
│   └── generate.py               ← 자동화 핵심 스크립트
├── docs/                         ← 자동 생성되는 폴더 (GitHub Pages)
│   ├── index.html
│   └── 2025-01-01-테스트이름.html
└── README.md
```

---

## 🚀 설치 방법 (5단계)

### 1단계. GitHub 저장소 만들기

1. GitHub에서 새 저장소 생성
2. 위 파일들을 업로드 (or git push)
3. **Settings → Pages → Source: `gh-pages` 브랜치** 선택

---

### 2단계. Serper API 키 받기 (무료 검색)

1. [serper.dev](https://serper.dev) 가입
2. 무료 플랜: **월 2,500회 무료**
3. Dashboard에서 API Key 복사

---

### 3단계. Google Sheets 연동

#### 3-1. 스프레드시트 만들기
1. Google Sheets에서 새 시트 생성
2. URL에서 ID 복사: `https://docs.google.com/spreadsheets/d/`**`여기가ID`**`/edit`
3. 첫 행에 헤더 입력:
   ```
   A: 날짜 | B: 테스트이름 | C: 설명 | D: 질문수 | E: 결과유형수 | F: 출처URL | G: 상태
   ```

#### 3-2. 서비스 계정 만들기
1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성
3. **API 및 서비스 → 라이브러리 → Google Sheets API 활성화**
4. **사용자 인증 정보 → 서비스 계정 만들기**
5. 키 생성 → JSON 다운로드
6. 해당 서비스 계정 이메일을 Sheets에 **편집자 권한**으로 공유

---

### 4단계. GitHub Secrets 등록

저장소 → **Settings → Secrets and variables → Actions → New repository secret**

| Secret 이름 | 값 |
|-------------|-----|
| `SERPER_API_KEY` | Serper에서 복사한 API Key |
| `GOOGLE_SHEETS_ID` | Sheets URL에서 복사한 ID |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | 다운로드한 JSON 파일 전체 내용 붙여넣기 |

---

### 5단계. 실행하기 🎉

1. GitHub 저장소 → **Actions 탭**
2. 왼쪽에서 **"🧠 심리테스트 자동 발행"** 클릭
3. **"Run workflow"** 버튼 클릭
4. 주제 입력 (예: `MBTI`, `연애유형`, `직장스타일`) 또는 빈칸으로 자동 검색
5. 약 1~2분 후 완료!

**발행 URL:** `https://[유저명].github.io/[저장소명]/`

---

## 💡 자주 쓰는 주제 예시

| 주제 입력 | 생성되는 테스트 |
|----------|---------------|
| `MBTI` | MBTI 기반 성격 유형 |
| `연애유형` | 나의 연애 스타일 |
| `직장스타일` | 직장에서 나는 어떤 타입? |
| `감성유형` | 당신의 감성 코드는? |
| (빈칸) | 자동으로 유행 테스트 검색 |

---

## 🔧 커스터마이징

### 질문/결과 수정
`scripts/generate.py` 파일에서:
- `generate_questions()` 함수 → 질문 내용 변경
- `generate_results()` 함수 → 결과 유형 변경

### 디자인 변경
`generate_html()` 함수 안의 CSS `<style>` 섹션에서:
- `--accent` 색상 변경
- 폰트 변경

---

## ❓ 문제 해결

| 증상 | 해결 |
|------|------|
| Actions 실패 | Secrets 이름 오타 확인 |
| Sheets 기록 안 됨 | 서비스 계정 이메일 공유 확인 |
| 페이지 안 보임 | Settings → Pages에서 gh-pages 브랜치 선택 확인 |
| 검색 결과 없음 | SERPER_API_KEY 만료 → serper.dev에서 확인 |
