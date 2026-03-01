"""
generate_dashboard.py
tests/ 폴더의 .js 파일들을 읽어서 dashboard-data.json 생성
"""

import os
import json
import re
from datetime import datetime

TESTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'mindpop', 'tests')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'dashboard-data.js')

def extract_field(js_text, field):
    """JS 객체에서 필드값 추출"""
    # string 필드
    m = re.search(rf"['\"]?{field}['\"]?\s*:\s*['\"]([^'\"]+)['\"]", js_text)
    if m:
        return m.group(1)
    # number 필드
    m = re.search(rf"['\"]?{field}['\"]?\s*:\s*(\d+)", js_text)
    if m:
        return int(m.group(1))
    # null 필드
    m = re.search(rf"['\"]?{field}['\"]?\s*:\s*null", js_text)
    if m:
        return None
    return None

def extract_array_field(js_text, field):
    """배열 필드 추출 (categories 등)"""
    m = re.search(rf"['\"]?{field}['\"]?\s*:\s*\[([^\]]+)\]", js_text)
    if m:
        items = re.findall(r"['\"]([^'\"]+)['\"]", m.group(1))
        return items
    return []

def count_occurrences(js_text, keyword):
    """keyword 등장 횟수 (questions, results 개수 추출용)"""
    return len(re.findall(rf"emoji\s*:", js_text)) // 2  # 대략적 추정

def parse_js_file(filepath):
    """JS 파일 파싱해서 테스트 메타데이터 반환"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath).replace('.js', '')
    stat = os.stat(filepath)
    modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d')

    # title에서 HTML 태그 제거
    title = extract_field(content, 'title') or filename
    title = re.sub(r'<[^>]+>', '', title)

    # questions 개수
    q_count = len(re.findall(r'emoji\s*:', content.split('results')[0]))

    # results 개수  
    results_section = content.split('results')[1] if 'results' in content else ''
    r_count = len(re.findall(r'\bid\s*:', results_section))

    return {
        'id': extract_field(content, 'id') or filename,
        'title': title,
        'emoji': extract_field(content, 'emoji') or '🧠',
        'badge': extract_field(content, 'badge'),
        'categories': extract_array_field(content, 'categories'),
        'participantsLabel': extract_field(content, 'participantsLabel') or '',
        'estimatedMinutes': extract_field(content, 'estimatedMinutes') or 2,
        'thumbColor': extract_field(content, 'thumbColor') or 1,
        'questionCount': q_count,
        'resultCount': r_count,
        'filename': filename,
        'lastModified': modified,
    }

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    tests = []
    if not os.path.exists(TESTS_DIR):
        print(f"[ERROR] tests 폴더 없음: {TESTS_DIR}")
        return

    for fname in sorted(os.listdir(TESTS_DIR)):
        if not fname.endswith('.js'):
            continue
        fpath = os.path.join(TESTS_DIR, fname)
        try:
            data = parse_js_file(fpath)
            tests.append(data)
            print(f"[OK] {fname} → {data['title'][:30]}")
        except Exception as e:
            print(f"[WARN] {fname} 파싱 실패: {e}")

    output = {
        'generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'totalTests': len(tests),
        'tests': tests
    }

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(f"window.DASHBOARD_DATA = {json.dumps(output, ensure_ascii=False, indent=2)};")

    print(f"\n✅ 완료! {len(tests)}개 테스트 → dashboard-data.js")

if __name__ == '__main__':
    main()
