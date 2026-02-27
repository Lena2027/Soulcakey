/* =============================================
   SOULCAKEY — tests/coffee.js
   ─────────────────────────────────────────────
   ✅ 새 테스트를 추가하려면 이 파일을 복사해서
      tests/ 폴더에 넣고 TESTS 객체에 등록하세요.
   ─────────────────────────────────────────────
   필드 설명:
   id              - 고유 식별자 (영어, 붙여쓰기)
   title           - 카드에 표시될 제목
   heroTitle       - 히어로 배너용 제목 (HTML 가능)
   heroSub         - 히어로 배너 부제목
   emoji           - 대표 이모지
   thumbColor      - 썸네일 색상 (1~8)
   badge           - 'HOT' | 'NEW' | null
   categories      - 카테고리 배열 (필터 탭 기준)
   participantsLabel - 참여자 수 텍스트
   estimatedMinutes  - 예상 소요 시간
   questions       - 질문 배열
     └ emoji       - 질문 이모지
     └ text        - 질문 내용
     └ answers     - 답변 배열
         └ text    - 답변 텍스트
         └ scores  - { resultId: 점수 } (여러 결과에 점수 분배 가능)
   results         - 결과 유형 배열
     └ id          - questions의 scores에서 참조할 ID
     └ emoji       - 결과 이모지
     └ title       - 결과 제목 (HTML 가능, <em> 강조 사용 권장)
     └ desc        - 결과 설명 (3~4줄)
     └ chemistry
         └ good    - { emoji, name } 잘 맞는 유형
         └ bad     - { emoji, name } 안 맞는 유형
   ============================================= */

TESTS['coffee'] = {
  id: 'coffee',
  title: '당신은 어떤 커피 같은 사람인가요?',
  heroTitle: '당신은 어떤<br>커피 같은 사람인가요?',
  heroSub: '성격부터 연애 스타일까지<br>딱 5문제로 알아보는 나의 커피 유형',
  emoji: '☕',
  thumbColor: 1,
  badge: 'HOT',
  categories: ['성격', '연애'],
  participantsLabel: '🔥 3.2만명',
  estimatedMinutes: 2,

  /* ── 질문 ── */
  questions: [
    {
      emoji: '☕',
      text: '카페에 들어갔습니다. 메뉴를 고르는 방법은?',
      answers: [
        { text: '그냥 늘 마시던 걸로. 변화는 필요 없어.',           scores: { iceamericano: 3, espresso: 1 } },
        { text: '오늘의 추천 메뉴를 물어본다. 새로운 거 도전!',       scores: { latte: 2, bubbletea: 2 } },
        { text: '메뉴판을 5분 동안 분석한 뒤 신중하게 결정.',         scores: { espresso: 3, iceamericano: 1 } },
        { text: '직원이 마시면 맛있겠다고 한 걸 주문한다.',           scores: { latte: 3, bubbletea: 1 } },
      ]
    },
    {
      emoji: '📱',
      text: '연락이 잘 안 되는 친구가 갑자기 연락이 왔어요. 반응은?',
      answers: [
        { text: '"어? 살아있었어?" 빠르게 답장하고 수다 떤다.',       scores: { bubbletea: 3, latte: 1 } },
        { text: '읽고 나중에 답장한다. (근데 나중이 언제인지 모름)', scores: { iceamericano: 3, espresso: 1 } },
        { text: '반가워서 바로 전화를 건다.',                        scores: { latte: 2, bubbletea: 2 } },
        { text: '짧게 답하고 안부만 물어본다.',                      scores: { espresso: 3, iceamericano: 1 } },
      ]
    },
    {
      emoji: '🌧️',
      text: '갑자기 비가 쏟아졌어요. 우산이 없을 때 나의 선택은?',
      answers: [
        { text: '그냥 맞으면서 뛰어간다. 시원하잖아.',               scores: { iceamericano: 3, espresso: 1 } },
        { text: '카페에 들어가서 비 그칠 때까지 기다린다.',           scores: { latte: 3, bubbletea: 1 } },
        { text: '편의점에서 바로 우산을 구매한다.',                   scores: { espresso: 3, iceamericano: 1 } },
        { text: '누군가에게 도움을 요청한다.',                        scores: { bubbletea: 3, latte: 1 } },
      ]
    },
    {
      emoji: '🎉',
      text: '모임에 처음 참석했을 때 나는?',
      answers: [
        { text: '먼저 말을 걸며 분위기를 주도한다.',                  scores: { bubbletea: 3, latte: 1 } },
        { text: '누군가 먼저 말을 걸어올 때까지 관찰한다.',           scores: { espresso: 2, iceamericano: 2 } },
        { text: '아는 사람 옆에 바짝 붙어있는다.',                    scores: { latte: 3, bubbletea: 1 } },
        { text: '음식·음료 가져오는 척 자연스럽게 대화를 시작한다.', scores: { iceamericano: 2, latte: 2 } },
      ]
    },
    {
      emoji: '💌',
      text: '좋아하는 사람이 생겼을 때 나의 행동은?',
      answers: [
        { text: '티 안 낸다. 절대. 혼자 마음속으로만.',               scores: { iceamericano: 3, espresso: 1 } },
        { text: '주변에 들키지 않게 살살 다가간다.',                  scores: { espresso: 2, iceamericano: 2 } },
        { text: '친구한테 말하고 어떻게 할지 전략을 짠다.',           scores: { latte: 2, bubbletea: 2 } },
        { text: '그냥 직접 말한다. 상대방도 알아야 하니까.',          scores: { bubbletea: 3, latte: 1 } },
      ]
    },
  ],

  /* ── 결과 유형 ── */
  results: [
    {
      id: 'iceamericano',
      emoji: '🧊',
      title: '당신은 <em>\'차갑지만 따뜻한<br>아이스 아메리카노\'</em> 같은 사람!',
      desc: '처음 만났을 땐 차갑고 도도해 보이지만, 알고 보면 누구보다 깊은 정이 있어요. 혼자만의 시간을 소중히 여기고, 감정 표현이 서툴지만 행동으로 마음을 전하는 타입이에요. 한 번 믿기 시작하면 끝까지 곁에 있어주는 사람입니다. ☕',
      chemistry: {
        good: { emoji: '🧋', name: '달콤한 버블티' },
        bad:  { emoji: '🍵', name: '진지한 녹차' },
      }
    },
    {
      id: 'latte',
      emoji: '☕',
      title: '당신은 <em>\'부드럽고 따뜻한<br>카페라떼\'</em> 같은 사람!',
      desc: '주변 사람들을 편안하게 만드는 특별한 능력이 있어요. 갈등을 싫어하고 모두와 잘 어울리는 분위기 메이커예요. 때론 너무 배려하다가 자신을 잃기도 하지만, 그 따뜻함이 당신의 최고 무기랍니다. ☁️',
      chemistry: {
        good: { emoji: '🧊', name: '쿨한 아메리카노' },
        bad:  { emoji: '🧃', name: '달달한 주스' },
      }
    },
    {
      id: 'espresso',
      emoji: '⚡',
      title: '당신은 <em>\'강렬하고 집중력 있는<br>에스프레소\'</em> 같은 사람!',
      desc: '적은 말로도 핵심을 찌르는 날카로운 사람이에요. 효율을 중시하고, 한번 목표를 잡으면 끝까지 파고드는 집념이 있어요. 처음엔 강렬해서 어렵게 느껴질 수 있지만, 믿을 수 있는 사람이에요. ⚡',
      chemistry: {
        good: { emoji: '🧁', name: '달콤한 마카롱' },
        bad:  { emoji: '☕', name: '느긋한 라떼' },
      }
    },
    {
      id: 'bubbletea',
      emoji: '🧋',
      title: '당신은 <em>\'에너지 넘치는<br>버블티\'</em> 같은 사람!',
      desc: '어딜 가나 분위기를 살리는 활기찬 에너지의 소유자예요. 새로운 것에 대한 호기심이 많고, 사람들과 함께할 때 가장 빛나는 타입이에요. 가끔 에너지가 넘쳐서 피곤하게 느껴질 수 있지만, 함께 있으면 항상 즐거워요! 🎉',
      chemistry: {
        good: { emoji: '⚡', name: '진중한 에스프레소' },
        bad:  { emoji: '🧊', name: '차가운 아메리카노' },
      }
    },
  ]
};
