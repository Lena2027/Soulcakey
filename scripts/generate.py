#!/usr/bin/env python3
"""SOULCAKEY 심리테스트 자동화 스크립트"""

import os, json, re, random
import requests
from datetime import datetime

SERPER_API_KEY    = os.environ.get("SERPER_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
SHEETS_ID         = os.environ.get("GOOGLE_SHEETS_ID", "")
SERVICE_ACCOUNT   = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
TOPIC             = os.environ.get("TOPIC", "자동 검색")
TODAY             = datetime.now().strftime("%Y-%m-%d")
TIMESTAMP         = datetime.now().strftime("%Y%m%d%H%M%S")
SITE_DIR          = "mindpop"
TESTS_DIR         = f"{SITE_DIR}/tests"
SHEET_NAME        = "SOULCAKEY 발행기록"


# ══════════════════════════════════════════════════════
# STEP 1. 주제 검색
# ══════════════════════════════════════════════════════
def get_topic() -> str:
    if TOPIC != "자동 검색":
        print(f"📌 지정 주제: {TOPIC}")
        return TOPIC

    if not SERPER_API_KEY:
        return "나는 어떤 음식 같은 사람일까?"

    try:
        res = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": "요즘 유행하는 심리테스트 2025", "gl": "kr", "hl": "ko", "num": 5},
            timeout=10
        )
        results = res.json().get("organic", [])
        if results:
            titles = [r.get("title", "") for r in results[:3]]
            print(f"🔍 검색: {titles[0]}")
            for title in titles:
                for kw in ["MBTI", "연애", "직장", "성격", "음식", "동물", "감성"]:
                    if kw in title:
                        return f"{kw} 유형 심리테스트"
            return titles[0][:30]
    except Exception as e:
        print(f"⚠️  검색 실패: {e}")

    return "나는 어떤 유형일까?"


# ══════════════════════════════════════════════════════
# STEP 2. Claude API로 테스트 생성
# ══════════════════════════════════════════════════════
def generate_test(topic: str) -> dict:
    if not ANTHROPIC_API_KEY:
        print("⚠️  ANTHROPIC_API_KEY 없음.")
        return fallback_test()

    prompt = f"""You are writing a Korean psychology test for SOULCAKEY website.
Topic: "{topic}"

Output ONLY a valid JSON object with NO comments, NO markdown, NO explanations.
Use this exact structure:

{{"id":"unique_english_id","title":"한국어 제목 20자 이하","heroTitle":"제목<br>2줄","heroSub":"부제목<br>설명","emoji":"🎯","thumbColor":1,"badge":"NEW","categories":["성격"],"participantsLabel":"🔥 1.2만명","estimatedMinutes":2,"questions":[{{"emoji":"😊","text":"질문 내용","answers":[{{"text":"답변1","scores":{{"a":3,"b":1}}}},{{"text":"답변2","scores":{{"b":3,"c":1}}}},{{"text":"답변3","scores":{{"c":3,"d":1}}}},{{"text":"답변4","scores":{{"d":3,"a":1}}}}]}}],"results":[{{"id":"a","emoji":"🌟","title":"당신은 <em>'결과 제목'</em> 같은 사람!","desc":"3문장 설명","chemistry":{{"good":{{"emoji":"😊","name":"잘맞는유형"}},"bad":{{"emoji":"😤","name":"안맞는유형"}}}}}}]}}

STRICT RULES:
1. questions = exactly 5 items
2. results = exactly 4 items  
3. categories: choose from [연애, 성격, 회사생활, B급감성, MBTI, 음식]
4. thumbColor: integer 1-8
5. NO // comments anywhere in JSON
6. ALL strings use double quotes only
7. Output ONLY the JSON object, nothing else"""

    try:
        res = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 4000,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=60
        )
        res.raise_for_status()
        text = res.json()["content"][0]["text"].strip()

        # JSON 정제
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'^```\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
        text = re.sub(r'//[^\n"]*\n', '\n', text)   # 주석 제거
        text = re.sub(r',(\s*[}\]])', r'\1', text)   # trailing comma 제거
        text = text.strip()

        data = json.loads(text)
        data["thumbColor"] = random.randint(1, 8)    # 매번 랜덤 색상
        print(f"✅ 생성 완료: {data.get('title')}")
        return data

    except Exception as e:
        print(f"⚠️  Claude API 실패: {e}")
        return fallback_test()


# ══════════════════════════════════════════════════════
# 기본 테스트 (API 실패 시)
# ══════════════════════════════════════════════════════
def fallback_test() -> dict:
    topics = [
        ("음식", "🍜", "당신은 어떤 음식 같은 사람?", "ramen", ["성격"]),
        ("동물", "🐾", "당신은 어떤 동물 같은 사람?", "animal", ["성격"]),
        ("날씨", "🌈", "당신은 어떤 날씨 같은 사람?", "weather", ["성격", "연애"]),
        ("커피", "☕", "당신은 어떤 커피 같은 사람?", "coffee2", ["성격", "연애"]),
        ("색깔", "🎨", "당신은 어떤 색깔 같은 사람?", "color", ["성격"]),
    ]
    t = random.choice(topics)
    return {
        "id": f"{t[3]}_{TIMESTAMP}",
        "title": t[2],
        "heroTitle": f"당신은 어떤<br>{t[0]} 같은 사람인가요?",
        "heroSub": f"5가지 질문으로 알아보는<br>나의 {t[0]} 유형",
        "emoji": t[1],
        "thumbColor": random.randint(1, 8),
        "badge": "NEW",
        "categories": t[4],
        "participantsLabel": f"🔥 {random.randint(1,5)}.{random.randint(1,9)}만명",
        "estimatedMinutes": 2,
        "questions": [
            {"emoji": "🌅", "text": "아침에 일어났을 때 나는?",
             "answers": [
                 {"text": "바로 활기차게 시작!", "scores": {"a": 3, "b": 1}},
                 {"text": "천천히 여유롭게.", "scores": {"b": 3, "c": 1}},
                 {"text": "할 일 먼저 확인.", "scores": {"c": 3, "d": 1}},
                 {"text": "조금 더 누워있기.", "scores": {"d": 3, "a": 1}},
             ]},
            {"emoji": "💬", "text": "친구가 고민을 털어놓을 때 나는?",
             "answers": [
                 {"text": "해결책을 바로 제시!", "scores": {"a": 3, "b": 1}},
                 {"text": "끝까지 들어준다.", "scores": {"b": 3, "c": 1}},
                 {"text": "같이 맛있는 거 먹자!", "scores": {"c": 3, "d": 1}},
                 {"text": "조용히 옆에 있어준다.", "scores": {"d": 3, "a": 1}},
             ]},
            {"emoji": "🏖️", "text": "갑자기 3일 휴가가 생겼다!",
             "answers": [
                 {"text": "친구들과 여행!", "scores": {"a": 3, "b": 1}},
                 {"text": "혼자 카페에서 쉬기.", "scores": {"b": 3, "c": 1}},
                 {"text": "감성 장소 탐방.", "scores": {"c": 3, "d": 1}},
                 {"text": "집에서 푹 쉬기.", "scores": {"d": 3, "a": 1}},
             ]},
            {"emoji": "💌", "text": "좋아하는 사람이 생겼을 때 나는?",
             "answers": [
                 {"text": "바로 고백!", "scores": {"a": 3, "b": 1}},
                 {"text": "자연스럽게 다가간다.", "scores": {"b": 3, "c": 1}},
                 {"text": "친구한테 먼저 물어본다.", "scores": {"c": 3, "d": 1}},
                 {"text": "혼자 마음속으로만.", "scores": {"d": 3, "a": 1}},
             ]},
            {"emoji": "😤", "text": "스트레스 해소법은?",
             "answers": [
                 {"text": "친구들과 신나게!", "scores": {"a": 3, "b": 1}},
                 {"text": "혼자 산책.", "scores": {"b": 3, "c": 1}},
                 {"text": "맛있는 거 먹기.", "scores": {"c": 3, "d": 1}},
                 {"text": "집에서 혼자만의 시간.", "scores": {"d": 3, "a": 1}},
             ]},
        ],
        "results": [
            {"id": "a", "emoji": "🔥", "title": "당신은 <em>'에너지 넘치는<br>불꽃'</em> 같은 사람!",
             "desc": "어딜 가나 분위기를 밝히는 에너지의 소유자예요. 목표를 향해 거침없이 나아가고, 함께 있으면 항상 즐거워요. 그 열정이 당신의 가장 큰 무기예요! ✨",
             "chemistry": {"good": {"emoji": "🌊", "name": "차분한 물결"}, "bad": {"emoji": "🍃", "name": "조용한 바람"}}},
            {"id": "b", "emoji": "🌊", "title": "당신은 <em>'깊고 차분한<br>바다'</em> 같은 사람!",
             "desc": "겉으로는 고요하지만 내면에는 깊은 감정이 있어요. 한번 맺은 인연을 소중히 여기고 신뢰를 중요시해요. 진국 중의 진국이에요! 💙",
             "chemistry": {"good": {"emoji": "🔥", "name": "활기찬 불꽃"}, "bad": {"emoji": "⚡", "name": "즉흥적인 번개"}}},
            {"id": "c", "emoji": "🌸", "title": "당신은 <em>'따뜻하고 포근한<br>봄바람'</em> 같은 사람!",
             "desc": "주변 사람들에게 따뜻한 온기를 전하는 사람이에요. 공감 능력이 뛰어나고 배려심이 넘쳐요. 당신 곁에 있으면 항상 편안해요! 🌷",
             "chemistry": {"good": {"emoji": "⚡", "name": "에너지 넘치는 번개"}, "bad": {"emoji": "🔥", "name": "강렬한 불꽃"}}},
            {"id": "d", "emoji": "⚡", "title": "당신은 <em>'자유롭고 번뜩이는<br>번개'</em> 같은 사람!",
             "desc": "예측 불가능한 매력으로 주변을 놀라게 하는 타입이에요. 창의력이 넘치고 새로운 것을 두려워하지 않아요. 늘 신선한 에너지를 줘요! ⚡",
             "chemistry": {"good": {"emoji": "🌸", "name": "따뜻한 봄바람"}, "bad": {"emoji": "🌊", "name": "차분한 바다"}}},
        ]
    }


# ══════════════════════════════════════════════════════
# STEP 3. tests/*.js 저장
# ══════════════════════════════════════════════════════
def save_test_js(data: dict) -> str:
    os.makedirs(TESTS_DIR, exist_ok=True)
    filename = f"{data['id']}.js"
    filepath = os.path.join(TESTS_DIR, filename)
    js = f"""/* SOULCAKEY — tests/{filename} | 자동 생성: {TODAY} */
TESTS['{data["id"]}'] = {json.dumps(data, ensure_ascii=False, indent=2)};
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(js)
    print(f"✅ 파일 저장: {filepath}")
    return filename


# ══════════════════════════════════════════════════════
# STEP 4. index.html 업데이트
# ══════════════════════════════════════════════════════
def inject_script_tag(filename: str):
    index_path = os.path.join(SITE_DIR, "index.html")
    if not os.path.exists(index_path):
        print(f"⚠️  {index_path} 없음.")
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
            '<script src="js/engine.js"></script>',
            f'{new_tag}\n<script src="js/engine.js"></script>'
        )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(updated)
    print(f"✅ index.html 업데이트 완료")


# ══════════════════════════════════════════════════════
# STEP 5. Google Sheets 기록
# ══════════════════════════════════════════════════════
def update_sheets(data: dict):
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
        sheet = service.spreadsheets()

        # 헤더 없으면 추가
        try:
            existing = sheet.values().get(
                spreadsheetId=SHEETS_ID, range=f"{SHEET_NAME}!A1:A1"
            ).execute()
            if not existing.get("values"):
                sheet.values().update(
                    spreadsheetId=SHEETS_ID, range=f"{SHEET_NAME}!A1",
                    valueInputOption="USER_ENTERED",
                    body={"values": [["날짜", "테스트ID", "제목", "카테고리", "질문수", "결과수", "상태"]]}
                ).execute()
        except:
            pass

        sheet.values().append(
            spreadsheetId=SHEETS_ID, range=f"{SHEET_NAME}!A:G",
            valueInputOption="USER_ENTERED",
            body={"values": [[
                TODAY, data["id"], data["title"],
                ", ".join(data.get("categories", [])),
                len(data.get("questions", [])),
                len(data.get("results", [])),
                "발행완료"
            ]]}
        ).execute()
        print("✅ Google Sheets 기록 완료")
    except Exception as e:
        print(f"⚠️  Sheets 실패: {e}")


# ══════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"\n🚀 SOULCAKEY 시작 | {TODAY}\n{'─'*40}")
    topic = get_topic()
    data  = generate_test(topic)
    print(f"📋 제목: {data['title']}")
    filename = save_test_js(data)
    inject_script_tag(filename)
    update_sheets(data)
    print(f"\n🎉 완료! '{data['title']}' 발행됨")
