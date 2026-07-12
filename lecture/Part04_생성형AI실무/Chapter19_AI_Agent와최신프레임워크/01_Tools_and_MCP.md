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
