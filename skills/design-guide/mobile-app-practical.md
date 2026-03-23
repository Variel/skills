# 모바일 앱 디자인 가이드 — 실무 레퍼런스

> 📍 이 문서는 `mobile-app.md`의 **Step 3. 실무 수치 확인**에서 참조됩니다.

> 접근성, iOS/Android 플랫폼 차이, 실무 수치, 내비게이션 패턴, 애니메이션, 성능.

## 접근성 상세 가이드

"모바일 접근성은 데스크톱보다 더 중요하다. 모바일은 모든 상황에서 사용된다 — 밝은 햇빛, 한 손, 이동 중, 소음 속."

```
Dynamic Type (iOS) / 텍스트 크기 조절 (Android):
  모든 텍스트는 시스템 크기 설정을 존중해야 한다
  테스트: 가장 큰 크기로 설정하고 레이아웃 깨짐 확인
  규칙:
    고정 높이 컨테이너에 텍스트 넣지 말라 (잘림 위험)
    줄 수 제한 시: numberOfLines + lineBreakMode (truncation)
    최소 텍스트 크기: 11pt (이보다 작으면 읽기 어려움)

VoiceOver (iOS) / TalkBack (Android):
  모든 인터랙티브 요소: accessibilityLabel 필수
  이미지:
    의미 있는 이미지: 내용 설명 (예: "팀 미팅 중인 사람들")
    장식 이미지: accessibilityElementsHidden = true
  커스텀 컴포넌트:
    accessibilityRole 명시 (button, link, header, image...)
    상태 변화: accessibilityValue 업데이트

  테스트: 눈 감고 VoiceOver/TalkBack만으로 주요 플로우 완수할 수 있는가?

터치 타겟:
  최소: 44×44pt (iOS) / 48×48dp (Android)
  인접 타겟 간격: 최소 8px (실수 방지)
  작은 시각적 요소도: 터치 영역은 최소 크기 유지 (padding으로)

  안티패턴: 시각적 크기 = 터치 영역 (아이콘 16px → 터치 영역도 16px)
  올바름: 시각적 16px 아이콘 + 투명 padding으로 48px 터치 영역

색상 & 대비:
  텍스트: 4.5:1 이상 (WCAG AA)
  대형 텍스트 (18px+): 3:1 이상
  UI 컴포넌트: 3:1 이상

  야외 사용 고려:
    햇빛 아래에서도 읽을 수 있는가?
    대비 높은 모드 테스트 필수

모션:
  Reduce Motion 설정 존중 (iOS: UIAccessibility.isReduceMotionEnabled)
  대안: 화려한 전환 → 심플한 페이드 또는 즉시 전환
  Parallax 효과: Reduce Motion에서 완전 비활성화
  자동 재생 미디어: 자동 정지
```

---

## iOS vs Android 플랫폼 차이

두 플랫폼은 철학이 다르다. "하나의 디자인으로 양쪽을 커버하겠다"는 나이브한 접근이다. 최소한 아래 차이를 인지하라.

```
내비게이션:
  iOS: 좌측 엣지 스와이프 → 뒤로 가기 (시스템 제스처)
  Android: 하단 백 버튼/제스처 → 뒤로 가기

  iOS: 내비게이션 바 좌측 [< 뒤로] 텍스트
  Android: 내비게이션 바 좌측 ← 화살표 아이콘

  결론: iOS 스와이프 뒤로를 차단하면 사용자가 혼란

상태 바:
  iOS: Dynamic Island (62px) / 노치 (47px) / 일반 (20px)
  Android: 24dp 고정
  → safe area 상단 처리 필수 (env(safe-area-inset-top))

하단 영역:
  iOS: 홈 인디케이터 34pt (safe area bottom)
  Android: 제스처 내비게이션 바 또는 3버튼 바
  → 하단 고정 요소는 safe area 위에 배치

타이포그래피:
  iOS: SF Pro (시스템 기본), Dynamic Type 시스템
  Android: Roboto (시스템 기본), Material Type Scale
  크로스 플랫폼: 시스템 폰트 사용 권장 또는 커스텀 폰트 양쪽 동일 적용

모달/시트:
  iOS: pageSheet (.formSheet) — 상단 둥근 모서리, 카드형
  Android: BottomSheet — 하단에서 올라옴, 풀스크린 가능

  iOS 16+: UISheetPresentationController (스냅 포인트 자동)
  Android: Material BottomSheetDialogFragment

날짜/시간 피커:
  iOS: 휠 스타일 또는 인라인 캘린더
  Android: Material DatePicker (캘린더 뷰)
  → 네이티브 피커 사용 권장 (사용자 익숙함)
  크로스 플랫폼: 커스텀 피커 시 양쪽 관례를 모두 테스트

알림:
  iOS: 배너 → 알림 센터 (스와이프로 행동)
  Android: 알림 패널 (인라인 행동 버튼, 진행 바 가능)

  iOS 10+: Rich Notification (이미지, 버튼)
  Android: Notification Channels (카테고리별 제어)

앱 아이콘:
  iOS: 1024×1024px, 라운드 사각형(자동 마스킹), 그림자 없음
  Android: 1024×1024px, Adaptive Icon (전경 + 배경 레이어)
  → 아이콘의 핵심 요소를 중앙 66% 안에 배치 (마스킹 대비)
```

---

## 실무 수치

### 접근법 A: iOS HIG 기반

```
고정 치수:
  상태 바         = 54px (Dynamic Island), 47px (노치), 20px (구형)
  내비게이션 바   = 44pt (Large Title +52pt = 96pt)
  탭 바           = 49pt + 하단 safe area 34pt
  콘텐츠 좌우 마진 = 16pt (컴팩트), 20pt (레귤러)

터치 타겟:
  최소 = 44×44pt / 권장 = 48×48pt / 버튼 간 최소 간격 = 8pt

타이포 (SF Pro, Dynamic Type):
  Large Title = 34pt Bold    Headline    = 17pt Semibold
  Title 1     = 28pt Bold    Body        = 17pt Regular
  Title 2     = 22pt Bold    Subheadline = 15pt Regular
  Title 3     = 20pt Semibold Footnote   = 13pt Regular
  Caption 1   = 12pt Regular Caption 2   = 11pt Regular

색상:
  systemBlue  = #007AFF (라이트) / #0A84FF (다크)
  systemRed   = #FF3B30 / #FF453A
  systemGreen = #34C759 / #30D158
  separator   = rgba(60,60,67,0.29) / rgba(84,84,88,0.6)
  배경 grouped = #F2F2F7 / #000000
```

### 접근법 B: Material Design 3 기반

```
고정 치수:
  상태 바      = 24dp
  Top App Bar  = 64dp(Small), 152dp(Medium), 280dp(Large)
  Bottom Nav   = 80dp
  FAB          = 56×56dp / 확장 96×96dp

터치 타겟: 최소 48×48dp

타이포 (Material 3):
  Display Large  = 57sp / line-height 64sp / tracking -0.25
  Display Medium = 45sp / 52sp
  Display Small  = 36sp / 44sp
  Headline Large = 32sp / 40sp
  Title Large    = 22sp / 28sp
  Body Large     = 16sp / 24sp / tracking +0.50
  Body Medium    = 14sp / 20sp / tracking +0.25
  Label Large    = 14sp / 20sp / tracking +0.10

Elevation: 0dp(배경) → 1dp(카드) → 3dp(버튼) → 6dp(FAB) → 8dp(nav) → 12dp(다이얼로그)

Shape: None(0) → ExtraSmall(4dp) → Small(8dp) → Medium(12dp) → Large(16dp) → ExtraLarge(28dp) → Full(50%)
```

### 접근법 C: 커스텀 디자인 시스템

```
간격 (6px 베이스):
  xxs = 2px   sm  = 12px   xl  = 36px
  xs  = 4px   md  = 18px   2xl = 48px
  s   = 6px   lg  = 24px   3xl = 72px

타이포 (브랜드 폰트):
  Micro    = 10px/600/uppercase/tracking +1.5px
  Caption  = 12px/400/tracking +0.3px
  Body     = 16px/400/line-height 1.5
  Title    = 24px/700/tracking -0.5px
  Hero     = 32px/800/tracking -1.0px

컴포넌트:
  리스트 아이템 = 56px 높이
  카드          = padding 16px, radius 12px
  인풋 필드     = 48px 높이, radius 8px
  Bottom Sheet  = radius 상단 20px, drag handle 36×4px
```

---

## 모바일 내비게이션 패턴 비교

```
패턴 A — 하단 탭 바 (Instagram, Uber):
  3-5개 최상위 목적지, 항상 표시, 한 손 접근 용이
  49pt(iOS) / 80dp(Android)

  규칙: 현재 탭 재탭 = 루트로 스크롤 + 스택 초기화
  규칙: 탭 아이콘 아래 레이블 필수 (아이콘만은 접근성 위반)
  규칙: 각 탭 아이콘은 활성/비활성 상태 구분 (filled vs outlined)

패턴 B — 햄버거 + 드로어 (Gmail, Slack):
  목적지 5개 초과 시, 계층적 내비게이션

  규칙: 드로어 너비 = 화면의 85% (최대 360px), 나머지는 딤 오버레이
  규칙: 엣지 스와이프 또는 햄버거 아이콘으로 열기
  안티패턴: 핵심 기능을 드로어 안에 숨기기 (발견하기 어렵다)

패턴 C — 제스처 기반 (Tinder, 지도):
  몰입형 경험, 카드 탐색, 미디어 소비

  규칙: 제스처 힌트(onboarding)가 반드시 필요
  규칙: 제스처의 대안 UI 항상 제공 (버튼, 메뉴)

패턴 D — 바텀 시트 기반 (Apple Maps, Uber):
  맥락 보존 + 상세 정보 동시 노출
  최대: 화면 - 64px 상단 여유

  규칙: 드래그 핸들이 보여야 시트가 조작 가능하다는 것을 인지
  규칙: 키보드가 올라오면 시트도 함께 올라가야 한다
```

---

## 모바일 애니메이션 & 트랜지션

```
화면 전환:
  Push (일반): 우→좌 슬라이드 300ms ease-out
  Pop (뒤로): 좌→우 슬라이드 250ms ease-in-out
  Modal 올림: 아래→위 슬라이드 350ms spring
  Modal 닫기: 위→아래 슬라이드 250ms ease-in
  탭 전환: 크로스 페이드 150ms (슬라이드 아님)

  iOS: UINavigationController 기본 전환은 interactive pop gesture와 연결
  Android: Material Shared Axis 또는 Fade Through

공유 요소 전환:
  목록 → 상세: 선택한 이미지/카드가 확대되며 상세 화면으로
  iOS: UIViewControllerAnimatedTransitioning
  Android: Shared Element Transition

  규칙: 전환 시작점과 끝점을 명확히 연결하라 (공간적 연속성)
  규칙: 전환 중 다른 요소는 페이드 아웃 → 전환 후 페이드 인

마이크로인터랙션:
  토글 전환: 200ms spring
  체크박스 체크: 150ms + 체크마크 그리기 애니메이션
  좋아요: 300ms scale(1→1.3→1) + 색상 전환 + 파티클(선택)
  삭제 스와이프: 항목 사라짐 300ms + 아래 항목 올라옴 200ms
  풀 투 리프레시 스피너: 당김에 비례한 회전 → 릴리즈 후 자동 회전

  60fps 유지 규칙:
    애니메이션은 transform + opacity만 사용 (레이아웃 변경 최소화)
    긴 리스트 스크롤 중 복잡한 애니메이션 피하라
    그림자 변경은 비용이 높다 → 가능하면 사전 렌더링
```

---

## 모바일 성능 & 체감 속도

```
체감 속도 기준:
  100ms   = 즉각 반응 (터치 피드백, 토글)
  300ms   = 빠름 (화면 전환, 드롭다운)
  1000ms  = 허용 (데이터 로딩, 검색 결과)
  3000ms+ = 느림 (스켈레톤 필수, 진행 표시기)
  10000ms = 한계 (사용자가 떠날 수 있다)

이미지 최적화:
  포맷: WebP (iOS 14+ / Android 4.0+)
  리사이징: 표시 크기의 2x (Retina 대응)
  지연 로딩: 뷰포트 밖 이미지는 스크롤 접근 시 로드
  placeholder: LQIP(Low Quality Image Placeholder) 또는 dominant color

  썸네일: 50-100KB 이하
  히어로: 200-400KB 이하
  전체 화면: 500KB-1MB 이하

앱 시작 속도:
  Cold Start 목표: 2초 이내
  Warm Start 목표: 1초 이내

  시각적 피드백: 스플래시 → 스켈레톤 → 콘텐츠
  안티패턴: 모든 데이터를 시작 시 로드 (필요한 것만 먼저)

  첫 의미 있는 콘텐츠(First Meaningful Content): 가능한 빨리
    → 캐시된 데이터 먼저 표시 + 백그라운드 갱신

메모리:
  이미지 캐시: 메모리 50-100MB 제한
  리스트: 셀 재사용으로 메모리 일정 유지
  대형 미디어: 화면에서 벗어나면 즉시 해제
```
