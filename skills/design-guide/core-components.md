# 핵심 컴포넌트 상세 가이드

> 자주 쓰이는 컴포넌트의 패딩, 간격, 라운딩, 사이즈 상세 스펙. 일관된 UI를 위한 기준값.

---

## 사이즈 체계

모든 컴포넌트는 동일한 사이즈 체계를 공유한다. 혼용하지 말라.

```
Size Scale (높이 기준):
  xs   = 24px   (뱃지, 태그, 작은 아이콘 버튼)
  sm   = 32px   (보조 버튼, 작은 인풋)
  md   = 40px   (기본값 — 대부분의 버튼/인풋)
  lg   = 48px   (강조 CTA, 모바일 터치 최적)
  xl   = 56px   (히어로 CTA, 대형 입력)
```

---

## 버튼 (Button)

### 사이즈별 스펙

```
       높이    패딩(좌우)   폰트     라운딩    아이콘
xs     24px    8px        12px     4px       16px
sm     32px    12px       13px     6px       16px
md     40px    16px       14px     8px       20px
lg     48px    20px       15px     8px       20px
xl     56px    24px       16px     10px      24px
```

### 내부 구조

```
┌─────────────────────────────────────┐
│  [패딩]  [아이콘]  [gap]  [텍스트]  [패딩]  │
└─────────────────────────────────────┘

아이콘-텍스트 gap: 8px (모든 사이즈 동일)
아이콘만 있을 때: 정사각형 (width = height)
```

### 버튼 그룹

```
버튼 간 gap: 8px (sm), 12px (md/lg)
그룹 내 버튼: 동일 사이즈 필수
구분선: 1px border, 중간 버튼 라운딩 0

┌──────┬──────┬──────┐
│ Left │ Mid  │ Right│
└──────┴──────┴──────┘
  └─ radius    └─ 0     └─ radius
```

### Variant 별 스타일

| Variant | 배경 | 텍스트 | 테두리 | 호버 |
|---------|-----|-------|-------|-----|
| **primary** | primary | white | none | primary-hover |
| **secondary** | transparent | primary | 1px primary | primary/10% bg |
| **ghost** | transparent | foreground | none | muted/50% bg |
| **danger** | destructive | white | none | destructive-hover |
| **link** | transparent | primary | none | underline |

---

## 인풋 (Input / TextField)

### 사이즈별 스펙

```
       높이    패딩(좌우)   폰트     라운딩
sm     32px    10px       13px     6px
md     40px    12px       14px     8px
lg     48px    14px       15px     8px
```

### 내부 구조

```
┌─────────────────────────────────────────┐
│ [leading]  [placeholder/value]  [trailing] │
└─────────────────────────────────────────┘

leading icon: 20px, 좌측 padding 안에 포함
trailing icon/button: 우측 padding 안에 포함
leading-텍스트 gap: 8px
텍스트-trailing gap: 8px
```

### 레이블 & 헬퍼 텍스트

```
Label
↓ 6px gap
┌─────────────────────┐
│ Input               │
└─────────────────────┘
↓ 4px gap
Helper text / Error message

레이블: 13px, weight 500
헬퍼: 12px, muted-foreground
에러: 12px, destructive
필수 표시(*): 레이블 직후, destructive 색
```

### 상태별 테두리

| 상태 | 테두리 | 배경 |
|-----|-------|-----|
| default | 1px border | transparent |
| hover | 1px border-hover | transparent |
| focus | 2px ring primary | transparent |
| error | 1px destructive | destructive/5% |
| disabled | 1px border | muted/50% |

---

## 카드 (Card)

### 기본 스펙

```
패딩: 16px (sm), 20px (md), 24px (lg)
라운딩: 8px (sm), 12px (md), 16px (lg)
테두리: 1px border (선택)
그림자: 0 1px 3px rgba(0,0,0,0.1) (선택)
```

### 내부 구조

```
┌─────────────────────────────────────┐
│ Header                         [⋯] │  ← 패딩과 동일
├─────────────────────────────────────┤  ← 1px border (선택)
│                                     │
│ Content                             │  ← 상하 패딩 동일
│                                     │
├─────────────────────────────────────┤
│ Footer                      [Action]│  ← 패딩과 동일
└─────────────────────────────────────┘

Header-Content 구분선: 1px border (선택)
Content-Footer 구분선: 없음 또는 1px border
섹션 간 gap: 16px (padding 없는 구조일 때)
```

### 카드 그리드

```
카드 간 gap: 16px (sm), 20px (md), 24px (lg)
그리드: 균등 너비 또는 min-width 기반 auto-fill
반응형: 1col (mobile) → 2col (tablet) → 3-4col (desktop)
```

---

## 모달 / 다이얼로그 (Modal)

### 사이즈별 스펙

```
         max-width    패딩
sm       400px        20px
md       560px        24px
lg       720px        24px
xl       960px        32px
full     90vw         32px
```

### 내부 구조

```
┌─────────────────────────────────────────┐
│ Title                              [×] │  ← 헤더: py-16px, px-패딩
├─────────────────────────────────────────┤  ← 1px border
│                                         │
│ Content                                 │  ← 본문: py-20px, px-패딩
│                                         │
├─────────────────────────────────────────┤  ← 1px border
│                        [Cancel] [Save] │  ← 푸터: py-16px, px-패딩
└─────────────────────────────────────────┘

타이틀: 18px (sm), 20px (md+), weight 600
닫기 버튼: 32px 터치 영역, 아이콘 20px
푸터 버튼 gap: 12px
푸터 버튼 정렬: 우측 (기본), 전체너비 (모바일)
```

### 배경 & 애니메이션

```
딤: rgba(0,0,0,0.5) — 클릭 시 닫기 (파괴적 작업 제외)
라운딩: 12px (sm/md), 16px (lg+)
등장: fade 150ms + scale(0.95→1) 200ms
퇴장: fade 100ms
```

---

## 토스트 / 스낵바 (Toast)

### 스펙

```
너비: 320-400px (데스크톱), 전체너비-32px (모바일)
높이: 자동 (최소 48px)
패딩: 12px 16px
라운딩: 8px
위치: 우측 하단 (기본), 상단 중앙 (간단한 확인)
```

### 내부 구조

```
┌─────────────────────────────────────┐
│ [icon] Message text      [Action] [×] │
└─────────────────────────────────────┘

아이콘: 20px, 좌측
아이콘-메시지 gap: 12px
메시지: 14px, 최대 2줄
액션 버튼: ghost/link variant, 우측
닫기: 20px 아이콘 (선택)
```

### 타입별 스타일

| 타입 | 아이콘 | 배경 | 자동닫힘 |
|-----|-------|-----|---------|
| success | ✓ (green) | surface | 5초 |
| info | ℹ (blue) | surface | 8초 |
| warning | ⚠ (yellow) | warning/10% | 10초 |
| error | ✕ (red) | destructive/10% | 수동 |

---

## 뱃지 / 태그 (Badge / Tag)

### 사이즈별 스펙

```
       높이    패딩(좌우)   폰트     라운딩
xs     18px    6px        11px     4px (또는 full)
sm     22px    8px        12px     4px (또는 full)
md     26px    10px       13px     6px (또는 full)
```

### 알림 뱃지 (숫자)

```
점만: 8px 원, 아이콘 우상단 50% 겹침
숫자: min-width 18px, padding 0 4px, 라운딩 full
최대: "99+" (3자리 이상 표시 금지)
위치: 부모 요소 기준 top: -4px, right: -4px
```

### Variant

| Variant | 배경 | 텍스트 |
|---------|-----|-------|
| default | muted | muted-foreground |
| primary | primary/15% | primary |
| success | success/15% | success |
| warning | warning/15% | warning |
| danger | destructive/15% | destructive |
| outline | transparent | foreground, 1px border |

---

## 아바타 (Avatar)

### 사이즈별 스펙

```
xs     24px    10px 폰트 (이니셜)
sm     32px    12px 폰트
md     40px    14px 폰트
lg     48px    16px 폰트
xl     64px    20px 폰트
2xl    96px    28px 폰트
```

### 스타일

```
라운딩: full (원형) — 기본값
폴백 순서: 이미지 → 이니셜 → 기본 아이콘
이니셜: 첫 글자 1-2개, weight 500, 대문자
상태 표시: 우하단 12px 원 (online/offline)
```

### 아바타 그룹

```
겹침: -8px (sm), -12px (md), -16px (lg)
테두리: 2px white (겹침 구분용)
최대 표시: 4-5개, 나머지 "+N" 표시
"+N" 스타일: 동일 사이즈, muted 배경
```

---

## 프로그레스 바 (Progress Bar)

### 스펙

```
높이: 4px (페이지 상단), 8px (인라인)
라운딩: full
배경: muted
채움: primary (기본), success/warning/danger (상태별)
```

### 애니메이션

```
진행: width transition 200ms ease-out
불확정(indeterminate): 좌우 왕복 1.5s ease-in-out
완료: 잠시 유지 후 fade-out 300ms
```

---

## 스켈레톤 (Skeleton)

### 스펙

```
색상: muted (배경), muted-foreground/30% (shimmer)
라운딩: 실제 콘텐츠와 동일
높이: 실제 콘텐츠와 동일 (layout shift 방지)
```

### 형태별 가이드

```
텍스트 줄: height 16-20px, 라운딩 4px
아바타: 원형, 실제 아바타 사이즈
카드: 실제 카드와 동일한 패딩/구조
테이블 행: 실제 행과 동일한 높이
```

### 애니메이션

```
Shimmer: 좌→우 그라데이션 슬라이드
주기: 1.5-2초
이징: linear
```

---

## 간격 시스템 요약

```
Component 간격:
  같은 그룹 내 요소: 8px
  연관 그룹 간: 16px
  섹션 간: 24-32px
  페이지 섹션 간: 48-64px

내부 패딩:
  작은 요소 (badge, tag): 6-8px
  중간 요소 (button, input): 12-16px
  큰 요소 (card, modal): 20-24px
  페이지 컨테이너: 16px (mobile), 24-32px (desktop)
```

---

## 라운딩 시스템 요약

```
none   = 0px     (테이블 셀, 일부 인풋)
sm     = 4px     (badge, tag, 작은 요소)
md     = 6px     (button sm)
default= 8px     (button, input, card — 기본값)
lg     = 12px    (card, modal)
xl     = 16px    (large modal, 히어로 카드)
full   = 9999px  (avatar, pill badge)
```
