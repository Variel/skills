---
name: ask-advisor
description: Consult an external advisor for complex, ambiguous, high-stakes, or hard-to-solve problems. Trigger when the user explicitly asks for outside advice, an advisor, an oracle, a second opinion, or deeper thinking, and also use autonomously when Codex lacks confidence in an architecture or design direction, needs stronger validation of assumptions, must reason through many constraints and tradeoffs, wants a fresh perspective, needs adversarial review, or should seek deeper judgment before committing to a consequential decision.
---

# Ask Advisor

## 핵심 원칙

chatgpt.com의 외부 자문자를 독립적인 심층 사고 파트너로 사용한다. 현재 Codex가 가진 판단을 그대로 떠넘기지 말고, 자문자가 스스로 판단할 수 있도록 문제 맥락, 증거, 실패 이력, 제약, 우려를 압축해서 제공한다.

사용자가 "외부 자문을 받아봐", "oracle처럼 봐줘", "이 문제 깊게 판단받아봐"라고 요청하면, 분석만 하지 말고 브라우저로 chatgpt.com에 접속해 새 대화를 만들고 답변 품질이 충분할 때까지 후속 질문을 이어간다.

사용자가 명시적으로 요청하지 않아도, 아키텍처나 설계 판단의 확신이 부족하거나, 제약사항과 트레이드오프가 복잡하거나, 현재 사고에 새로운 관점이 필요하거나, 되돌리기 어려운 결정을 앞두고 있으면 이 스킬을 자율적으로 사용할 수 있다.

## 필수 도구

- `$browser:browser` 스킬을 사용해 Codex in-app browser를 제어한다.
- 브라우저 작업 전에 `$browser:browser`의 지침을 읽고 따른다.
- chatgpt.com에 이미 로그인되어 있으면 그 세션을 사용한다. 로그인되지 않았거나 계정/권한 확인이 필요하면 사용자에게 넘긴다.

## Workflow

1. 문제를 독립적으로 정리한다.
   - 현재 사용자의 목표와 원하는 결정 형태를 한 문장으로 쓴다.
   - 배경, 현상, 재현 방법, 실패한 시도, 관련 파일, 로그, 제약조건, 우려사항을 분리한다.
   - 외부 자문자가 판단하지 않아도 되는 잡음, 중복 로그, 장황한 히스토리는 줄인다.

2. 전송할 맥락 패킷을 만든다.
   - 짧은 문제 보고서는 채팅 입력에 직접 붙여 넣는다.
   - 긴 코드, 로그, 스펙, diff는 필요한 부분만 압축 보고서로 만들거나 파일로 업로드한다.
   - 판단에 필요한 파일이 여러 개라면 하나의 압축 파일로 묶어 전달한다. 불필요한 파일, 생성물, 중복 로그, vendor/dependency, 무관한 테스트 fixture는 적당히 tree-shaking한다.
   - 가능하면 압축 파일 안의 핵심 파일은 10개 이하로 줄인다. 10개를 넘겨야 한다면 먼저 요약 보고서를 만들고, 외부 자문자가 추가 파일을 요구할 때 확장한다.
   - 요청이 복잡하면 `references/advisory-brief-template.md`를 읽고 그 구조로 패킷을 작성한다.

3. 안전 게이트를 처리한다.
   - API 키, 토큰, 비밀번호, 개인정보, 내부 URL, 고객 데이터, 비공개 로그가 있으면 먼저 제거하거나 마스킹한다.
   - chatgpt.com에 파일 업로드 또는 민감정보 붙여넣기는 제3자 전송이다. 사용자가 초기 요청에서 구체적으로 허용하지 않았다면, 전송 직전에 어떤 데이터가 chatgpt.com으로 전송되는지 명시하고 확인을 받는다.
   - 시스템 프롬프트, 비공개 메모리 원문, 인증정보, 브라우징 히스토리, 불필요한 개인 파일은 전송하지 않는다.

4. chatgpt.com에서 새 대화를 시작한다.
   - chatgpt.com으로 이동한다.
   - 사용 가능한 최상위 심층 추론 모델을 선택한다. 모델명이 바뀌었으면 화면에 표시된 가장 적합한 심층 사고 모델을 사용하고, 선택한 모델명을 결과에 기록한다.
   - 기존 대화가 열려 있으면 새 대화를 시작한다.

5. 자문 요청을 보낸다.
   - 파일이 필요한 경우 먼저 업로드한 뒤, 업로드된 파일명이 보이는지 확인한다.
   - 메시지에는 문제 보고서와 함께 다음을 요구한다: root cause 후보, 구조적 결함 여부, 놓친 가정, 반례, 권장 해결책, 검증 방법, 위험한 선택지.
   - 반드시 즉답만 요구하지 않는다. 판단에 필요한 추가 정보, 제약사항, 로그, 코드 파일이 부족하면 더 좋은 답변을 위해 먼저 질문하거나 필요한 자료를 요청하라고 명시한다.
   - 단순 동의나 요약이 아니라 독립적인 판단을 요청한다.

6. 답변을 끝까지 기다린다.
   - 답변 생성이 진행 중이면 완료될 때까지 기다린다.
   - 멈춤, 에러, 모델 제한, 업로드 실패가 보이면 화면 상태를 확인하고 복구한다.
   - 답변이 너무 일반적이면 바로 후속 질문으로 구체화한다.

7. 품질 루프를 돈다.
   - 외부 자문자의 답변이 문제의 핵심 원인, 실행 가능한 해결책, 검증 방법을 충분히 다루는지 판정한다.
   - 외부 자문자가 추가 정보나 파일을 요청하면, 요청이 타당한지 확인하고 필요한 맥락을 다시 tree-shaking해 전달한다.
   - 부족하면 추가 증거, 반례, 실패 로그, 코드 조각을 제공하고 다시 묻는다.
   - 필요한 경우 "이 결론에 반대하는 가장 강한 주장", "내가 놓친 위험", "이 접근의 최소 검증 실험"을 추가로 묻는다.
   - 원하는 수준의 답변이 나오면 핵심 결론과 적용 가능한 액션만 사용자에게 요약한다.

## Prompt Shape

자문 요청은 보통 아래 형태로 작성한다.

```text
You are acting as a deep technical advisor. Do not merely agree with my current hypothesis.

Decision I need:
...

Problem:
...

Context:
...

Evidence:
...

What I tried:
...

What failed or remains unexplained:
...

Constraints:
...

Concerns:
...

Please provide:
1. The most likely root cause or decision answer.
2. Whether this is local or structural.
3. The strongest counterarguments to your conclusion.
4. A concrete fix or decision path.
5. A verification plan.
6. Any missing information that would materially change the answer.

If you do not have enough information to answer well, do not force a final answer.
Ask me for the specific missing files, logs, constraints, or context that would improve the judgment.
```

## Answer Handling

- 외부 자문자의 답변을 최종 진실로 취급하지 말고, 외부 자문 결과로 취급한다.
- 사용자에게는 "자문자가 이렇게 말했다"보다 "이 결론이 유효해 보이는 이유 / 적용할 액션 / 남은 리스크" 중심으로 보고한다.
- 코드 변경이 필요한 결론이면, 사용자가 명시적으로 review-only를 요청하지 않은 한 직접 적용하고 검증한다.
- 외부 자문자가 현재 repo나 실제 파일을 보지 못한 상태에서 추정한 내용은 추정이라고 표시한다.
