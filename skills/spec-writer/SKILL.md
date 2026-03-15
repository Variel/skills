---
name: spec-writer
description: Guide for writing effective specifications. This skill should be used when users want to write a new specification or update an existing specification.
---

## 스펙 작성 절차

### 1. 니즈 정렬 및 현황 파악

1. 사용자 요청을 바탕으로 사용자가 해결하고자 하는 **문제(Problem)**, 그 **배경(Context)**, 그리고 **성공 기준(Success Criteria)**(왜/무엇이 달라져야 하는지)을 추출해 핵심 니즈를 정의합니다.  
   단순 기능 정의가 아니라 “무엇이 달라져야 성공인가”를 명확히 합니다.

2. 사용자의 요청안이 문제 해결에 충분하지 않거나 더 나은 해결책이 있는 경우 **대안 스펙 옵션(Spec Options)**으로 제안합니다.
   - 각 옵션마다 기대 효과 / 비용 / 리스크 / 트레이드오프를 명시합니다.
   - 옵션 제안은 사용자의 목표를 바꾸기 위한 것이 아니라 목표 달성 확률을 높이기 위한 것이어야 합니다.

3. 스펙을 정확히 쓰기 위해 필요한 도메인/시스템 이해는 서브에이전트를 통해 수집합니다.
   - 수집 대상은 “코드”가 아니라 다음과 같은 **현황 중심 정보**입니다.
     - 현재 동작(As-Is Behavior)
     - 제약(Constraints)
     - 인터페이스/계약(Contracts)
     - 의존성(Dependencies)
     - 실패 케이스(Failure Modes)
   - 또한 도메인 지식, 유사 시스템 패턴, 유사 솔루션 사례 등 인터넷을 통해 습득 가능한 지식도 포함합니다.
   - 중요한 판단에 영향을 주는 정보는 가능하면 “근거가 무엇인지(관찰/문서/로그 등)”를 함께 남깁니다.

4. 사용자와 스펙을 합의하기 전까지 다음 항목들을 반복 정렬합니다.
   - 용어 정의(Glossary) 정렬
   - 요구사항 Commitment Level 정렬
     - **Committed**: 이번에 반드시 할 것
     - **Planned**: 앞으로 반드시 할 예정인 것
     - **Candidate**: 앞으로 할 수도 있는 것
     - **Never**: 앞으로도 절대 하지 않을 것
   - 경계 조건 / 예외 케이스 처리 기준
   - 수용 기준(AC)으로 검증 가능하게 만들기
   - 불확실한 항목은 숨기지 않고, **가정(Assumption)** 또는 **미해결 질문(Open Question)**으로 분리합니다.

### 2. 상위 스펙 작성

상위 스펙은 다음 두 가지 역할을 가지고 있습니다:

1. 사용자가 읽고 작업의 목표와 방향성을 파악할 수 있도록 하며, 정렬에 대한 피드백을 제공할 수 있도록 하는 역할.
2. 상세 스펙 작성을 위한 틀을 제공하는 역할.

상위 스펙은 사용자의 문제를 해결할 수 있는 핵심 플로우를 중심으로 작성하며, 대표적인 유즈케이스들을 모두 커버할 수 있도록 작성합니다.
사용자와 합의 된 내용을 바탕으로 상위 스펙을 작성합니다.

상위 스펙에는 구체적인 소스코드나 구현 세부사항을 넣지 않고, 인터페이스와 데이터 형식 등을 최소화 하며, 대신 다음을 명확히 합니다.

- 각 요구사항이 목표에 어떻게 기여하는지(Traceability)
- 각 요구사항의 “완료 판정” 방법(AC/검증)
- 범위 경계와 예외 케이스, 예외 처리 기준

#### 상위 스펙 작성 형식

- 한 줄 요약 (Outcome Statement)
  - “누가 / 무엇을 / 왜 / 어떤 상태로 만든다”
- 문제 정의 & 배경 (Problem & Context)
  - 현 상태(As-Is)
  - 사용자가 겪는 Pain Point
  - 왜 지금 필요한지(우선순위 근거)
- 목표 (Goals) & 성공 지표 (Success Metrics)
  - 성공을 판단할 정량/정성 기준
  - “완료”의 정의(Definition of Done)
- 스펙 안정성 분류 (Spec Stability Classification)
  - **Stable**: 변경 가능성 낮음 (변경 시 사용자 재정렬 필요)
  - **Flexible**: 목표/AC를 해치지 않는 범위에서 조정 가능
  - **Experimental**: 검증 필요 (중단 조건/판정 기준을 명시)
- 용어 정의 (Glossary)
- 요구사항 (Requirements)
  - 기능 요구사항(FR): **Committed / Planned / Candidate / Never**를 명시합니다.
  - 비기능 요구사항(NFR): 성능, 안정성, 보안/프라이버시, 운영, 비용, 접근성 등  
    비기능 요구사항도 반드시 사용자와 합의하여 정의합니다.
- 수용 기준 (Acceptance Criteria)
  - "Given / When / Then" 형식으로 작성합니다.
  - 테스트 가능하고 모호하지 않게 작성합니다.
  - 주요 사용자 플로우 + 엣지 케이스 포함
- 범위 경계 (Non-goals)
  - 하면 안 되는 것(명시적으로 금지)
  - 할 수도 있지만 이번 범위 밖(차기 후보)
- 제약 & 가정 (Constraints & Assumptions)
  - 기술/정책/시간/조직적 제약을 명시합니다.
  - 외부 의존성(3rd party, 다른 팀, 릴리즈 정책)
- 리스크 & 완화책 (Risk Ledger)
  - 발생 가능성 / 임팩트 / 완화 / 조기 신호(Early Warning Signal)
- 검증 계획 (Verification Plan)
  - AC를 어떻게 검증할지(테스트, 로그, 모니터링, QA 시나리오)
  - “무엇을 보면 성공이라고 말할 수 있는지”까지 포함

#### 상위 스펙 Freeze 조건

상위 스펙이 Freeze(합의 완료)되기 전까지 상세 스펙 작성 단계로 넘어가지 않습니다.

- Freeze는 “변경 금지”가 아니라, **무단 변경 금지**입니다.
- Freeze 이후 변경이 필요하면 변경 사유와 영향 범위를 정리하고 사용자와 재정렬합니다.
- 변경은 다음 두 가지로 구분합니다.
  - **Stable 항목 변경**: 반드시 사용자 재합의 후 진행합니다.
  - **Flexible 항목 조정**: 목표 및 AC를 침범하지 않는 범위에서는 진행 가능하나, 변경 사유와 영향 범위를 SPEC.md에 기록합니다.
- Experimental 항목은 사전에 정의된 성공/중단 기준에 따라 유지 또는 중단 여부를 판단합니다.

### 3. 상세 스펙 작성

상세 스펙은 상위 스펙을 기준으로, **실행 가능한 단위로 분해하여 파일 단위로 작성**합니다.  
상세 스펙의 목적은 구현 이전에 요구사항을 충분히 고정하고, 에이전트가 임의 해석 없이 작업할 수 있도록 계약과 경계를 명확히 하는 것입니다.

상세 스펙은 다음 네 가지 관점으로 구성됩니다:

- **A. Behavior Spec (행동 명세)**
- **B. Constraint Spec (제약 명세)**
- **C. Interface Spec (표면/계약 명세)**
- **D. Realization Spec (구현 전략 명세)**

이 네 가지는 “섹션 종류”이지, 파일을 네 개로 나누라는 의미는 아닙니다.  
각 상세 스펙 파일은 하나의 논리적 단위를 다루며, 그 내부에 A/B/C/D 네 섹션을 모두 포함합니다.

#### 3.1 상세 스펙 파일 분할 기준

상세 스펙은 다음 기준 중 하나 이상을 만족할 때 **새 파일로 분리**합니다.

##### 3.1.1. 책임 경계가 분리되는 경우 (Responsibility Boundary)

- 독립적으로 구현/테스트/배포 가능
- 다른 팀/시스템과 계약을 맺는 지점
- 데이터 소유권이 분리되는 지점

예:

- `auction-creation`
- `bid-submission`
- `payment-processing`

##### 3.1.2. 상태 모델이 분리되는 경우 (State Boundary)

- 별도의 상태 전이(State Machine)를 가짐
- 수명주기(Lifecycle)가 독립적임

##### 3.1.3. 외부 계약이 분리되는 경우 (Interface Boundary)

- 별도 API 엔드포인트
- 별도 CLI 명령어
- 별도 이벤트 스키마
- 별도 화면 단위(View/Route)

##### 3.1.4. 리스크 또는 제약이 강하게 분리되는 경우

- 보안/결제/인증 등 고위험 영역
- 성능 요구사항이 다른 영역과 현저히 다름

##### 3.1.5. 분할 원칙

- 하나의 상세 스펙 파일은 **하나의 명확한 책임 단위**를 다룬다.
- 파일 하나에 여러 독립적 책임을 섞지 않는다.
- 지나치게 미세하게 쪼개지 않는다. (구현 파일 단위와 동일하게 쪼개지 않음)
- 파일 간 Forward Dependency는 금지한다.
  - 상위 스펙에 정의되지 않은 계약에 의존하면 안 된다.

#### 3.2. 폴더 구조 규칙 및 정리 원칙

```
/spec
  OVERVIEW.md # 상위 스펙
  /auction
    auction-creation.md
    bid-submission.md
  /payment
    payment-processing.md
```

- 폴더는 “도메인 또는 기능 영역” 기준으로 구성한다.
- 파일은 “구현 단위가 아니라 책임 단위” 기준으로 구성한다.
- 상세 스펙 파일은 서로 독립적으로 읽어도 이해 가능해야 한다.
- 모든 상세 스펙 파일은 상위 스펙의 특정 Requirement ID와 연결되어야 한다.

#### 3.3. Flow 정의 (Behavior Specification)

상세 스펙에서 사용하는 **Flow**는 다음을 의미합니다.

> Flow는 “하나의 명확한 Trigger로 시작하여,
> 시스템 상태 변화를 일으키고,
> 하나의 의미 있는 결과로 종료되는 행동 단위”입니다.

Flow는 UI 화면 흐름을 의미하지 않습니다.  
CLI 명령 실행, API 호출, 이벤트 수신, 스케줄 작업 등
모든 행위 트리거를 포함합니다.

Flow는 반드시 다음 조건을 만족해야 합니다:

- 단일 Trigger로 시작한다.
- 명확한 종료 조건을 가진다.
- 하나 이상의 상태 변화 또는 외부 관측 가능한 결과를 만든다.
- 실패 시나리오가 정의 가능하다.

Flow는 상세 스펙 파일 내부의 Behavior를 구성하는 최소 행동 단위입니다.

Flow ID는 다음 형식을 따릅니다:

<DOMAIN>-<UNIT>-<SEQUENCE>

예:

- AUCTION-CREATE-01
- BID-SUBMIT-01
- PAYMENT-CONFIRM-01

Flow ID는 파일 간 충돌하지 않도록 전역적으로 유니크해야 합니다.

#### 3.4. 상세 스펙 파일 내부 구조

각 상세 스펙 파일은 다음 구조를 반드시 따른다.

```markdown
# [파일명]

## 1. 한 줄 요약 (Outcome Statement)

“누가 / 무엇을 / 왜 / 어떤 상태로 만든다”

---

## 2. 상위 스펙 연결 (Traceability)

- Related Goals:
- Related Requirements (FR/NFR ID):
- Related AC:

---

## 3. Behavior Specification

이 파일이 다루는 책임 단위의 모든 행동을 정의합니다.

Behavior는 하나 이상의 **Flow**로 구성됩니다.
각 Flow는 독립적으로 식별 가능하며, 고유한 Flow ID를 가집니다.

Flow는 UI 흐름이 아니라, 시스템의 “행동 단위”입니다.

### 3.1 Flow 목록

각 Flow는 반드시 ID를 가집니다.

#### Flow ID: AUCTION-CREATE-01

- Actor:
- Trigger:
- Preconditions:
- Main Flow:
- Alternative Flow:
- Outputs:
- Side Effects:
- Failure Modes:
- State Transition (Optional):

> Behavior는 “무엇이 일어나야 하는가”만 정의합니다.
> “어떻게 구현하는가”는 여기 쓰지 않습니다.

---

## 4. Constraint Specification

이 파일의 책임 단위에 적용되는 제약을 정의합니다.

### Constraint ID: PERF-001

- Category:
- Description:
- Scope: (Flow ID 또는 전체)
- Measurement:
- Verification:
- Related Behavior:

> 전역 제약은 상위 스펙에 두고,
> 이 단위에 특화된 제약만 여기 작성합니다.

---

## 5. Interface Specification

외부에 노출되는 모든 계약을 정의합니다.

필요한 유형만 작성합니다.

### 5.1 GUI Interface (해당 시)

- View ID:
- User Actions:
- UI States:
- Error Presentation:
- Related Flow:

### 5.2 CLI Interface (해당 시)

- Command:
- Flags:
- Output Format:
- Exit Codes:
- Related Flow:

### 5.3 API Contract (해당 시)

- Endpoint:
- Method:
- Auth:
- Request Schema:
- Response Schema:
- Status Codes:
- Error Schema:
- Idempotency:
- Related Flow:

> Interface는 표현이 아니라 계약입니다.
> 시각적 스타일은 목표/AC와 연결될 때만 구체화합니다.

---

## 6. Realization Specification

Behavior와 Constraint를 만족시키기 위한 설계 전략을 정의합니다.

- Module Boundaries:
- Data Ownership:
- State Model:
- Concurrency Strategy:
- Failure Handling:
- Deployment Location:
- Observability Plan:
- Migration / Rollback:

> 소스코드는 작성하지 않습니다.
> 그러나 구현자가 임의 설계를 하지 않도록 충분히 구체적이어야 합니다.

---

## 7. Dependency Map

- Depends On:
- Blocks:
- Parallelizable With:

> 정의되지 않은 계약에 의존하는 Forward Dependency는 금지합니다.

---

## 8. Acceptance Criteria

- Given / When / Then 형식
- 주요 플로우 + 엣지 케이스 포함
- Constraint 위반 케이스 포함
```

#### 3.5. A/B/C/D 활용 원칙

A/B/C/D는 파일을 나누는 기준이 아니라,  
각 파일 내부에서 반드시 작성해야 하는 “관점 체크리스트”입니다.

- A (Behavior): 이 단위에서 어떤 변화가 발생하는가?
- B (Constraint): 이 단위에서 무엇이 절대 깨지면 안 되는가?
- C (Interface): 외부와의 계약은 무엇인가?
- D (Realization): 이걸 어떤 전략으로 만족시킬 것인가?

에이전트는 A를 먼저 작성하고,
B로 A를 제한하며,
C로 외부 계약을 고정하고,
D로 실행 전략을 설계합니다.

순서를 어기지 않습니다.

#### 3.6. 상세 스펙 Freeze 규칙

- 모든 상세 스펙 파일이 상위 스펙과 Traceability를 갖기 전까지 Freeze하지 않습니다.
- 파일 간 의존관계가 명확히 정리되기 전까지 실행 단계로 넘어가지 않습니다.
- Stable 항목 변경은 사용자 재합의 후 진행합니다.
- Flexible 항목은 AC를 침범하지 않는 범위에서 조정 가능하나 변경 로그를 남깁니다.
- Experimental 항목은 사전 정의된 성공/중단 기준에 따라 유지 여부를 판단합니다.
