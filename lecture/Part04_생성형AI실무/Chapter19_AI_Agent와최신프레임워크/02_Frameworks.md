# 19.4 LangChain · 19.5 LangGraph

LangChain은 model, retriever, tool과 agent의 통합·고수준 추상화를 제공합니다. LangGraph는 state, node, edge로 장기 실행·상태 기반 workflow를 제어하는 저수준 orchestration에 초점을 둡니다.

선택 기준:

- 단순 RAG chain: 직접 코드 또는 LangChain
- 일반 tool-calling loop: 고수준 agent 검토
- 분기·재시도·checkpoint·human-in-the-loop: LangGraph 검토
- 작은 deterministic workflow: framework 없이 명시적 함수가 더 단순할 수 있음

Framework는 품질을 자동 보장하지 않습니다. 버전 변화가 빠르므로 핵심 domain logic과 평가를 framework API에서 분리합니다.
