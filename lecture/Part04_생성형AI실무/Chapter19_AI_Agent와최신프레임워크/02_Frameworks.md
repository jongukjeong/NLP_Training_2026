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
