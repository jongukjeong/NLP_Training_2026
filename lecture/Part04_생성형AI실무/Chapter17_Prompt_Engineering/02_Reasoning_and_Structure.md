# 17.4 Chain of Thought · 17.5 Structured Output

복잡한 task는 문제를 단계로 나누고 필요한 중간 검증을 요청할 수 있습니다. 내부 추론 전체를 노출하도록 요구하기보다 최종 답과 검증 가능한 짧은 근거·계산 결과를 요청합니다.

Structured Output은 후속 시스템이 파싱할 schema를 강제합니다.

```json
{
  "category": "delivery",
  "priority": "high",
  "reason": "배송 지연과 행사 일정 충돌"
}
```

JSON parse, 필수 field, enum, 길이와 금지값을 코드로 검증하고 실패 시 제한된 재시도를 수행합니다. 자연어로 “JSON으로 써줘”만 요청하는 것보다 API의 schema 기능을 우선 검토합니다.
