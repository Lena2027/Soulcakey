/* =============================================
   SOULCAKEY — main.js
   메인 페이지 카드 렌더링 & 카테고리 필터.
   건드릴 일 거의 없습니다.
   ============================================= */

/* ── 카테고리 필터 ── */
function filterCat(el, category) {
  document.querySelectorAll('.cat-tag').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  renderCards(category);
}

/* ── 카드 그리드 렌더링 ── */
function renderCards(filterCategory = '전체') {
  const grid = document.getElementById('test-grid');
  if (!grid) return;

  const filteredTests = Object.values(TESTS).filter(test =>
    filterCategory === '전체' || test.categories.includes(filterCategory)
  );

  grid.innerHTML = filteredTests.map(test => `
    <div class="test-card" onclick="startTest('${test.id}')">
      <div class="card-thumb thumb-${test.thumbColor}">
        <span>${test.emoji}</span>
        ${test.badge ? `<div class="card-hot">${test.badge}</div>` : ''}
      </div>
      <div class="card-body">
        <div class="card-tags">
          ${test.categories.map(c => `<span class="card-tag">#${c}</span>`).join('')}
        </div>
        <div class="card-title">${test.title}</div>
        <div class="card-meta">
          <div class="card-participants">${test.participantsLabel}</div>
          <span>→</span>
        </div>
      </div>
    </div>
  `).join('');
}

/* ── 히어로 배너 렌더링 ── */
function renderHero() {
  // badge가 'HOT'인 테스트를 히어로로 표시, 없으면 첫 번째
  const hero = Object.values(TESTS).find(t => t.badge === 'HOT') || Object.values(TESTS)[0];
  if (!hero) return;

  document.getElementById('hero-title').innerHTML      = hero.heroTitle || hero.title;
  document.getElementById('hero-sub').innerHTML        = hero.heroSub   || '';
  document.getElementById('hero-emoji').textContent    = hero.emoji;
  document.getElementById('hero-participants').innerHTML = `
    ${hero.emoji} ${hero.participantsLabel} &nbsp;|&nbsp; ⏱ 약 ${hero.estimatedMinutes || 2}분 소요 &nbsp;|&nbsp; 📌 ${hero.categories.join(' · ')}
  `;
  document.getElementById('hero-btn').onclick = () => startTest(hero.id);
}

/* ── 페이지 로드 시 초기화 ── */
window.addEventListener('DOMContentLoaded', () => {
  renderHero();
  renderCards();
});
