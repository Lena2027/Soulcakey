/* =============================================
   SOULCAKEY — tests/office.js
   "직장에서 나는 어떤 캐릭터?" 테스트
   ============================================= */

TESTS['office'] = {
  id: 'office',
  title: '직장에서 나는 어떤 캐릭터일까?',
  heroTitle: '직장에서 나는<br>어떤 캐릭터일까?',
  heroSub: '회의실부터 퇴근길까지<br>당신의 진짜 직장인 유형을 찾아드려요',
  emoji: '🏢',
  thumbColor: 2,
  badge: 'NEW',
  categories: ['회사생활', '성격'],
  participantsLabel: '👥 1.8만명',
  estimatedMinutes: 2,

  questions: [
    {
      emoji: '📋',
      text: '월요일 아침 회의. 팀장이 아이디어를 물어봤을 때 나는?',
      answers: [
        { text: '미리 준비해온 아이디어를 자신 있게 발표한다.',       scores: { leader: 3, planner: 1 } },
        { text: '좋은 아이디어가 떠올랐지만 일단 눈치를 본다.',       scores: { silent: 3, supporter: 1 } },
        { text: '다른 사람 아이디어에 적극적으로 공감하며 보완한다.', scores: { supporter: 3, planner: 1 } },
        { text: '이미 머릿속에 정리된 계획을 조목조목 설명한다.',     scores: { planner: 3, leader: 1 } },
      ]
    },
    {
      emoji: '😤',
      text: '억울한 업무가 떨어졌을 때 나의 반응은?',
      answers: [
        { text: '왜 제 업무죠? 정중하게 이의를 제기한다.',            scores: { leader: 3, planner: 1 } },
        { text: '속으로 욕하면서 그냥 한다. 어쩌겠어.',               scores: { silent: 3, supporter: 1 } },
        { text: '일단 해놓고 나중에 넌지시 어필한다.',                scores: { supporter: 2, planner: 2 } },
        { text: '일정과 리소스를 계산해서 현실적으로 협의한다.',      scores: { planner: 3, leader: 1 } },
      ]
    },
    {
      emoji: '🍱',
      text: '점심시간, 팀 회식 메뉴를 정해야 해요. 나는?',
      answers: [
        { text: '"제가 맛집 알아요!" 바로 추천하고 예약까지 잡는다.', scores: { leader: 3, supporter: 1 } },
        { text: '"아무거나요~" 진심으로 아무거나 괜찮다.',             scores: { silent: 3, supporter: 1 } },
        { text: '모두가 좋아할 메뉴를 조율하며 의견을 모은다.',       scores: { supporter: 3, planner: 1 } },
        { text: '회식 장소 후보를 엑셀로 정리해서 공유한다.',         scores: { planner: 3, silent: 1 } },
      ]
    },
    {
      emoji: '📮',
      text: '퇴근 10분 전, 긴급 업무가 들어왔어요!',
      answers: [
        { text: '일정 조율하고 내일 첫 번째로 처리하겠다고 한다.',    scores: { leader: 2, planner: 2 } },
        { text: '남아서 처리한다. 언제 또 이런 부탁을 하겠어.',       scores: { silent: 2, supporter: 2 } },
        { text: '우선순위를 따져보고 팀원에게 배분한다.',             scores: { leader: 3, planner: 1 } },
        { text: '야근 전 체크리스트를 작성하고 차근차근 진행한다.',   scores: { planner: 3, silent: 1 } },
      ]
    },
    {
      emoji: '🏆',
      text: '팀 프로젝트가 성공했어요! 나의 소감은?',
      answers: [
        { text: '"제 전략이 통했군요 ㅎ" (속마음)',                   scores: { leader: 3, planner: 1 } },
        { text: '"다들 수고했어요..." 조용히 자리로 돌아간다.',        scores: { silent: 3, planner: 1 } },
        { text: '"팀원들이 다 잘해줘서요!" 진심으로 공을 돌린다.',    scores: { supporter: 3, silent: 1 } },
        { text: '이번 프로젝트 회고 문서를 이미 작성 중이다.',        scores: { planner: 3, leader: 1 } },
      ]
    },
  ],

  results: [
    {
      id: 'leader',
      emoji: '🦁',
      title: '당신은 <em>\'타고난 팀장<br>리더형\'</em>!',
      desc: '회의실에서 가장 먼저 손드는 타입이에요. 추진력이 있고 결단력이 빠르며, 자연스럽게 팀을 이끄는 카리스마가 있어요. 간혹 독단적으로 보일 수 있지만, 팀이 흔들릴 때 가장 먼저 중심을 잡아주는 존재예요. 🦁',
      chemistry: {
        good: { emoji: '📊', name: '꼼꼼한 플래너형' },
        bad:  { emoji: '🦁', name: '또 다른 리더형' },
      }
    },
    {
      id: 'planner',
      emoji: '📊',
      title: '당신은 <em>\'완벽주의<br>플래너형\'</em>!',
      desc: '계획 없이 움직이는 것을 극도로 싫어하는 타입이에요. 모든 걸 체계적으로 정리하고, 리스크를 미리 파악하는 능력이 탁월해요. 함께 일하면 "이 사람 없으면 안 돼"라는 말을 듣는 핵심 인재예요. 📋',
      chemistry: {
        good: { emoji: '🦁', name: '추진력 있는 리더형' },
        bad:  { emoji: '🌊', name: '즉흥적인 자유인' },
      }
    },
    {
      id: 'supporter',
      emoji: '🌻',
      title: '당신은 <em>\'팀의 비타민<br>서포터형\'</em>!',
      desc: '팀원들이 편하게 일할 수 있도록 분위기를 만드는 데 탁월해요. 공감 능력이 뛰어나고 협업 상황에서 빛을 발하는 타입이에요. 조용히 곁에서 돕는 것 같지만, 사실 팀의 모든 것을 꿰뚫고 있는 무서운 사람입니다. 🌻',
      chemistry: {
        good: { emoji: '📊', name: '체계적인 플래너형' },
        bad:  { emoji: '😤', name: '독단적인 외로운 늑대' },
      }
    },
    {
      id: 'silent',
      emoji: '🎯',
      title: '당신은 <em>\'말 없이 결과로 보여주는<br>조용한 에이스\'</em>!',
      desc: '존재감은 없는 것 같지만, 성과물을 열면 항상 가장 완성도가 높은 타입이에요. 불필요한 사교에 에너지 낭비하기보다 업무에 집중하는 것을 선호해요. 팀장이 가장 믿고 의지하는 숨은 보물 같은 존재예요. 🎯',
      chemistry: {
        good: { emoji: '🌻', name: '살갑게 챙겨주는 서포터형' },
        bad:  { emoji: '🎙️', name: '수다스러운 관심종자형' },
      }
    },
  ]
};
