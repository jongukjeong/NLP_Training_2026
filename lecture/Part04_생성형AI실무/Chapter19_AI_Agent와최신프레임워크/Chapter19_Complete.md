# Chapter 19 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 19. AI Agent와 최신 프레임워크

1. [Function Calling·Tool Calling·MCP](01_Tools_and_MCP.md)
2. [LangChain·LangGraph와 설계](02_Frameworks.md)
3. [안전과 평가](03_Safety_and_Evaluation.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: AI Assistant](05_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 19 원리·수학·실습 가이드

## 1. Agent의 실행 루프

Agent는 모델이 답만 생성하는 것을 넘어 목표를 위해 도구를 선택하고 결과를 관찰해 다음 행동을 정한다.

`사용자 요청 → 계획/라우팅 → 도구 호출 → 결과 검증 → 응답 또는 다음 호출`

Function/Tool Calling에서 모델은 함수명과 인자를 구조화해 제안하고, 실제 실행·권한 검증·재시도는 애플리케이션이 책임진다.

## 2. 신뢰성과 비용

각 단계 성공확률이 `p`이고 독립이라고 단순화하면 n단계 전체 성공률은 `p^n`이다. 단계당 0.95라도 10단계면 `0.95^10≈0.60`이다. 불필요한 단계 축소, 각 결과 검증, 재시도 한도가 중요하다.

\[
ExpectedCost=\sum_i P(step_i\ reached)\times Cost_i
\]

지연도 모델 호출과 도구 호출의 합이므로 병렬 가능한 읽기 작업, 캐시, 종료 조건을 설계한다.

## 3. MCP와 프레임워크

MCP는 모델 애플리케이션과 외부 도구·리소스를 연결하는 공통 규약이다. 도구 설명과 입력 스키마는 짧고 구체적으로 만들며 최소 권한을 적용한다. LangChain은 구성요소 조합, LangGraph는 상태·분기·재개가 필요한 워크플로 표현에 유용하다. 단순 한두 번 호출이면 프레임워크 없이 구현하는 편이 명확할 수 있다.

## 4. 안전 설계

- 읽기와 쓰기 도구를 구분하고 외부 전송·삭제·결제는 확인을 받는다.
- 도구 인자를 schema로 검증하고 경로·도메인 allowlist를 둔다.
- 웹·문서의 명령을 신뢰된 시스템 지시로 취급하지 않는다.
- 최대 단계, 시간, 비용, 재시도 한도를 둔다.
- 호출 ID, 입력 요약, 결과, 오류, 승인자를 감사 로그로 남긴다.

평가는 task success, 잘못된 도구 선택률, 인자 오류율, 평균 단계, P95 지연, 비용, 안전 위반률로 한다.

1. 단계가 길수록 전체 성공률이 낮아지는 이유는?
2. MCP와 LangGraph의 역할 차이는?
3. 어떤 도구 호출에 사람 승인이 필요한가?

---

<!-- SOURCE: 01_Tools_and_MCP.md -->

# 19.1 Function Calling · 19.2 Tool Calling · 19.3 MCP

Tool Calling에서 모델은 실행할 함수와 인수를 제안하지만 실제 실행·권한·검증 책임은 애플리케이션에 있습니다.

```text
사용자 요청 → 모델 tool call → schema 검증 → 권한 확인
→ 실제 함수 실행 → 결과를 모델/사용자에게 반환
```

읽기와 쓰기 tool을 구분하고 결제·삭제·전송 같은 부작용에는 명시적 사용자 확인, idempotency key, audit log를 적용합니다.

MCP는 AI 애플리케이션과 외부 시스템 연결을 표준화합니다.

- Prompts: 사용자가 선택하는 템플릿
- Resources: 애플리케이션이 context로 관리하는 데이터
- Tools: 모델이 호출을 선택할 수 있는 실행 기능

MCP 연결 자체가 신뢰를 보장하지 않습니다. server 출처, tool schema, 인증·권한과 반환 데이터를 검증합니다.

## Agent와 일반 챗봇의 차이

일반 챗봇은 주로 텍스트 답을 만들고, Agent는 목표를 위해 도구를 선택하고 실행 결과를 관찰한 뒤 다음 행동을 정합니다. 모델은 도구 호출을 “제안”하며 실제 권한 확인과 실행은 애플리케이션 책임입니다.

## Tool schema가 중요한 이유

```json
{
  "name": "get_order",
  "arguments": {"order_id": "A-1004"}
}
```

함수 설명이 모호하면 잘못된 도구를 선택하고, 인자 타입이 느슨하면 실행 오류가 납니다. 필수값, 형식, 허용 범위를 schema로 검증합니다.

## 단계가 길어질 때의 신뢰도

각 단계 성공확률이 0.95라고 단순 가정하면 10단계 전체 성공확률은 다음과 같습니다.

\[
0.95^{10}\approx0.60
\]

각 단계가 꽤 정확해 보여도 긴 연쇄의 전체 성공률은 빠르게 낮아집니다. 불필요한 호출을 줄이고 매 단계 결과를 검사해야 합니다.

## MCP의 쉬운 역할

MCP는 서로 다른 AI 애플리케이션과 도구 제공자가 공통 방식으로 도구·리소스·프롬프트를 설명하고 연결하도록 돕는 규약입니다. MCP 자체가 Agent의 계획 알고리즘이나 업무 프레임워크는 아닙니다.

## 읽기와 쓰기 권한

조회는 자동 실행할 수 있어도 메일 전송, 결제, 삭제, 외부 공개는 사용자 확인을 받아야 합니다. 최소 권한, allowlist, 최대 단계, timeout, 비용 한도와 감사 로그를 둡니다.

## 평가 지표

최종 task success 외에 도구 선택 정확도, 인자 오류율, 평균 호출 수, 재시도율, P95 지연, 비용, 승인 없는 쓰기 시도를 측정합니다.

---

<!-- SOURCE: 02_Frameworks.md -->

# 19.4 LangChain · 19.5 LangGraph

LangChain은 model, retriever, tool과 agent의 통합·고수준 추상화를 제공합니다. LangGraph는 state, node, edge로 장기 실행·상태 기반 workflow를 제어하는 저수준 orchestration에 초점을 둡니다.

선택 기준:

- 단순 RAG chain: 직접 코드 또는 LangChain
- 일반 tool-calling loop: 고수준 agent 검토
- 분기·재시도·checkpoint·human-in-the-loop: LangGraph 검토
- 작은 deterministic workflow: framework 없이 명시적 함수가 더 단순할 수 있음

Framework는 품질을 자동 보장하지 않습니다. 버전 변화가 빠르므로 핵심 domain logic과 평가를 framework API에서 분리합니다.

## Chain과 Agent 구분

Chain은 실행 순서가 개발자에 의해 거의 고정되고, Agent는 모델이 상태에 따라 다음 도구를 선택합니다. 정해진 `검색→요약→저장`이면 chain이 단순하고, 요청마다 필요한 도구가 달라지면 agent가 적합할 수 있습니다.

## 상태에 무엇을 저장할까

LangGraph 같은 상태 그래프에서 상태에는 사용자 요청, 현재 단계, 도구 결과 요약, 오류 횟수, 승인 여부를 저장할 수 있습니다. 전체 원문을 무제한 누적하면 메모리와 개인정보 위험이 커집니다.

## Middleware의 쉬운 의미

Middleware는 모델이나 도구 호출 전후에 공통 처리를 끼우는 층입니다.

```text
요청 → 인증/PII 마스킹 → 모델 호출 → 출력 검사 → 응답
                  ↘ 재시도·timeout·로그 ↗
```

- 컨텍스트 관리: 오래된 메시지를 요약하거나 제거
- 호출 제한: 단계·토큰·비용 한도
- 복원력: timeout과 제한된 재시도
- 도구 최적화: 현재 상황에 필요한 도구만 노출

## Guardrail

Guardrail은 입력·출력·도구 실행이 정한 정책을 지키는지 검사합니다. 프롬프트 문장 하나가 아니라 schema validation, 권한 검사, 금지 작업 차단, 개인정보 탐지, 사람 승인 같은 여러 층으로 구성합니다.

## Human-in-the-Loop

사람 검토를 모든 단계에 넣으면 자동화 이점이 사라지고, 전혀 넣지 않으면 고위험 쓰기가 실행될 수 있습니다. 결제, 삭제, 외부 전송, 권한 변경처럼 되돌리기 어렵거나 영향이 큰 행동 직전에 승인을 요청합니다.

승인 화면에는 사용 목적, 실행할 도구, 핵심 인자, 예상 영향이 보여야 합니다. “계속할까요?”만으로는 충분한 판단 정보를 주지 못합니다.

## Multi-Agent 판단

여러 agent는 역할 분리와 병렬 작업에 도움이 될 수 있지만 호출 횟수, 상태 동기화, 오류 지점이 늘어납니다. 단일 agent와 명시적 도구만으로 해결되는 문제에는 멀티 agent를 사용하지 않습니다.

Router는 입력을 전문 agent로 보내고, handoff는 한 agent가 다른 agent에게 제어권과 필요한 문맥을 넘깁니다. 전달 문맥의 범위와 최종 책임 주체를 명확히 합니다.

---

<!-- SOURCE: 03_Safety_and_Evaluation.md -->

# Agent 안전과 평가

최소 권한 원칙으로 tool별 읽기/쓰기 scope, 허용 resource, timeout과 호출 횟수를 제한합니다.

필수 평가:

- 올바른 tool 선택률
- argument schema 정확도
- 불필요한 tool 호출률
- 권한 없는 요청 거부율
- loop/재시도 상한
- 최종 답변 정확도와 출처
- latency·비용·실패 복구

Prompt injection, tool output injection과 데이터 exfiltration을 위협 모델에 포함합니다. 중요한 쓰기는 모델이 바로 실행하지 않고 계획 표시 → 사용자 확인 → 실행 → 결과 검증 단계를 둡니다.

---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 요약과 퀴즈

1. 모델이 tool call을 제안하면 자동 실행해야 하나요? **아니요**
2. 쓰기 tool에 필요한 추가 절차는? **권한·사용자 확인·감사 로그**
3. MCP의 세 primitive는? **Prompts, Resources, Tools**
4. 복잡한 stateful workflow에 적합한 것은? **LangGraph**
5. Framework가 품질을 자동 보장하나요? **아니요**
6. Agent loop에 상한이 필요한 이유는? **무한 반복·비용·부작용 방지**
7. Tool output도 신뢰할 수 없는 입력인가요? **예**

---

<!-- SOURCE: 05_Practice.md -->

# 실습: AI Assistant 제작

FAQ 검색과 주문 상태 조회 tool을 가진 deterministic assistant를 구현합니다. 외부 API 없이 tool routing·schema·audit log를 학습합니다.

- [안내](examples/05_ai_assistant_solution/README.md)
- [코드](examples/05_ai_assistant_solution/ai_assistant.py)
- [FAQ](examples/05_ai_assistant_solution/faq.csv)
- [주문 데이터](examples/05_ai_assistant_solution/orders.csv)

