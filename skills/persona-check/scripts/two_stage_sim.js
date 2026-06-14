// 2단계 합성 사용자 시뮬레이션 — Claude Code Workflow 템플릿
//
// 런타임: 이 파일은 Claude Code의 Workflow 런타임 전용이다(phase/pipeline/agent/args 전역).
// Codex 등 Workflow가 없는 환경에선 그대로 실행되지 않는다 — 아래 프롬프트·스키마(A 빌더 / B
// 워크스루 / 집계)를 그 환경의 서브에이전트나 순차 실행으로 옮겨 써라. 프롬프트 자체는 런타임 무관.
// 프롬프트·스키마 원본은 ../references/prompts.md 에 그대로 있다(이 파일과 동일하게 유지).
//
// 사용법: 아래 `FILL:` 표시된 부분(제품 도메인 한 줄, 발견경로 레퍼런스, 화면 분기 지도)만
// 제품에 맞게 채우고, args 로 페르소나 배열을 넘겨 Workflow 도구로 실행한다.
//   args = [{ id, name, seg, path }]   // path = split_personas.py가 만든 1인 1파일
// 산출물: { results: [{id,name,segment,dossier,journal}], aggregate: {report, actionItems} }
//
// 설계 원칙(오염 방지) — SKILL.md의 규칙이 이 프롬프트들에 박혀 있다. 함부로 빼지 말 것:
//  - A(빌더)와 B(워크스루)는 다른 에이전트(만드는 추론 ≠ 쓰는 추론).
//  - B엔 스키마 없음(생각을 텍스트로 흘림). 직전 선택이 다음 Read를 결정(순차 추론 강제).
//  - 앱 정체/버전/플랫폼/이전 구현/부정점화 등 단서를 흘리지 않는다.

export const meta = {
  name: 'persona-check',
  description: '합성 페르소나 N명을 2단계(빌더→워크스루)로 시뮬레이션하고 집계한다',
  phases: [
    { title: '빌더(A)', detail: '형편·니즈·발견경로→설치 도시에 완성(화면 안 봄)' },
    { title: '워크스루(B)', detail: '그 인물로 화면을 하나씩 보며 생각 일지' },
    { title: '집계', detail: '도시에+일지 N쌍 종합(화면 결함 vs 경로-기대 불일치 구분)' },
  ],
}

// ── FILL 1: 제품이 다루는 의사결정/과업을 한 줄로(앱 정체를 페르소나에게 직접 노출하지 않게,
//           빌더의 '니즈 생성'용 힌트로만). 예: '가계부/지출 관리', '중고거래', '주거 의사결정' ──
const PRODUCT_DOMAIN = '<FILL: 이 제품이 도와주는 영역 한 줄>'

// ── FILL 2: 실제 발견 경로 레퍼런스(인스타 광고/바이럴/쓰레드/유튜버/지인의 실제 말투·메시지) ──
// deep-research로 모으거나 도메인 지식으로 작성. '결' 참고용이라 직접 작성도 허용.
const DISCOVERY_REFS = `
[참고 · 이런 제품이 실제로 소개되는 말투(결만 참고, 그대로 베끼지 말 것)]
· 인스타 피드/릴스 광고 — 불안+즉시성 후크 + "회원가입 없이/무료" + CTA "지금 …하기".
· '요즘 깔아야 할 앱 모음' 바이럴(카드뉴스/블로그/쓰레드) — 여러 앱 중 한 줄 소개.
· 쓰레드 입소문(반말·솔직체) — 개인 경험담 "~해봤는데 이게 제일 …함".
· 지인 카톡 추천(드묾) — "너 ~한다며? 이거 깔아봐 [링크]".
· 유튜버 멘트(교육체) — "~하기 전에 이것부터 확인하세요(설명란 링크)".
`

// ── FILL 3: 화면 파일 경로 + 분기 지도(첫 화면 → 선택 → 다음 화면). B가 직전 선택으로 다음 Read를 고르게 한다 ──
const NAV = `
[화면 파일 · 분기 지도]
- 첫 화면(공통): /ABS/PATH/shots/01_first.png
- (선택 A) → /ABS/PATH/shots/02_a.png → /ABS/PATH/shots/03_a_result.png
- (선택 B) → /ABS/PATH/shots/02_b_result.png
- (선택 C) → /ABS/PATH/shots/02_c_result.png
`

const A_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    persona: { type: 'string' },
    segment: { type: 'string' },
    circumstances: { type: 'string', description: '직업·나이·지역·가구로 추론한 형편을 인물 목소리로 서술' },
    domainNeed: { type: 'string', description: `이 인물이 ${PRODUCT_DOMAIN}에 대해 품을 법한 구체적 사정(스스로 생성)` },
    needStrength: { type: 'string', enum: ['절박', '보통', '막연', '거의 없음'] },
    discoveryChannel: { type: 'string', description: '미디어 습관에 맞는 발견 경로 1개' },
    heardMessage: { type: 'string', description: '그 경로에서 들은/본 소개 메시지(거기서 들은 만큼)' },
    installNarrative: { type: 'string', description: '그걸 보고 설치까지 이른 생각의 흐름(1인칭)' },
  },
  required: ['persona', 'segment', 'circumstances', 'domainNeed', 'needStrength', 'discoveryChannel', 'heardMessage', 'installNarrative'],
}

const AGG_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    report: { type: 'string', description: '한국어 마크다운: 1)한눈 요약(다시열까·이탈체감·발견경로·니즈세기 분포) 2)발견 경로가 만든 기대가 첫 화면에서 충족/배신됐나(같은 화면도 경로 따라 갈림) 3)화면별 공통 반응·마찰 4)지역·생애단계 차이 5)남은 블로커. **화면 자체 결함**과 **경로-기대 불일치**를 반드시 구분. 인터랙션 결과 주장은 스크린샷 환각 가능성 표시. 근거에 인물 이름과 일지 인용.' },
    actionItems: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { item: { type: 'string' }, who: { type: 'string' }, priority: { type: 'string', enum: ['P0', 'P1', 'P2'] } }, required: ['item', 'who', 'priority'] } },
  },
  required: ['report', 'actionItems'],
}

const personas = typeof args === 'string' ? JSON.parse(args) : args

phase('빌더(A)')
const results = (await pipeline(
  personas,
  // 단계 A — 빌더: 인물 도시에 완성(앱 화면 안 봄)
  (p) => agent(
    '너는 한 명의 한국인을 ‘완성’하는 작가다. 카드의 빈칸을 그 사람답게 채워, 다음 사람이 그대로 ‘그 사람이 되어’ 행동할 수 있는 인물 도시에(dossier)를 만든다. 앱 얘기는 아직 없다.\n\n' +
    '[1] Read 도구로 ' + p.path + ' 를 읽어 인물 파악(인구통계·직업·취미·가족).\n' +
    '[2] 형편 채우기: 이 직업·나이·지역(' + p.seg + ')·가구라면 소득/모은 돈/지금 사는 형태/빚이 대략 어느 정도일지 근거와 함께 이 인물 목소리로 정하라.\n' +
    '[3] ' + PRODUCT_DOMAIN + '에 대한 사정 만들기: 이 사람이 지금 그 영역에서 품을 법한 구체적 사정을 스스로 만들어라. 생활에서 자연스럽게 나와야 하고, 세기는 절박/보통/막연/거의 없음 중 이 인물의 결대로 솔직히. 꾸미지 말 것.\n' +
    '[4] 발견 경로 → 설치: 미디어 습관에 맞는 경로 하나로 ‘어떤 앱’을 접해 막 깔아본 상태를 만든다. 앱이 무슨 앱인지는 ‘거기서 들은 만큼’만 안다(그 이상 모름). 어느 경로로, 거기서 뭐라고 적힌/말해진 걸 보고, 어떤 생각을 거쳐 설치까지 했는지 정하라.\n' +
    DISCOVERY_REFS + '\n결과는 지정된 JSON 스키마로만 출력하라.',
    { label: 'A:' + p.id, phase: '빌더(A)', schema: A_SCHEMA },
  ),
  // 단계 B — 워크스루: 그 인물이 되어 앱을 처음 써본다. 스키마 없음 = 생각 일지 텍스트.
  async (dossier, p) => {
    if (!dossier) return null
    const journal = await agent(
      '너는 아래 인물 ‘그 사람’이다. 이 도시에가 너의 형편·마음·이 앱을 알게 된 경로 전부다. 여기서 벗어나지 마라. 너는 방금 이 앱을 처음 열었고, 앱이 뭘 하는지는 ‘들은 만큼’만 안다.\n\n' +
      '[인물 도시에]\n' + JSON.stringify(dossier, null, 2) + '\n\n' +
      '[규칙 — 가장 중요] 한 번에 화면 하나씩. 반드시 이 순서로 반복하라: ① Read 도구로 그 화면 이미지를 연다 → ② ‘다음 화면을 읽기 전에’ 그 화면을 보고 든 생각을 이 인물 말투로 충분히(짧게 말고) 텍스트로 적는다: 뭐가 먼저 눈에 들어왔나, 무슨 뜻으로 읽혔나, 헷갈리거나 거슬린 건, 지금 마음, 그래서 무엇을 누를 것인가와 그 이유 → ③ 그 선택에 해당하는 ‘다음 화면’만 Read 한다. 어떤 화면을 다음에 읽을지는 네가 방금 내린 선택으로 정해진다 — 미리 다 읽지 마라. 이건 그냥 ‘어떤 앱의 화면’이다(사전 지식 없이 본 것만으로 반응).\n\n' +
      NAV + '\n' +
      '첫 화면부터 시작해 위 분기를 따라가고, 마지막 화면을 본 뒤 ‘닫을지/무엇을 누를지’와 ‘다시 열 마음이 있는지’까지 적고 끝낸다.\n\n' +
      '너의 답변은 [화면1 Read 후 생각 → 선택 → 화면2 Read 후 생각 → 선택 → … → 마무리]가 이어지는 하나의 연속된 1인칭 일지여야 한다. JSON으로 요약하지 말고 생각의 흐름을 그대로 글로 풀어라.',
      { label: 'B:' + p.id, phase: '워크스루(B)' },
    )
    return { id: p.id, name: p.name, segment: p.seg, dossier, journal }
  },
)).filter(Boolean)

phase('집계')
function trunc(s, n) { return s && s.length > n ? s.slice(0, n) + '…' : (s || '') }
const packed = results.map((r) => ({
  persona: r.name, segment: r.segment,
  need: r.dossier.domainNeed, strength: r.dossier.needStrength,
  channel: r.dossier.discoveryChannel, heard: r.dossier.heardMessage,
  journal: trunc(r.journal, 3500),
}))
const aggregate = await agent(
  '너는 UX 리서처다. 합성 페르소나 ' + results.length + '명을 2단계로 시뮬레이션했다: 각 인물은 먼저 형편·니즈·발견경로(발견→설치)를 스스로 구성했고(도시에), 그 다음 그 인물이 되어 제품 화면을 하나씩 보며 생각 일지를 남겼다(journal). 아래 N쌍을 종합해 한국어 마크다운 보고서를 써라. 일지에서 실제 표현을 인용하고 인물 이름을 근거로 달아라.\n\n' +
  JSON.stringify(packed) + '\n\n' +
  '반드시: (1) 발견 경로가 만든 기대가 첫 화면에서 충족/배신됐나(같은 화면도 경로 따라 갈릴 수 있음), (2) 화면별 공통 반응·마찰, (3) 니즈 세기와 이탈의 관계, (4) 지역·생애단계 차이, (5) 남은 블로커(actionItems P0~P2). **화면 자체 결함**과 **경로-기대 불일치**를 구분하고, ‘탭하니 반응 없음’ 같은 인터랙션 결과 주장은 정적 스크린샷 기반이라 환각일 수 있음을 표시하라.',
  { label: '집계', phase: '집계', schema: AGG_SCHEMA },
)

return { results, aggregate }
