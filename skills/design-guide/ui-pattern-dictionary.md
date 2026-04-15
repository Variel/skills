# UI 패턴 사전

> 108종 UI 패턴의 명칭과 용도를 빠르게 찾는 레퍼런스. "이 UI 이름이 뭐더라?" 할 때 참조.

---

## Navigation (14)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Hamburger Menu** | 3선 아이콘으로 메뉴 토글. 모바일 필수 | Mobile, Responsive |
| **Tab Bar** | 화면 하단 고정 주요 섹션 전환. iOS/Android 표준 | Mobile, iOS, Android |
| **Breadcrumb** | 현재 위치까지 계층 경로 표시 | Web, Hierarchy |
| **Sidebar Navigation** | 좌측 고정 네비게이션. 데스크톱 관리자 화면 | Desktop, Admin |
| **Mega Menu** | 호버 시 대형 패널 확장, 카테고리별 링크 | Web, EC, Large Site |
| **Pagination** | 콘텐츠를 페이지 단위로 분할 | Web, List |
| **Infinite Scroll** | 스크롤 끝에서 자동 추가 로딩 | Mobile, SNS, Feed |
| **Sticky Header** | 스크롤해도 상단 고정 헤더 | Web, Mobile |
| **Drawer** | 화면 가장자리에서 슬라이드인 패널 | Mobile, Responsive |
| **Command Palette** | ⌘K로 호출하는 검색+명령 UI | Desktop, Productivity |
| **Segmented Control** | 2~5개 배타적 선택지 버튼 그룹. 탭의 경량판 | iOS, Mobile, Filter |
| **Tabs** | 같은 화면 내 콘텐츠 영역 전환 | Web, Desktop, Mobile |
| **Stepper / Wizard** | 멀티스텝 프로세스 순차 안내 | Form, EC, Onboarding |
| **Anchor Navigation** | 페이지 내 섹션으로 스무스 스크롤 | LP, Web, Long-form |

---

## Layout (9)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Grid Layout** | 균등 그리드 셀에 콘텐츠 배치 | Web, Basic, Responsive |
| **Masonry Layout** | 높이 다른 카드를 벽돌처럼 빈틈없이 배치 | Web, Image, Pinterest |
| **Card Layout** | 정보를 독립 카드 단위로 정리 | Web, Mobile, Basic |
| **Split Screen** | 화면을 좌우 2분할 | LP, Web, Desktop |
| **Hero Section** | 페이지 최상단 대형 비주얼+헤드라인+CTA | LP, Web, Marketing |
| **Bento Grid** | 다양한 크기 카드를 타일 배치. 모던 대시보드 | Web, Modern, Dashboard |
| **Holy Grail Layout** | 헤더+푸터+3컬럼 전통 웹 레이아웃 | Web, Classic, Desktop |
| **Full Bleed** | 콘텐츠를 화면 너비 전체로 확장 | Web, LP, Photo |
| **Sticky Sidebar** | 메인 스크롤에 따라가는 사이드바 | Web, Blog, EC |

---

## Forms & Input (17)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Text Field** | 1줄 텍스트 입력. 라벨+플레이스홀더+검증 상태 | Form, Basic |
| **Textarea** | 여러 줄 텍스트 입력 | Form, Basic |
| **Select / Dropdown** | 선택지 목록에서 1개 선택 | Form, Basic |
| **Checkbox** | 복수 선택 가능한 체크 UI | Form, Basic |
| **Radio Button** | 배타적 단일 선택 | Form, Basic |
| **Toggle Switch** | ON/OFF 즉시 반영 스위치 | Form, Mobile, Settings |
| **Slider / Range** | 드래그로 수치 연속 선택 | Form, Filter |
| **Date Picker** | 캘린더에서 날짜 선택 | Form, Booking |
| **File Upload** | 파일 선택 또는 드래그&드롭 | Form, Web |
| **Search Bar** | 키워드 입력 검색 | Basic, Web, Mobile |
| **Autocomplete** | 입력에 따라 후보 자동 표시 | Form, Search |
| **Tag Input** | 칩 형태로 태그 추가/삭제 | Form, Tag |
| **OTP Input** | 1문자씩 분리된 핀 코드 입력 | Form, Auth, Security |
| **Password Strength Meter** | 비밀번호 강도 실시간 표시 | Form, Security |
| **Color Picker** | 색상 시각적 선택 | Form, Design Tool |
| **Inline Edit** | 텍스트 클릭→편집 모드 전환 | Form, Advanced |
| **Multi-step Form** | 긴 폼을 단계별 분할 | Form, UX |

---

## Data Display (13)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Table** | 행/열 구조화 데이터. 정렬/필터 포함 | Data, Admin |
| **List View** | 데이터를 수직 리스트로 표시 | Data, Basic, Mobile |
| **Tree View** | 계층 데이터를 접기/펼치기 트리로 | Data, Hierarchy |
| **Timeline** | 시간축 따라 이벤트 표시 | Data, History |
| **Kanban Board** | 카드를 컬럼 간 드래그 이동 | Task, Project |
| **Stat Card** | 숫자 지표를 크게 강조하는 카드 | Dashboard, Data |
| **Badge** | 아이콘 모서리의 작은 알림 마크 | UI Part, Notification |
| **Tag / Chip** | 카테고리/상태를 작은 라벨로 표현 | UI Part, Category |
| **Avatar** | 프로필 이미지/이니셜 원형 표시 | UI Part, User |
| **Progress Bar** | 진행률 횡 막대 표시 | UI Part, Progress |
| **Skeleton Screen** | 로딩 중 레이아웃 골격 플레이스홀더 | Loading, UX |
| **Empty State** | 데이터 없을 때 안내+CTA | UX, State |
| **Chart / Graph** | 데이터 시각화 (선/막대/원) | Data, Dashboard |

---

## Feedback (8)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Toast / Snackbar** | 일시적 메시지, 자동 사라짐 | Notification, Lightweight |
| **Modal / Dialog** | 배경 딤+전면 콘텐츠. 주목 강제 | Overlay, Critical |
| **Alert / Banner** | 상단 고정 중요 알림 | Notification, Important |
| **Tooltip** | 호버/포커스 시 보조 정보 팝업 | Help, Micro-interaction |
| **Popover** | 클릭 트리거 리치 플로팅 UI | Overlay, Info |
| **Loading Spinner** | 처리 중 회전 애니메이션 | Loading, Basic |
| **Confirmation Dialog** | 파괴적 작업 전 확인 요청 | Safety, Confirm |
| **Notification Panel** | 알림 목록 드롭다운 | Notification, Overlay |

---

## Content (9)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Accordion** | 클릭으로 내용 펼침/접음 | Content, FAQ |
| **Carousel / Slider** | 좌우 스와이프/클릭으로 콘텐츠 전환 | Content, Image, Mobile |
| **Lightbox** | 이미지 풀스크린 오버레이 확대 | Image, Overlay |
| **Pricing Table** | 요금제 횡 비교 테이블 | Marketing, LP, SaaS |
| **Testimonial** | 사용자 후기/추천문 표시 | Marketing, LP, Trust |
| **CTA Section** | 행동 유도 대형 버튼+메시지 섹션 | Marketing, LP, Conversion |
| **FAQ Section** | 자주 묻는 질문+답변 모음 | Support, LP |
| **Feature Section** | 기능을 아이콘+텍스트 그리드로 | LP, Marketing |
| **Comparison Table** | 옵션별 기능 비교표 | Marketing, Decision |

---

## Actions (8)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Button** | 클릭으로 액션 실행. Primary/Secondary/Ghost 등 | Basic, Form |
| **FAB** | 화면 위 떠있는 원형 메인 액션 버튼 | Mobile, Material Design |
| **Context Menu** | 우클릭 액션 메뉴 | Desktop, Operation |
| **Action Sheet** | 하단에서 올라오는 모바일 액션 선택 | Mobile, iOS |
| **Split Button** | 메인 액션 + 드롭다운 추가 액션 조합 | Desktop, Advanced |
| **Button Group** | 관련 버튼 횡 결합 표시 | UI Part, Basic |
| **Swipe Actions** | 리스트 항목 좌우 스와이프 액션 | Mobile, Gesture |
| **Pull to Refresh** | 화면 당겨서 새로고침 | Mobile, Gesture |

---

## Mobile (4)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Bottom Sheet** | 하단에서 올라오는 반모달 패널 | Mobile, Overlay |
| **Stories** | 상단 원형 아이콘 행. 탭→풀스크린 콘텐츠 | SNS, Video |
| **App Bar** | 앱 상단 타이틀 바. 뒤로+타이틀+액션 | Mobile, Navigation |
| **Speed Dial** | FAB 탭→서브 액션 부채꼴 펼침 | Mobile, Material Design |

---

## Social & Communication (5)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Chat UI** | 메시지 좌우 배치 채팅 형식 | Message, Realtime |
| **Comment Thread** | 중첩 댓글+답글 스레드 | Community, Comment |
| **Emoji Reactions** | 콘텐츠에 이모지로 반응 | Social, Micro-interaction |
| **Feed Card** | SNS 피드 포스트 카드 | SNS, Feed |
| **@Mention** | @입력 시 유저 후보 서제스트 | Social, Input Assist |

---

## Onboarding & Guidance (3)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Walkthrough** | UI 요소 하이라이트+단계별 안내 오버레이 | Onboarding, Tutorial |
| **Welcome Screen** | 앱 첫 실행 스와이프 인트로 화면 | Onboarding, Mobile |
| **Progress Checklist** | 셋업 완료도 체크리스트+다음 액션 유도 | Onboarding, Gamification |

---

## Media (3)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Video Player** | 영상 재생 UI. 재생/시크/음량/전체화면 | Media, Video |
| **Audio Player** | 음성 재생 UI. 재생/파형/프로그레스 | Media, Audio |
| **Image Gallery** | 이미지 그리드/슬라이드. 탭→확대 | Image, Media |

---

## Commerce (3)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Product Card** | 상품 이미지+이름+가격+레이팅 | EC, Product |
| **Shopping Cart** | 선택 상품+수량+소계+결제 진행 | EC, Checkout |
| **Rating / Review** | 별/점수로 평가 표시/입력 | EC, Feedback |

---

## Advanced Patterns (6)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Dark Mode Toggle** | 라이트/다크 테마 전환 | Accessibility, Settings |
| **Drag & Drop** | 드래그로 요소 재배치/이동 | Interaction, Advanced |
| **Virtual Scroll** | 보이는 부분만 DOM 렌더링 (대량 데이터) | Performance, Data |
| **Responsive Breakpoints** | 화면 폭에 따른 레이아웃 변화 | Responsive, Basic, CSS |
| **Micro-interactions** | 호버/클릭/전환 시 작은 애니메이션 | Animation, UX |
| **Keyboard Shortcuts** | 단축키 목록 오버레이 | Accessibility, Power User |

---

## Authentication (2)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **Login Form** | 이메일/비밀번호 로그인+소셜 버튼 | Auth, Form |
| **Sign Up Form** | 계정 생성 폼 | Auth, Form |

---

## Error & System (4)

| 패턴 | 설명 | 태그 |
|-----|------|-----|
| **404 Page** | 페이지 없음 에러 화면 | Error, Web |
| **Error State** | 작업 실패 상태+복구 액션 안내 | Error, UX |
| **Maintenance Page** | 시스템 점검 중 안내 페이지 | System, Web |
| **Cookie Banner** | 쿠키 동의 요청 GDPR 배너 | Legal, Web |

---

## 동의어 매핑

혼동하기 쉬운 용어들:

| 표준 명칭 | 동의어 |
|----------|-------|
| Hamburger Menu | Side Drawer, Slide-out Menu, Nav Drawer |
| Bottom Sheet | Modal Sheet, Half Sheet, Peek Card |
| Toast | Snackbar, Notification Toast |
| Drawer | Side Panel, Slide Panel |
| FAB | Floating Action Button |
| Stepper | Wizard, Multi-step, Progress Steps |
| Segmented Control | Button Group Toggle, Pill Toggle |
| Skeleton Screen | Placeholder, Content Loader, Shimmer |
| Command Palette | Spotlight, Quick Actions, ⌘K Menu |
| Tag / Chip | Label, Badge (맥락에 따라) |
