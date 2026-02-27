/* =============================================
   SOULCAKEY — engine.js
   테스트 실행 엔진. 건드리지 마세요.
   새 테스트를 추가할 때는 tests/ 폴더만 건드리면 됩니다.
   ============================================= */

const Engine = (() => {
  let currentTest = null;   // 현재 실행 중인 테스트 데이터
  let currentQ    = 0;      // 현재 질문 인덱스
  let scores      = {};     // { resultId: score } 누적 점수

  /* ── 페이지 전환 ── */
  function showPage(name) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById('page-' + name).classList.add('active');
    window.scrollTo(0, 0);
  }

  /* ── 테스트 시작 ── */
  function startTest(testId) {
    const test = TESTS[testId];
    if (!test) return console.error(`테스트 '${testId}'를 찾을 수 없습니다.`);

    currentTest = test;
    currentQ    = 0;
    scores      = {};
    // 모든 결과 id를 0으로 초기화
    test.results.forEach(r => { scores[r.id] = 0; });

    showPage('test');
    renderQuestion();
  }

  /* ── 질문 렌더링 ── */
  function renderQuestion() {
    const q     = currentTest.questions[currentQ];
    const total = currentTest.questions.length;
    const pct   = Math.round(((currentQ + 1) / total) * 100);

    // 프로그레스 바
    document.getElementById('q-count').textContent        = `${currentQ + 1} / ${total}`;
    document.getElementById('q-percent').textContent      = `${pct}%`;
    document.getElementById('progress-fill').style.width = pct + '%';

    // 질문 애니메이션 재실행
    const area = document.getElementById('question-area');
    area.style.animation = 'none';
    area.offsetHeight;
    area.style.animation = 'fadeSlide 0.4s ease';

    document.getElementById('q-emoji').textContent = q.emoji;
    document.getElementById('q-text').textContent  = q.text;

    // 답변 버튼 렌더링
    const answersEl = document.getElementById('answers');
    answersEl.innerHTML = '';
    q.answers.forEach(answer => {
      const btn = document.createElement('button');
      btn.className = 'answer-btn';
      btn.innerHTML = `<span>${answer.text}</span>`;
      btn.onclick   = () => selectAnswer(btn, answer.scores);
      answersEl.appendChild(btn);
    });
  }

  /* ── 답변 선택 ── */
  function selectAnswer(btn, answerScores) {
    if (btn.classList.contains('selected')) return;

    // 모든 버튼 비활성화
    document.querySelectorAll('.answer-btn').forEach(b => b.style.pointerEvents = 'none');
    btn.classList.add('selected');

    // 점수 누적: { iceamericano: 2, espresso: 1 } 형태
    if (answerScores) {
      Object.entries(answerScores).forEach(([id, val]) => {
        scores[id] = (scores[id] || 0) + val;
      });
    }

    setTimeout(() => {
      currentQ++;
      if (currentQ < currentTest.questions.length) {
        renderQuestion();
      } else {
        showResult();
      }
    }, 600);
  }

  /* ── 결과 계산 & 렌더링 ── */
  function showResult() {
    // 가장 높은 점수의 결과 찾기
    const topResultId = Object.entries(scores)
      .sort(([, a], [, b]) => b - a)[0][0];

    const result = currentTest.results.find(r => r.id === topResultId);
    if (!result) return;

    // 결과 카드 채우기
    document.getElementById('result-type-label').textContent = `${result.emoji} 당신의 유형`;
    document.getElementById('result-emoji').textContent      = result.emoji;
    document.getElementById('result-title').innerHTML        = result.title;
    document.getElementById('result-desc').textContent       = result.desc;

    // 케미 채우기
    document.getElementById('chem-good-emoji').textContent = result.chemistry.good.emoji;
    document.getElementById('chem-good-name').textContent  = result.chemistry.good.name;
    document.getElementById('chem-bad-emoji').textContent  = result.chemistry.bad.emoji;
    document.getElementById('chem-bad-name').textContent   = result.chemistry.bad.name;

    showPage('result');
  }

  /* ── 공유 유틸 ── */
  function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2200);
  }

  /* ── Public API ── */
  return { startTest, showPage, showToast };
})();

/* 전역 바인딩 (HTML onclick에서 사용) */
function startTest(id)  { Engine.startTest(id); }
function showPage(name) { Engine.showPage(name); }

function shareKakao() { Engine.showToast('카카오톡 공유 기능은 SDK 연동 후 활성화됩니다 💬'); }
function copyLink()   {
  navigator.clipboard.writeText(window.location.href)
    .then(() => Engine.showToast('링크가 복사되었어요! 🔗'))
    .catch(() => Engine.showToast('복사하려면 HTTPS 환경이 필요해요'));
}
function saveImage()  { Engine.showToast('이미지 저장 기능은 Canvas 생성 후 활성화됩니다 📸'); }
