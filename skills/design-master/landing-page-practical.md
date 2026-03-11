# 랜딩 페이지 디자인 가이드 — 실무 레퍼런스

> 마이크로카피, Core Web Vitals, 모바일 반응형, 업종별 변형, 스크롤 인터랙션, SEO.

## 마이크로카피

랜딩 페이지의 전환율은 디자인 50% + 카피 50%다. 작은 텍스트가 큰 차이를 만든다.

```
CTA 버튼 카피:
  나쁨: "제출", "확인", "시작"
  보통: "가입하기", "다운로드하기"
  좋음: "무료로 시작하기 →", "내 사이트 만들기 →", "14일 무료 체험"
  최고: 결과를 암시 ("성장 시작하기", "팀을 연결하세요")

  규칙: 동사 + 결과/혜택
  규칙: "→" 화살표는 진행감을 준다
  규칙: "무료" 또는 "신용카드 불필요"를 CTA 근처에

보조 텍스트 (CTA 아래):
  "30일 환불 보장" / "언제든 해지 가능" / "설정 5분이면 끝"
  폰트: 12-13px, muted, CTA 아래 8-12px

폼 필드:
  레이블: "이메일" → "업무용 이메일" (B2B일 때)
  플레이스홀더: "you@company.com"
  에러: "이메일을 입력해주세요" → "올바른 이메일 형식을 입력해주세요 (예: name@company.com)"

가격:
  "월 $12" → "$12/월, 연간 결제 시 $9/월"
  "무료 플랜" → "Free forever — 신용카드 불필요"
  취소선: "$29" → "$19" (할인 강조)

안티패턴:
  "여기를 클릭하세요" (모호, 접근성 나쁨)
  "데모 요청" (요청이라는 단어가 장벽)
  과도한 느낌표!!! (신뢰 감소)
  모호한 약속: "혁신적인", "세계 최고의", "완벽한" (증거 없는 주장)
```

---

## 성능 & Core Web Vitals

랜딩 페이지는 속도가 전환율이다. 로드 시간 1초 증가 = 전환율 7% 감소 (Google 데이터).

```
Core Web Vitals 목표:
  LCP (Largest Contentful Paint): <2.5초
    히어로 이미지/텍스트가 2.5초 안에 렌더
    → 히어로 이미지: preload + 적정 크기 + WebP/AVIF
    → 웹폰트: font-display: swap + preload
    → Critical CSS: above-the-fold CSS 인라인

  INP (Interaction to Next Paint): <200ms
    CTA 클릭 → 시각적 반응까지 200ms 이내
    → JavaScript 번들 최소화
    → 이벤트 핸들러 최적화

  CLS (Cumulative Layout Shift): <0.1
    콘텐츠 로딩 중 레이아웃 밀림 방지
    → 이미지/비디오: width + height 또는 aspect-ratio 명시
    → 웹폰트: size-adjust로 FOUT 최소화
    → 동적 콘텐츠: 자리 예약(placeholder) 후 교체

이미지 최적화:
  히어로: WebP/AVIF, 200-400KB 이하
  섹션 이미지: WebP, 100-200KB
  아이콘/로고: SVG 또는 아이콘 폰트
  지연 로딩: 폴드 아래 모든 이미지에 loading="lazy"
  반응형: srcset + sizes로 디바이스별 최적 크기

  <img srcset="img-480.webp 480w,
               img-960.webp 960w,
               img-1920.webp 1920w"
       sizes="(max-width: 768px) 100vw, 50vw"
       loading="lazy" alt="...">

폰트 최적화:
  폰트 수: 최대 2개 패밀리
  서브셋: 사용하는 글리프만 포함 (한글: unicode-range)
  preload: <link rel="preload" href="font.woff2" as="font" crossorigin>
  font-display: swap (FOIT 방지)
  가변 폰트(Variable Font): 하나의 파일로 여러 weight

JavaScript:
  초기 번들: 100KB 이하 (gzip)
  지연 로딩: 폴드 아래 인터랙션용 JS는 dynamic import
  써드파티: analytics, chat widget 등은 defer 또는 idle callback
  안티패턴: GTM 태그 20개+ (렌더링 블로킹)
```

---

## 모바일 반응형 전략

"데스크톱 먼저 만들고 모바일에 맞추기"는 가능하지만, **모바일에서 깨지는 요소를 방치하면 전환의 60%를 잃는다** (모바일 트래픽 비율 고려).

```
레이아웃 전환:
  데스크톱 2칼럼 → 모바일 1칼럼 스택
  데스크톱 카드 그리드 3열 → 모바일 1열 스택 또는 수평 스크롤
  데스크톱 사이드 이미지 → 모바일 이미지 위/텍스트 아래
  데스크톱 수치 4열 → 모바일 2×2 그리드

타이포 스케일:
  데스크톱 → 모바일 축소 비율:
  히어로 헤드라인: 56-72px → 32-40px
  섹션 헤드라인: 36-48px → 24-32px
  본문: 16-18px → 16px (축소하지 말라)
  CTA: 16px → 16px (축소하지 말라)

간격 축소:
  섹션 padding: 96-128px → 48-64px
  그룹 간격: 48-64px → 24-32px
  좌우 마진: 48px → 16-20px

CTA 모바일 최적화:
  전체 너비 버튼 (좌우 마진 16px)
  높이: 52-56px (터치 타겟)
  고정 하단 CTA (선택적): 스크롤 시 하단에 sticky CTA 바
    높이: 64-72px (safe area 포함)
    그림자: 0 -4px 12px rgba(0,0,0,0.1) (위쪽 그림자)

모바일 특화:
  비디오: 자동 재생 비활성화 또는 정적 이미지 대체
  parallax: 비활성화 (성능)
  호버 효과: 터치에서 의미 없음 → 제거 또는 탭으로 대체
  표: 수평 스크롤 또는 카드형으로 변환

  테스트: 실제 기기에서 확인 (에뮬레이터만으로 불충분)
```

---

## 업종별 랜딩 페이지 변형

모든 랜딩 페이지가 같은 구조일 수 없다. 업종에 따라 강조점이 다르다.

```
SaaS (B2B):
  강조: 데모/무료 체험 CTA + ROI 수치 + 기업 로고
  특이점: "Book a Demo" CTA, 사례 연구 중심, 보안 인증 뱃지
  히어로: 제품 스크린샷/대시보드 캡처
  사회적 증명: 기업 로고 + 사례 연구 + G2/Capterra 평점

SaaS (B2C):
  강조: 무료 가입 CTA + 기능 시연 + 사용자 후기
  특이점: 소셜 로그인, 가격 투명성, 커뮤니티
  히어로: 사용자 경험 비주얼 (사용 중 화면)
  사회적 증명: 사용자 수 + 평점 + SNS 언급

이커머스:
  강조: 제품 이미지 + 가격 + 구매 CTA + 리뷰
  특이점: 이미지 갤러리, 사이즈 가이드, 배송 정보
  히어로: 제품 이미지 풀 블리드 + 가격 + 즉시 구매
  사회적 증명: 별점 + 리뷰 수 + "N명이 지금 보고 있습니다"
  긴급성: "재고 3개 남음", "오늘 주문하면 내일 도착"

에이전시/포트폴리오:
  강조: 작업물 쇼케이스 + 프로세스 설명 + 문의 CTA
  특이점: 비주얼 중심, 케이스 스터디, 클라이언트 로고
  히어로: 대표 작업물 + 한 줄 포지셔닝
  CTA: "프로젝트 문의" 또는 "견적 요청"

이벤트/컨퍼런스:
  강조: 날짜/장소 + 스피커 + 티켓 CTA
  특이점: 카운트다운 타이머, 스케줄, 스피커 프로필
  히어로: 이벤트 비주얼 + 날짜 + 장소 + [티켓 구매]
  긴급성: "Early Bird 할인 D-7", "잔여 좌석 50석"
  사회적 증명: 이전 행사 사진/비디오 + 참가자 수

앱 다운로드:
  강조: 기기 목업 + 스토어 뱃지 + 기능 하이라이트
  히어로: 핸드폰 목업 (기울임 3D) + 앱스토어/구글플레이 버튼
  기능: 스크린샷 캐러셀 (3-5장)
  사회적 증명: 앱스토어 평점 + 리뷰 발췌
  안티패턴: QR코드만 크게 배치 (모바일 사용자는 QR을 못 스캔한다)

오픈소스:
  강조: GitHub 스타 수 + 코드 예시 + 빠른 시작 가이드
  히어로: 터미널 코드 블록 + "npm install" 또는 "pip install"
  기능: Before/After 코드 비교
  사회적 증명: GitHub 스타, 컨트리뷰터 수, 다운로드 수
  CTA: "Get Started" + "View on GitHub" (보조)
```

---

## 실무 수치 — 히어로, CTA, 섹션 간격

### 접근법 A: 넓은 여백 + 중앙 정렬 — 프리미엄 SaaS

Stripe, Linear 스타일.

```
히어로:
  전체 높이       = 100vh (최소 700px)
  콘텐츠 max-width = 800px, 중앙 정렬
  헤드라인         = 56-72px / weight 700 / tracking -0.03em / #111
  서브라인         = 18-20px / weight 400 / line-height 1.6 / #6B7280
  헤드-서브 간격   = 24px
  서브-CTA 간격    = 32px

CTA:
  주 CTA  = height 48px, padding 0 32px, font 16px/600
            radius 12px, 배경 #111, 글자 #FFF, hover → #333
  보조 CTA = height 48px, padding 0 24px, 테두리 1px #D1D5DB
  간격 = 12px

섹션:
  padding = 96-128px (상하)
  max-width = 1200px
  그룹 간 = 48-64px
  배경 교대: #FFF → #FAFAFA → #FFF → #111
```

**적합**: B2B SaaS, 핀테크, API, 개발자 도구.

### 접근법 B: 밀도 높은 정보 — 전환율 최적화

HubSpot, Shopify 스타일.

```
히어로:
  높이 = auto (500-600px)
  2칼럼 = 텍스트 55% : 비주얼 45%, gap 48px
  헤드라인 = 40-52px / weight 800 / line-height 1.15
  배지 = 12px/600, padding 4px 12px, radius 99px, #EEF2FF/#4338CA
  신뢰 로고 바 = CTA 아래 16px, 로고 높이 24-32px, 회색조

CTA:
  주 CTA  = height 52px, padding 0 28px, font 16px/700
            radius 8px, 그라디언트 (#7C3AED → #6D28D9)
            box-shadow: 0 4px 14px rgba(124,58,237,0.35)

섹션:
  padding = 64-80px (상하)
  3칼럼 카드 = padding 32px, gap 24px, radius 16px
```

**적합**: PLG 제품, 무료 체험, 스타트업 런칭.

### 접근법 C: 풀스크린 비주얼 — 감성 우선

Apple, Arc Browser 스타일.

```
히어로:
  높이 = 100vh, 배경: 풀블리드 이미지/비디오
  오버레이 = linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.6))
  헤드라인 = 64-96px / weight 700 / #FFFFFF / 중앙
  CTA = height 56px, padding 0 40px, 배경 #FFF, 글자 #111, radius 99px
        hover → scale(1.03)

섹션:
  비주얼 = 100vh, 배경 이미지/비디오, 텍스트 오버레이
  텍스트 = padding 120-160px, max-width 640px, font 24-28px/300

색상 (다크 기조):
  배경 #000000, 텍스트 #FFFFFF/#rgba(255,255,255,0.6)
  강조 단일 컬러 (예: #FF6B35)
```

**적합**: 하드웨어, 럭셔리, 크리에이티브 도구, 이벤트.

### 접근법 D: 인터랙티브 데모 중심

Vercel, Supabase 스타일.

```
히어로:
  2칼럼: 텍스트 40% + 코드 60%
  헤드라인 = 48-56px / weight 700
  코드 블록 = padding 24px, 배경 #0D1117, radius 12px
              font 14px JetBrains Mono, line-height 1.7
              syntax: keyword #FF7B72, string #A5D6FF, function #D2A8FF

CTA:
  주 = "Get started →" height 44px, 배경 #FFF, 글자 #000, radius 8px
  터미널 CTA = height 44px, 배경 #1E1E1E, 글자 #4ADE80, 복사 아이콘

기능 섹션:
  탭 데모 = 탭 height 40px, fade 200ms
  비교 = Before(#FEE2E2) vs After(#DCFCE7)
```

**적합**: 개발자 도구, API, 인프라, 오픈소스.

---

## 스크롤 인터랙션 상세

```
Intersection Observer 패턴:
  요소가 뷰포트에 진입 시 애니메이션 트리거
  threshold: 0.2 (20% 보일 때)
  rootMargin: "0px 0px -10% 0px" (약간 더 스크롤해야 트리거)

  기본 등장: opacity 0 → 1, translateY(20px) → 0, 600ms ease-out
  엇갈림(stagger): 카드 그리드에서 각 카드 100-150ms 간격으로
  한 번만: 한번 등장하면 다시 사라지지 않음 (once: true)

Sticky 섹션 (Pin and Swap):
  좌측 텍스트 고정 + 우측 비주얼 스크롤에 따라 전환
  구현: position: sticky + Intersection Observer로 활성 항목 변경
  높이: 각 단계 × 100vh (3단계면 300vh 섹션)

  규칙: 모바일에서는 sticky 제거 → 일반 스택 레이아웃
  규칙: 현재 활성 항목을 시각적으로 강조 (opacity, color, underline)

카운트업 애니메이션:
  트리거: 뷰포트 진입 시
  기간: 1.5-2초
  이징: ease-out (빠르게 시작, 천천히 끝)
  포맷: 쉼표 구분 (1,234,567) 또는 축약 (1.2M)
  소수점: 필요 시 마지막 0.3초에 소수점 이하 추가

Parallax:
  배경 이미지: transform: translateY(calc(var(--scroll) * 0.3))
  전경 요소: 기본 스크롤 (1x)
  규칙: 3개 이상 레이어 금지 (혼란)
  규칙: 텍스트에 parallax 적용하지 말라 (가독성 저하)
  모바일: 완전 비활성화 (성능, 이질감)

  prefers-reduced-motion:
    모든 스크롤 애니메이션 → 즉시 표시 (opacity: 1, transform: none)
    parallax → 정적 배치
    카운트업 → 최종 값 즉시 표시
```

---

## SEO & 메타데이터

```
필수 메타:
  <title>: 60자 이내, 핵심 키워드 포함
  <meta name="description">: 155자 이내, CTA 포함
  Open Graph: og:title, og:description, og:image (1200×630px)
  Twitter Card: twitter:card, twitter:title, twitter:image

구조화된 데이터:
  Organization: 회사 정보 (logo, name, url)
  Product: 가격, 평점 (이커머스)
  FAQ: FAQ 섹션의 질문/답변 (FAQ Schema)
  Breadcrumb: 내비게이션 경로

시맨틱 HTML:
  <header>: 헤더/내비게이션
  <main>: 본문
  <section>: 각 섹션 (aria-labelledby로 제목 연결)
  <article>: 블로그 글, 사례 연구
  <footer>: 푸터

  h1: 페이지당 하나 (히어로 헤드라인)
  h2: 각 섹션 제목
  h3: 섹션 내 하위 제목

  안티패턴: 시각적 크기만으로 헤딩 수준 결정 (h2 건너뛰고 h4)

이미지 SEO:
  alt 텍스트: 모든 의미 있는 이미지에 설명
  장식 이미지: alt="" (빈 문자열)
  파일명: "hero-dashboard-preview.webp" (의미 있게)

성능 = SEO:
  Core Web Vitals → Google 검색 순위 팩터
  모바일 친화성 → Google 모바일 우선 인덱싱
  HTTPS → 필수
```
