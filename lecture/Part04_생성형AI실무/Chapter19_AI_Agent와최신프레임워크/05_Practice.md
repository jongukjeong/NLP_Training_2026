# 실습: AI Assistant 제작

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

FAQ 검색과 주문 상태 조회 tool을 가진 deterministic assistant를 구현합니다. 외부 API 없이 tool routing·schema·audit log를 학습합니다.

- [안내](examples/05_ai_assistant_solution/README.md)
- [코드](examples/05_ai_assistant_solution/ai_assistant.py)
- [FAQ](examples/05_ai_assistant_solution/faq.csv)
- [주문 데이터](examples/05_ai_assistant_solution/orders.csv)

## AI Assistant 실습 범위

FAQ 검색과 주문 상태 조회 두 개의 읽기 도구부터 시작합니다. 외부 쓰기는 기본 실습에서 제외하거나 명시적 승인 단계를 둡니다.

## 도구 schema

```python
def get_order_status(order_id: str) -> dict:
    """허용된 주문번호의 현재 배송 상태를 조회한다."""
```

주문번호 형식과 사용자 권한을 함수 실행 전에 검사합니다.

## Workflow

```text
요청 분류 → FAQ 또는 주문 조회 → 결과 검증 → 답변
                         ↘ 오류 → 안전한 안내
```

최대 단계와 timeout을 설정해 반복 호출을 막습니다.

## 테스트 사례

- 정상 FAQ
- 존재하지 않는 주문
- 다른 사용자 주문
- 도구 timeout
- 문서 속 지시문
- 같은 요청 반복

## 결과 로그

요청 ID, 선택 도구, 인자 유효성, 호출 수, 최종 성공과 오류 유형을 CSV에 저장합니다.

## 완료 기준

도구 2개 이상, schema 검증, 권한 검사, 최대 단계, 20개 테스트, 안전 실패 0건, README와 감사 로그 예시를 제출합니다.
