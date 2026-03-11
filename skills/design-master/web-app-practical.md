# 웹 앱 디자인 가이드 — 실무 레퍼런스

> 접근성, 간격·타이포·색상 수치, 애니메이션, 반응형 전략, 대시보드 패턴.

## 접근성 상세 가이드

"접근성은 체크리스트가 아니라 설계 원칙이다." 후반에 추가하는 것이 아니라, 첫 와이어프레임부터 고려하라.

```
포커스 관리 (SPA 필수):
  페이지 전환 시: 새 페이지의 <h1> 또는 주 콘텐츠에 포커스 이동
  모달 열림: 모달 첫 포커스 가능 요소로 이동, Tab 트랩
  모달 닫힘: 트리거 요소로 포커스 복원
  동적 콘텐츠 추가: aria-live="polite"로 스크린 리더에 알림
  삭제 행동: 삭제된 항목의 다음/이전 항목으로 포커스 이동

포커스 스타일:
  :focus-visible 사용 (마우스 클릭 시 불필요한 아웃라인 제거)
  아웃라인: 2px solid, primary 색, offset 2px
  고대비 모드 대응: outline-style: solid (dotted/dashed 피함)

키보드 내비게이션:
  모든 인터랙티브 요소: Tab으로 도달 가능
  커스텀 위젯: 방향키(←→↑↓) 내부 이동 + Tab으로 위젯 탈출
  단축키: 최소 ⌘Z(undo), ⌘S(save), Esc(닫기/취소) 지원
  단축키 충돌: OS/브라우저 기본 단축키와 겹치지 않게

ARIA 라이브 리전 결정:
  긴급/차단적 → aria-live="assertive" (에러, 로그아웃 경고)
  비긴급 정보 → aria-live="polite" (성공 메시지, 결과 개수)
  사용하지 말 것 → 캐러셀 자동 전환, 마케팅 배너, 대화상자 열림(aria-haspopup 사용)

색상 대비:
  일반 텍스트: 4.5:1 이상 (WCAG AA)
  대형 텍스트(18px+ 또는 14px+ Bold): 3:1 이상
  UI 컴포넌트(아이콘, 테두리): 3:1 이상
  권장: APCA 기준 Lc 60+ (본문), Lc 45+ (대형 텍스트)

모션:
  prefers-reduced-motion: reduce 미디어 쿼리 존중
  대안: 애니메이션 → 즉시 전환(instant), 또는 지속시간 0ms
  절대 금지: 깜빡임 3회/초 이상 (발작 위험)
```

---

## 실무 수치 — 간격, 타이포, 색상

### 접근법 A: 8px 그리드 시스템 — 구조적 엄밀함

8px 배수 기준. Atlassian, Red Hat, GitHub 등 대규모 디자인 시스템에서 채택.

```
간격 스케일 (Atlassian 기준):
  space.025 =  2px   (미세 조정)
  space.050 =  4px   (아이콘 내부 패딩)
  space.075 =  6px   (보조 간격)
  space.100 =  8px   (인접 요소 간 최소 간격)
  space.150 = 12px   (폼 필드 내부 패딩)
  space.200 = 16px   (카드 패딩, 리스트 항목 간격)
  space.300 = 24px   (섹션 내 그룹 간격)
  space.400 = 32px   (섹션 간 간격)
  space.600 = 48px   (페이지 영역 구분)
  space.800 = 64px   (최상위 레이아웃 마진)
  space.1000= 80px   (페이지 간 대구분)

  음수 간격(Negative): -2px ~ -32px (컨테이너 패딩 탈출, 요소 겹침 시)

타이포그래피 (8px line-height 정렬):
  Caption     12px / line-height 16px (2×8)
  Body-sm     14px / line-height 20px
  Body        16px / line-height 24px (3×8)
  Heading-sm  20px / line-height 28px
  Heading     24px / line-height 32px (4×8)
  Display     32px / line-height 40px (5×8)

버튼 높이:
  Small   = 28px (padding: 4px 12px)
  Medium  = 36px (padding: 8px 16px)
  Large   = 44px (padding: 10px 24px)
```

**적합**: 엔터프라이즈 SaaS, 데이터 중심 대시보드, 대규모 팀 협업 제품.

### 접근법 B: 4px 베이스 + 유연한 스케일

4px 최소 단위. Vercel(Geist), Linear, Tailwind CSS 등 모던 제품.

```
간격 스케일 (Tailwind 호환):
  0.5 = 2px    2   = 8px    5   = 20px
  1   = 4px    3   = 12px   6   = 24px
  1.5 = 6px    4   = 16px   8   = 32px

타이포그래피 (Geist 스타일):
  Caption     11px / line-height 16px / tracking +0.01em / weight 400
  Label       13px / line-height 16px / tracking +0.00em / weight 500
  Body        14px / line-height 20px / tracking  0.00em / weight 400
  Title       16px / line-height 24px / tracking -0.011em/ weight 500
  Heading     24px / line-height 32px / tracking -0.029em/ weight 600
  Display     48px / line-height 48px / tracking -0.040em/ weight 700

버튼:
  Small   = 32px 높이 (padding: 0 12px, font: 13px, radius: 6px)
  Medium  = 36px 높이 (padding: 0 16px, font: 14px, radius: 8px)
  Large   = 44px 높이 (padding: 0 20px, font: 14px, radius: 10px)
  아이콘 전용 = 36×36 (radius: 8px)
```

**적합**: 개발자 도구, 프로젝트 관리 앱, 밀도 높은 모던 SaaS.

### 접근법 C: 콘텐츠 폭 중심 레이아웃

사이드바 없이 콘텐츠 max-width 제한. Notion, Substack, 문서형 앱.

```
콘텐츠 최대 폭:
  읽기 중심   = max-width: 680px  (블로그, 문서, 설정)
  작업 중심   = max-width: 960px  (폼, 리스트, 상세 뷰)
  대시보드    = max-width: 1200px (카드 그리드, 차트)
  전폭(Full)  = 제한 없음        (테이블, 캔버스, IDE)

페이지 마진:
  ≤768px   : padding 16px
  769-1024 : padding 32px
  1025-1440: padding 48px (또는 auto margin + max-width)
  ≥1441    : padding 64px (또는 중앙 정렬)

수직 리듬:
  같은 그룹 내 요소     = 8-12px
  논리적 블록 간        = 24-32px
  페이지 섹션 간        = 48-64px
  페이지 상단 여백      = 32-48px
```

**적합**: 문서 도구, CMS, 블로그, 설정/프로필 페이지.

### 접근법 D: 다크 테마 우선 설계

다크 모드 기본, 라이트 파생. Figma, Discord, Spotify.

```
다크 테마 색상:
  배경:
    Surface-0   = #0A0A0A (페이지 배경)
    Surface-1   = #111111 (카드, 패널)
    Surface-2   = #1A1A1A (호버, 선택)
    Surface-3   = #222222 (인풋, 드롭다운)
  텍스트:
    Primary     = #EDEDED (대비 15.4:1)
    Secondary   = #A0A0A0 (대비 7.1:1)
    Tertiary    = #666666 (대비 3.8:1)
  테두리:
    Subtle      = #1F1F1F
    Default     = #2E2E2E
    Strong      = #444444
  강조:
    Brand       = #3B82F6
    Success     = #22C55E
    Warning     = #F59E0B
    Danger      = #EF4444

라이트 테마 대응:
  Surface-0 → #FFFFFF     Primary text → #111111
  Surface-1 → #F9FAFB     Secondary text → #6B7280
  Surface-2 → #F3F4F6     Border Default → #E5E7EB
```

**적합**: 코드 에디터, 미디어 플랫폼, 데이터 모니터링.

---

## 애니메이션 & 트랜지션

```
지속시간 원칙:
  즉각 피드백 (토글, 체크박스)     = 100ms
  작은 전환 (호버, 포커스)         = 150ms
  중간 전환 (드롭다운, 탭)         = 200ms
  큰 전환 (모달, 페이지)           = 300ms
  복잡한 전환 (페이지 전환, 레이아웃) = 400ms
  500ms 이상은 "느리다"고 느낀다 — 피하라

이징 함수:
  ease-out (빠르게 시작, 부드럽게 끝) → 대부분의 등장 애니메이션에 사용
  ease-in (느리게 시작, 빠르게 끝)   → 퇴장 애니메이션
  ease-in-out                      → 위치 이동, 레이아웃 변경
  linear                           → 프로그래스 바, 로딩 스피너

비대칭 타이밍:
  등장 = 300ms / 퇴장 = 200ms (등장이 살짝 더 길어야 자연스럽다)
  모달 등장 = 200ms scale(0.95→1) + fade / 모달 퇴장 = 150ms fade

CSS 커스텀 이징 참고:
  Material: cubic-bezier(0.4, 0, 0.2, 1)  — standard
  Apple:    cubic-bezier(0.25, 0.1, 0.25, 1) — default
  Vercel:   cubic-bezier(0.16, 1, 0.3, 1)  — spring-like
```

---

## 반응형 브레이크포인트 전략 비교

```
전략 A — 디바이스 중심 (Bootstrap 전통):
  sm: 576px   md: 768px   lg: 992px   xl: 1200px   2xl: 1400px
  → 직관적, 디바이스 범주 명확 / 768-992px 구간이 어정쩡

전략 B — 콘텐츠 중심 (Tailwind 현대):
  sm: 640px   md: 768px   lg: 1024px  xl: 1280px   2xl: 1536px
  → 콘텐츠 흐름 맞춤, 와이드 모니터 우수 / 디바이스 매핑 덜 직관적

전략 C — 레이아웃 전환 중심 (커스텀):
  compact: ≤640px   (단일 칼럼, 사이드바 숨김)
  medium:  641-1024px (사이드바 접힘 or 오버레이)
  wide:    1025-1440px (사이드바 + 콘텐츠)
  ultra:   ≥1441px  (사이드바 + 콘텐츠 + 보조 패널)
  → 실제 레이아웃 변화에 직결 / 팀 내 합의 필요

사이드바 너비 변화 (전략 C):
  compact  → 0px (hamburger)
  medium   → 64px (아이콘만)
  wide     → 240px (펼침)
  ultra    → 280px + 보조 패널 320px
```

---

## 대시보드 설계 패턴

대시보드는 "모든 것을 한눈에"가 아니라 "가장 중요한 것을 한눈에"다.

```
KPI 카드:
  구조: 레이블(12-14px, muted) + 수치(28-36px, Bold) + 변화(%)(14px, 색상)
  높이: 80-120px
  그리드: 1행에 3-5개 (반응형: 모바일 1-2개)
  수치 변화: ▲ 초록 (긍정), ▼ 빨강 (부정), — 회색 (변화 없음)
  수치 포맷: 1,234 (쉼표) / 12.3K (축약) / $1.2M (단위 포함)

차트 배치:
  1행: KPI 카드 바 (전체 너비)
  2행: 주요 차트 (2/3) + 보조 차트 또는 리스트 (1/3)
  3행: 데이터 테이블 (전체 너비)

  차트당 하나의 인사이트. 차트 상단에 인사이트 헤드라인을 넣어라
  예: "이번 달 매출이 전월 대비 23% 증가했습니다" (차트 위 텍스트)

실시간 업데이트:
  폴링 주기: 15-60초 (용도에 따라)
  업데이트 표시: 수치 변경 시 배경 플래시(200ms) 또는 숫자 카운트업 애니메이션
  마지막 업데이트 시각: 대시보드 우측 상단에 "최종 업데이트: 2분 전"
  연결 끊김: 비커넥티비티 배너 + 마지막 데이터 유지 + 회색조 전환

위젯 레이아웃:
  CSS Grid 사용: grid-template-columns: repeat(12, 1fr)
  위젯 최소 크기: 3칼럼 × 200px 높이
  간격: 16-24px
  사용자 커스텀: 드래그로 위치/크기 조절 (선택적)
```
