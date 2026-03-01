TESTS['연락_스타일로_보는_나의_연애_유형_202603011612'] = {
  id: '연락_스타일로_보는_나의_연애_유형_202603011612',
  title: '연락 스타일로 보는 나의 연애 유형',
  heroTitle: '내 <em>연락 스타일</em>로 알아보는<br>진짜 연애 성향은?',
  heroSub: '메시지 하나로 드러나는 당신의 애착 유형',
  emoji: '💌',
  thumbColor: 3,
  badge: 'NEW',
  categories: ['연애', '심리', '소통'],
  participantsLabel: '🔥 0명',
  estimatedMinutes: 3,
  questions: [
    {
      emoji: '📱',
      text: '좋아하는 사람에게서 연락이 왔을 때 나의 반응은?',
      answers: [
        { text: '즉시 확인하고 바로 답장을 보낸다', scores: { instant: 2 } },
        { text: '메시지를 여러 번 읽어보고 신중하게 답장한다', scores: { thoughtful: 2 } },
        { text: '내 일정에 맞춰 여유 있을 때 답장한다', scores: { free: 2 } },
        { text: '상대방의 메시지 톤에 맞춰 답장 스타일을 조절한다', scores: { empathic: 2 } },
      ]
    },
    {
      emoji: '⏰',
      text: '하루 동안 연인과의 연락 빈도로 적당하다고 생각하는 것은?',
      answers: [
        { text: '계속 연결되어 있는 느낌이 들 정도로 자주', scores: { instant: 2 } },
        { text: '아침, 점심, 저녁 정도의 규칙적인 안부', scores: { thoughtful: 2 } },
        { text: '특별한 일이 있을 때나 하고 싶을 때만', scores: { free: 2 } },
        { text: '상대방의 스케줄과 기분을 고려해서 유동적으로', scores: { empathic: 2 } },
      ]
    },
    {
      emoji: '💭',
      text: '메시지로 감정을 표현할 때 나는?',
      answers: [
        { text: '솔직하고 직접적으로 내 감정을 다 드러낸다', scores: { instant: 2 } },
        { text: '신중하게 단어를 선택해서 정확히 전달한다', scores: { thoughtful: 2 } },
        { text: '너무 무거워지지 않게 가볍게 표현한다', scores: { free: 2 } },
        { text: '상대방이 받아들이기 편한 방식으로 조절한다', scores: { empathic: 2 } },
      ]
    },
    {
      emoji: '😰',
      text: '연인이 평소보다 답장이 늦을 때 나의 반응은?',
      answers: [
        { text: '불안해하며 여러 번 메시지를 확인하고 걱정한다', scores: { instant: 2 } },
        { text: '이유가 있을 거라 생각하고 기다려준다', scores: { thoughtful: 2 } },
        { text: '별로 신경 쓰지 않고 내 일을 계속한다', scores: { free: 2 } },
        { text: '상대방 상황을 먼저 생각해보고 이해하려 한다', scores: { empathic: 2 } },
      ]
    },
    {
      emoji: '💝',
      text: '진지한 대화나 깊은 얘기를 시작할 때 나는?',
      answers: [
        { text: '바로 솔직하게 내 마음을 털어놓는다', scores: { instant: 2 } },
        { text: '적절한 타이밍을 기다렸다가 차근차근 얘기한다', scores: { thoughtful: 2 } },
        { text: '너무 무거운 분위기가 되지 않게 조심스럽게', scores: { free: 2 } },
        { text: '상대방의 컨디션과 기분을 먼저 파악한다', scores: { empathic: 2 } },
      ]
    },
    {
      emoji: '⚡',
      text: '연인과 의견 충돌이나 갈등이 생겼을 때?',
      answers: [
        { text: '빨리 해결하고 싶어서 계속 연락을 시도한다', scores: { instant: 2 } },
        { text: '냉정을 찾고 정리해서 대화를 제안한다', scores: { thoughtful: 2 } },
        { text: '서로 시간을 두고 자연스럽게 풀리기를 기다린다', scores: { free: 2 } },
        { text: '상대방의 감정을 먼저 살피고 맞춰서 접근한다', scores: { empathic: 2 } },
      ]
    },
    {
      emoji: '💕',
      text: '연인과의 관계 상태를 확인하고 싶을 때?',
      answers: [
        { text: '직접 물어보거나 관련 대화를 자주 꺼낸다', scores: { instant: 2 } },
        { text: '적절한 순간에 진지하게 대화 시간을 갖는다', scores: { thoughtful: 2 } },
        { text: '굳이 말로 하지 않고 자연스런 분위기로 파악한다', scores: { free: 2 } },
        { text: '상대방의 말이나 행동에서 신호를 세심하게 읽는다', scores: { empathic: 2 } },
      ]
    }
  ],
  results: [
    {
      id: 'instant',
      emoji: '⚡',
      title: '<em>즉답형 로맨티스트</em>',
      desc: '사랑할 때는 온 마음을 다하는 당신! 연락이 오면 즉시 반응하고, 상대방의 빠른 답장을 기대해요. 감정 표현이 솔직하고 직접적이며, 연인과의 연결감을 중시하는 따뜻한 마음의 소유자입니다. 다만 때로는 상대방에게 부담을 줄 수 있으니, 적당한 여유를 두는 것도 좋아요.',
      chemistry: {
        good: { emoji: '🤗', name: '신중한 감정 표현가' },
        bad: { emoji: '🌊', name: '자유로운 소통러' },
      }
    },
    {
      id: 'thoughtful',
      emoji: '🎯',
      title: '<em>신중한 감정 표현가</em>',
      desc: '균형 잡힌 소통의 달인이에요. 메시지 하나하나에 진심을 담아 신중하게 전달하고, 상대방의 감정도 세심하게 배려해요. 깊이 있는 대화를 선호하며 안정적인 관계를 추구하는 당신은 연애에서 가장 이상적인 파트너 타입이에요. 상대방에게 든든한 안정감을 주는 존재입니다.',
      chemistry: {
        good: { emoji: '⚡', name: '즉답형 로맨티스트' },
        bad: { emoji: '🌊', name: '자유로운 소통러' },
      }
    },
    {
      id: 'free',
      emoji: '🌊',
      title: '<em>자유로운 소통러</em>',
      desc: '독립적이고 자유로운 영혼의 소유자예요. 연락 빈도나 시간에 얽매이지 않고, 서로의 개인 공간을 존중하는 여유로운 연애 스타일을 추구해요. 압박감 없는 자연스러운 관계를 선호하며, 상대방에게도 같은 자유로움을 기대합니다. 때로는 더 많은 관심 표현이 필요할 수도 있어요.',
      chemistry: {
        good: { emoji: '💫', name: '감정 동조형 공감자' },
        bad: { emoji: '⚡', name: '즉답형 로맨티스트' },
      }
    },
    {
      id: 'empathic',
      emoji: '💫',
      title: '<em>감정 동조형 공감자</em>',
      desc: '상대방의 마음을 읽는 천재예요! 상대방의 감정 상태와 상황을 항상 고려하며, 그에 맞춰 유연하게 소통 스타일을 조절해요. 높은 공감 능력으로 상대방이 편안함을 느낄 수 있게 만드는 따뜻한 연인이에요. 가끔은 자신의 욕구도 솔직하게 표현하는 것을 잊지 마세요.',
      chemistry: {
        good: { emoji: '🌊', name: '자유로운 소통러' },
        bad: { emoji: '🎯', name: '신중한 감정 표현가' },
      }
    }
  ]
};