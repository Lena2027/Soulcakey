#!/usr/bin/env python3
"""
SOULCAKEY 심리테스트 자동화 스크립트
─────────────────────────────────────
1. Serper API로 유행 심리테스트 검색
2. Claude API로 테스트 콘텐츠 생성 (tests/*.js 포맷)
3. Google Sheets에 날짜/이름/내용 기록
4. index.html에 새 테스트 <script> 태그 자동 삽입
"""

import os, json, re, sys, random
import requests
from datetime import datetime

# ── 환경변수 ──────────────────────────────────────────
SERPER_API_KEY    = os.environ.get("SERPER_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
SHEETS_ID         = os.environ.get("GOOGLE_SHEETS_ID", "")
SERVICE_ACCOUNT   = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
TOPIC             = os.environ.get("TOPIC", "자동 검색")
TODAY             = datetime.now().strftime("%Y-%m-%d")
TIMESTAMP         = datetime.now().strftime("%Y%m%d%H%M%S")
SITE_DIR          = "mindpop"
TESTS_DIR         = f"{SITE_DIR}/tests"


# ══════════════════════════════════════════════════════
# STEP 1. 유행 심리테스트 주제 검색
# ══════════════════════════════════════════════════════
def search_trending_topic() -> str:
    if TOPIC != "자동 검색":
        print(f"📌 지정 주제: {TOPIC}")
        return TOPIC

    if not SERPER_API_KEY:
        print("⚠️  SERPER_API_KEY 없음. 기본 주제 사용.")
        return "나는 어떤 음식 같은 사람일까?"

    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": "요즘 유행하는 심리테스트 2025", "gl": "kr", "hl": "ko", "num": 5}

    try:
        res = requests.post("https://google.serper.dev/search",
                            headers=headers, json=payload, timeout=10)
        res.raise_for_status()
        results = res.json().get("organic", [])
        if results:
            titles = [r.get("title", "") for r in results[:3]]
            print(f"🔍 검색 결과: {titles[0]}")
            return extract_topic(titles)
    except Exception as e:
        print(f"⚠️  검색 실패: {e}")

    return "나는 어떤 계절 같은 사람일까?"


def extract_topic(titles: list) -> str:
    keywords = ["MBTI", "연애", "직장", "성격", "음식", "동물", "캐릭터", "감성", "스타일"]
    for title in titles:
        for kw in keywords:
            if kw in title:
                return f"{kw} 유형 심리테스트"
    return titles[0][:30] if titles else "나는 어떤 유형일까?"


# ══════════════════════════════════════════════════════
# STEP 2. 테스트 데이터 생성
# ══════════════════════════════════════════════════════
def generate_test_data(topic: str) -> dict:
    if ANTHROPIC_API_KEY:
        return generate_with_claude(topic)
    print("⚠️  ANTHROPIC_API_KEY 없음. 내장 템플릿 사용.")
    return build_fallback_test()


def generate_with_claude(topic: str) -> dict:
    prompt = f"""당신은 SOULCAKEY 심리테스트 사이트의 콘텐츠 작가입니다.
주제: "{topic}"

아래 JSON 형식에 맞게 심리테스트를 만들어주세요.
반드시 유효한 JSON만 출력하고, 코드블록이나 설명 없이 순수 JSON만 출력하세요.

{{
  "id": "영어소문자만_언더바허용 (예: season, my_food)",
  "title": "카드에 보여줄 짧은 제목 (30자 이하)",
  "heroTitle": "히어로 배너 제목 HTML (br 사용, 2줄)",
  "heroSub": "히어로 부제목 HTML (br 사용)",
  "emoji": "대표 이모지 1개",
  "thumbColor": 1에서 8 사이 숫자,
  "badge": "NEW",
  "categories": ["카테고리1"],
  "participantsLabel": "🔥 1.5만명",
  "estimatedMinutes": 2,
  "questions": [
    {{
      "emoji": "이모지",
      "text": "질문 내용",
      "answers": [
        {{ "text": "답변1", "scores": {{ "결과id1": 3, "결과id2": 1 }} }},
        {{ "text": "답변2", "scores": {{ "결과id2": 3, "결과id3": 1 }} }},
        {{ "text": "답변3", "scores": {{ "결과id3": 3, "결과id4": 1 }} }},
        {{ "text": "답변4", "scores": {{ "결과id4": 3, "결과id1": 1 }} }}
      ]
    }}
  ],
  "results": [
    {{
      "id": "결과id1",
      "emoji": "이모지",
      "title": "당신은 <em>'강조<br>강조2'</em> 같은 사람!",
      "desc": "3~4문장 결과 설명",
      "chemistry": {{
        "good": {{ "emoji": "이모지", "name": "잘 맞는 유형" }},
        "bad":  {{ "emoji": "이모지", "name": "안 맞는 유형" }}
      }}
    }}
  ]
}}

조건:
- questions는 정확히 5개
- results는 정확히 4개
- 카테고리는 다음 중 선택: 연애, 성격, 회사생활, B급감성, MBTI, 음식
- 재미있고 공감 가는 한국어 콘텐츠로 작성
- 반드시 완전한 JSON만 출력하고 중간에 주석(//)을 절대 넣지 마세요
- 모든 문자열에서 작은따옴표 대신 큰따옴표만 사용하세요"""

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-haiku-4-5",
        "max_tokens": 3000,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        res = requests.post("https://api.anthropic.com/v1/messages",
                            headers=headers, json=payload, timeout=30)
        res.raise_for_status()
        text = res.json()["content"][0]["text"].strip()
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        text = re.sub(r'//.*?\n', '\n', text)  # 주석 제거
        data = json.loads(text)
        data["thumbColor"] = random.randint(1, 8)  # ← 이 줄 추가
        print(f"✅ Claude API 생성 완료: {data.get('title')}")
        return data
    except Exception as e:
        print(f"⚠️  Claude API 실패: {e}. 내장 템플릿 사용.")
        return build_fallback_test()


def build_fallback_test() -> dict:
    """API 없이 사용하는 기본 내장 테스트"""
    return {
        "id": f"test_{TIMESTAMP}",
        "title": "당신은 어떤 계절 같은 사람인가요?",
        "heroTitle": "당신은 어떤<br>계절 같은 사람인가요?",
        "heroSub": "5가지 질문으로 알아보는<br>나의 숨겨진 계절 성격",
        "emoji": "🌸",
        "thumbColor": 3,
        "badge": "NEW",
        "categories": ["성격", "연애"],
        "participantsLabel": "🔥 2.1만명",
        "estimatedMinutes": 2,
        "questions": [
            {
                "emoji": "🌤️",
                "text": "아침에 눈을 떴을 때 기분이 가장 좋은 날씨는?",
                "answers": [
                    {"text": "화창하고 맑은 날. 에너지 충전!",      "scores": {"summer": 3, "spring": 1}},
                    {"text": "선선하고 바람 부는 날. 산책하기 딱!", "scores": {"autumn": 3, "winter": 1}},
                    {"text": "포근하고 따뜻한 봄날 같은 날씨.",     "scores": {"spring": 3, "summer": 1}},
                    {"text": "눈 오거나 흐린 날. 집에 있기 좋아.", "scores": {"winter": 3, "autumn": 1}},
                ]
            },
            {
                "emoji": "💬",
                "text": "친구가 갑자기 고민을 털어놓을 때 나의 반응은?",
                "answers": [
                    {"text": "해결책을 바로 제시해준다.",             "scores": {"summer": 2, "autumn": 2}},
                    {"text": "일단 다 들어주고 공감한다.",            "scores": {"spring": 3, "winter": 1}},
                    {"text": "같이 맛있는 거 먹으러 가자고 한다.",   "scores": {"summer": 3, "spring": 1}},
                    {"text": "조용히 옆에 있어준다.",                 "scores": {"winter": 3, "autumn": 1}},
                ]
            },
            {
                "emoji": "🏖️",
                "text": "갑자기 3일 휴가가 생겼다! 나의 선택은?",
                "answers": [
                    {"text": "친구들 불러 신나는 여행 계획!",        "scores": {"summer": 3, "spring": 1}},
                    {"text": "혼자 조용한 카페나 독서 삼매경.",       "scores": {"winter": 3, "autumn": 1}},
                    {"text": "평소 가고 싶던 감성 장소 탐방.",        "scores": {"autumn": 2, "spring": 2}},
                    {"text": "그냥 집에서 푹 쉰다. 이게 최고.",      "scores": {"winter": 2, "autumn": 2}},
                ]
            },
            {
                "emoji": "💌",
                "text": "썸 타는 상대에게 먼저 연락할 때 나는?",
                "answers": [
                    {"text": "생각나면 바로 연락. 솔직한 게 최고.", "scores": {"summer": 3, "spring": 1}},
                    {"text": "빌미를 만들어서 자연스럽게 연락.",     "scores": {"spring": 2, "autumn": 2}},
                    {"text": "상대방이 먼저 연락하길 기다린다.",     "scores": {"winter": 3, "autumn": 1}},
                    {"text": "친구들한테 물어보고 신중하게.",         "scores": {"autumn": 3, "winter": 1}},
                ]
            },
            {
                "emoji": "😤",
                "text": "스트레스를 받았을 때 나의 해소법은?",
                "answers": [
                    {"text": "친구들과 신나게 놀며 발산!",            "scores": {"summer": 3, "spring": 1}},
                    {"text": "혼자 산책하거나 드라이브.",              "scores": {"autumn": 3, "winter": 1}},
                    {"text": "맛있는 걸 잔뜩 먹는다.",                "scores": {"spring": 3, "summer": 1}},
                    {"text": "집에서 조용히 혼자만의 시간.",           "scores": {"winter": 3, "autumn": 1}},
                ]
            },
        ],
        "results": [
            {
                "id": "spring",
                "emoji": "🌸",
                "title": "당신은 <em>'설레고 따뜻한<br>봄'</em> 같은 사람!",
                "desc": "주변 사람들에게 따뜻한 온기를 전하는 사람이에요. 새로운 시작을 두려워하지 않고, 작은 것에서 행복을 찾는 능력이 있어요. 가끔 감수성이 넘쳐 쉽게 감동받지만, 그게 당신의 가장 큰 매력이에요. 🌷",
                "chemistry": {
                    "good": {"emoji": "☀️", "name": "활기찬 여름"},
                    "bad":  {"emoji": "❄️", "name": "차가운 겨울"}
                }
            },
            {
                "id": "summer",
                "emoji": "☀️",
                "title": "당신은 <em>'뜨겁고 에너지 넘치는<br>여름'</em> 같은 사람!",
                "desc": "어딜 가나 분위기를 밝히는 에너지의 소유자예요. 목표를 향해 거침없이 나아가고, 함께 있으면 지루할 틈이 없어요. 가끔 너무 강렬해서 상대방이 지칠 수도 있지만, 그 열정이 당신의 무기예요. 🔥",
                "chemistry": {
                    "good": {"emoji": "🍂", "name": "차분한 가을"},
                    "bad":  {"emoji": "🌸", "name": "섬세한 봄"}
                }
            },
            {
                "id": "autumn",
                "emoji": "🍂",
                "title": "당신은 <em>'깊고 감성적인<br>가을'</em> 같은 사람!",
                "desc": "생각이 깊고 감성이 풍부한 사람이에요. 겉으로는 차분해 보이지만 내면에는 풍부한 감정이 숨어있어요. 신중하게 행동하고 한번 맺은 인연을 소중히 여기는 타입이에요. 🎑",
                "chemistry": {
                    "good": {"emoji": "☀️", "name": "활기찬 여름"},
                    "bad":  {"emoji": "🌸", "name": "감성적인 봄"}
                }
            },
            {
                "id": "winter",
                "emoji": "❄️",
                "title": "당신은 <em>'고요하고 신비로운<br>겨울'</em> 같은 사람!",
                "desc": "조용하지만 존재감 있는 독특한 매력의 소유자예요. 혼자만의 시간을 소중히 여기고, 깊이 있는 대화를 좋아해요. 처음엔 차갑게 보일 수 있지만, 알고 보면 따뜻한 내면이 있어요. 🌟",
                "chemistry": {
                    "good": {"emoji": "🍂", "name": "감성적인 가을"},
                    "bad":  {"emoji": "☀️", "name": "활기찬 여름"}
                }
            },
        ]
    }


# ══════════════════════════════════════════════════════
# STEP 3. tests/*.js 파일 저장
# ══════════════════════════════════════════════════════
def save_test_js(data: dict) -> str:
    os.makedirs(TESTS_DIR, exist_ok=True)
    test_id  = data["id"]
    filename = f"{test_id}.js"
    filepath = os.path.join(TESTS_DIR, filename)

    js = f"""/* =============================================
   SOULCAKEY — tests/{filename}
   자동 생성: {TODAY}  |  주제: {data['title']}
   ============================================= */

TESTS['{test_id}'] = {json.dumps(data, ensure_ascii=False, indent=2)};
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(js)
    print(f"✅ 테스트 파일 생성: {filepath}")
    return filename


# ══════════════════════════════════════════════════════
# STEP 4. index.html <script> 태그 삽입
# ══════════════════════════════════════════════════════
def inject_script_tag(filename: str):
    index_path = os.path.join(SITE_DIR, "index.html")
    if not os.path.exists(index_path):
        print(f"⚠️  {index_path} 없음. 건너뜀.")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_tag = f'<script src="tests/{filename}"></script>'
    if new_tag in content:
        print(f"ℹ️  이미 등록됨: {filename}")
        return

    marker = "<!-- 새 테스트 추가 시 여기에 한 줄 추가 -->"
    if marker in content:
        updated = content.replace(marker, f"{new_tag}\n{marker}")
    else:
        updated = content.replace(
            '<script src="js/engine.js">',
            f'{new_tag}\n<script src="js/engine.js">'
        )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"✅ index.html 업데이트 완료")


# ══════════════════════════════════════════════════════
# STEP 5. Google Sheets 기록
# ══════════════════════════════════════════════════════
def update_google_sheets(data: dict):
    if not SHEETS_ID or not SERVICE_ACCOUNT:
        print("⚠️  Google Sheets 설정 없음. 건너뜀.")
        return

    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build

        creds = Credentials.from_service_account_info(
            json.loads(SERVICE_ACCOUNT),
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        service = build("sheets", "v4", credentials=creds)

        row = [
            TODAY,
            data["id"],
            data["title"],
            ", ".join(data.get("categories", [])),
            len(data.get("questions", [])),
            len(data.get("results", [])),
            data.get("badge", ""),
            "발행완료"
        ]
        # 헤더가 없으면 첫 행에 헤더 추가
        existing = service.spreadsheets().values().get(
            spreadsheetId=SHEETS_ID, range="SOULCAKEY 발행기록!A1:A1"
        ).execute()
        if not existing.get("values"):
            header = [["날짜", "테스트ID", "제목", "카테고리", "질문수", "결과수", "뱃지", "상태"]]
            service.spreadsheets().values().update(
                spreadsheetId=SHEETS_ID, range="SOULCAKEY 발행기록!A1",
                valueInputOption="USER_ENTERED", body={"values": header}
            ).execute()

        service.spreadsheets().values().append(
            spreadsheetId=SHEETS_ID, range="SOULCAKEY 발행기록!A:H",
            valueInputOption="USER_ENTERED", body={"values": [row]}
        ).execute()

        print(f"✅ Google Sheets 기록 완료")
    except Exception as e:
        print(f"⚠️  Sheets 실패: {e}")


# ══════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"\n🚀 SOULCAKEY 자동화 시작 | {TODAY}\n{'─'*40}")

    topic     = search_trending_topic()
    test_data = generate_test_data(topic)
    print(f"📋 테스트 제목: {test_data['title']}")

    filename = save_test_js(test_data)
    inject_script_tag(filename)
    update_google_sheets(test_data)

    print(f"\n🎉 완료! '{test_data['title']}' 발행 준비됨")
