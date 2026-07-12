# Chapter 19. AI Agent와 최신 프레임워크 — 통합 원고

> 이 문서는 Chapter 19. AI Agent와 최신 프레임워크 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 19. AI Agent와 최신 프레임워크 — `README.md`
- 19.1 Function Calling · 19.2 Tool Calling · 19.3 MCP — `01_Tools_and_MCP.md`
- 19.4 LangChain · 19.5 LangGraph — `02_Frameworks.md`
- Agent 안전과 평가 — `03_Safety_and_Evaluation.md`
- 요약과 퀴즈 — `04_Summary_and_Quiz.md`
- 실습: AI Assistant 제작 — `05_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 19. AI Agent와 최신 프레임워크

# Chapter 19. AI Agent와 최신 프레임워크

1. [Function Calling·Tool Calling·MCP](01_Tools_and_MCP.md)
2. [LangChain·LangGraph와 설계](02_Frameworks.md)
3. [안전과 평가](03_Safety_and_Evaluation.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: AI Assistant](05_Practice.md)


---

<!-- SOURCE: 01_Tools_and_MCP.md -->

# 19.1 Function Calling · 19.2 Tool Calling · 19.3 MCP

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


---

<!-- SOURCE: 02_Frameworks.md -->

# 19.4 LangChain · 19.5 LangGraph

# 19.4 LangChain · 19.5 LangGraph

LangChain은 model, retriever, tool과 agent의 통합·고수준 추상화를 제공합니다. LangGraph는 state, node, edge로 장기 실행·상태 기반 workflow를 제어하는 저수준 orchestration에 초점을 둡니다.

선택 기준:

- 단순 RAG chain: 직접 코드 또는 LangChain
- 일반 tool-calling loop: 고수준 agent 검토
- 분기·재시도·checkpoint·human-in-the-loop: LangGraph 검토
- 작은 deterministic workflow: framework 없이 명시적 함수가 더 단순할 수 있음

Framework는 품질을 자동 보장하지 않습니다. 버전 변화가 빠르므로 핵심 domain logic과 평가를 framework API에서 분리합니다.


---

<!-- SOURCE: 03_Safety_and_Evaluation.md -->

# Agent 안전과 평가

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

# 실습: AI Assistant 제작

FAQ 검색과 주문 상태 조회 tool을 가진 deterministic assistant를 구현합니다. 외부 API 없이 tool routing·schema·audit log를 학습합니다.

- [안내](examples/05_ai_assistant_solution/README.md)
- [코드](examples/05_ai_assistant_solution/ai_assistant.py)
- [FAQ](examples/05_ai_assistant_solution/faq.csv)
- [주문 데이터](examples/05_ai_assistant_solution/orders.csv)

