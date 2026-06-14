# k-persona — 페르소나 샘플링 (번들 참조)


# Korean Persona Validation

## Overview

제품을 출시 전 검증할 때, 페르소나를 **지어내지 말고** `k-persona` CLI로 한국 인구통계(통계청 기반 합성 100만 명)에서 **실제 분포에 맞는 페르소나를 뽑아** 검증한다.

**핵심 원칙: 페르소나 1명 = 서브에이전트 1명.** 각 페르소나를 별도 서브에이전트에 주입해 *독립적으로* 반응하게 한다. 한 컨텍스트에서 여러 명을 동시에 연기하면 반응이 서로 오염되고 뭉뚱그려진다 — 그게 이 방식의 핵심을 무너뜨린다.

## When to Use

- 기능·카피·플로우·가격·온보딩을 **타깃 사용자 입장에서** 검증할 때
- 특정 세그먼트(예: 서울 30대 워킹맘, 지방 소도시 자영업자)의 현실적 반응이 필요할 때
- synthetic user research / 페르소나 패널 / 사용성 사전 점검
- **쓰지 말 것:** 비(非)한국 사용자 대상(데이터셋은 한국 한정), 실제 사용자 인터뷰가 필요한 경우

## Workflow

CLI는 `npx k-persona <command>`로 호출한다(설치 불필요). 최초 1회 `npx k-persona setup`으로 데이터셋을 받는다(`PERSONA_DATA_DIR`로 위치 지정 가능).

1. **어휘 확인** — 필터에 쓸 정확한 한국어 값을 본다. 지어내면 0건이 나온다.
   `npx k-persona fields` · `npx k-persona values <컬럼>` (예: `values education_level`)
2. **세그먼트 점검** — 패널을 뽑기 전 크기·분포를 확인(0명/너무 좁지 않은지).
   `npx k-persona stats --province 서울 --age 30-39 --by occupation`
3. **패널 샘플링** — `--seed`를 반드시 줘서 재현 가능하게. 양면 기능(예: 마켓플레이스)이면 공급·수요 양쪽을 패널에 넣는다.
   `npx k-persona sample --province 서울 --age 30-39 --sex 여자 -n 5 --seed panelA`
4. **서브에이전트 대입(핵심)** — 브리프 **1개당 서브에이전트 1명**을 띄우고, 그 브리프 + 검증 과제를 준다. 각자 그 인물로서만 반응한다. *직접 다 연기하지 말 것.*
5. **집계** — 반응을 모아 교차 시그널(공통 우려, 세그먼트 차이, 채택 블로커)을 뽑는다.

수정 후 재검증은 **같은 시드**로 같은 패널을 다시 띄우면 된다.

## Quick Reference

| 명령 | 용도 |
|---|---|
| `npx k-persona setup` | 데이터셋 다운로드(최초 1회) |
| `npx k-persona fields` | 필터 컬럼·테마 목록 |
| `npx k-persona values <컬럼>` | 컬럼의 실제 값(필터 어휘) |
| `npx k-persona stats [필터] --by <컬럼>` | 세그먼트 건수/분포 |
| `npx k-persona sample [필터] -n N --seed S` | 페르소나 N명 → role-play 브리프 |
| `npx k-persona get <uuid>` | 단건 조회 |

필터: `--sex --province --district --education --occupation --marital --family-type --housing --age 30-39 --match <키워드>`. 토큰 절약은 `--only <테마>`, 기계 처리는 `--format json`.

## Dispatch Pattern

`sample`이 낸 브리프를 그대로 서브에이전트 프롬프트에 넣는다:

```
[페르소나 브리프 전체 붙여넣기]

위 인물로서, 다음을 검증하세요: "<기능/카피/플로우>".
이 사람이 실제로 쓸지·안 쓸지, 우려, 기대를 1인칭으로 답하세요.
```

브리프는 끝에 "역할 지시"가 들어 있어 그대로 주입하면 인물 일관성이 유지된다.

## Common Mistakes

- **페르소나를 지어냄** → 인구통계 근거·재현성 상실. 항상 `sample`로 뽑는다.
- **한 컨텍스트에서 여러 명을 동시에 연기** → 반응 오염. 반드시 서브에이전트로 분리.
- **`--seed` 누락** → 수정 후 같은 패널로 재검증 불가.
- **양면 기능인데 한쪽만** → 공급·수요(발행자/수령자 등) 양쪽을 패널에 포함.
- **필터 값을 추측** → 0건. 먼저 `values <컬럼>`으로 확인.
