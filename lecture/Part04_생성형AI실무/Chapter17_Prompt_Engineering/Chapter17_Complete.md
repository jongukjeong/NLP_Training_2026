# Chapter 17. Prompt Engineering — 통합 원고

> 이 문서는 Chapter 17. Prompt Engineering 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 17. Prompt Engineering — `README.md`
- 17.1~17.3 Prompt 기본·Zero-shot·Few-shot — `01_Prompt_Principles.md`
- 17.4 Chain of Thought · 17.5 Structured Output — `02_Reasoning_and_Structure.md`
- 프롬프트 평가와 최적화 — `03_Evaluation.md`
- 요약과 퀴즈 — `04_Summary_and_Quiz.md`
- 실습: 프롬프트 최적화 — `05_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 17. Prompt Engineering

# Chapter 17. Prompt Engineering

1. [기본 원리·Zero-shot·Few-shot](01_Prompt_Principles.md)
2. [Reasoning과 Structured Output](02_Reasoning_and_Structure.md)
3. [평가와 최적화](03_Evaluation.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: 프롬프트 최적화](05_Practice.md)


---

<!-- SOURCE: 01_Prompt_Principles.md -->

# 17.1~17.3 Prompt 기본·Zero-shot·Few-shot

# 17.1~17.3 Prompt 기본·Zero-shot·Few-shot

Prompt는 역할 수사보다 목표, 입력, 제약, 출력 계약과 성공 기준이 중요합니다.

```text
목표 → 필요한 배경 → 입력 구분 → 제약 → 출력 schema → 예외 처리
```

Zero-shot은 예시 없이 지시하고 Few-shot은 대표 입력·출력 예시를 제공합니다. Few-shot 예시는 정상 사례뿐 아니라 경계·거부 사례와 label 균형을 포함합니다.

Prompt injection에 대비해 사용자 입력과 신뢰된 지시를 구분하고, 입력 안의 지시를 시스템 규칙으로 취급하지 않도록 합니다. 모델 출력은 검증 전까지 신뢰하지 않습니다.


---

<!-- SOURCE: 02_Reasoning_and_Structure.md -->

# 17.4 Chain of Thought · 17.5 Structured Output

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


---

<!-- SOURCE: 03_Evaluation.md -->

# 프롬프트 평가와 최적화

# 프롬프트 평가와 최적화

좋아 보이는 예시 하나가 아니라 고정 평가셋으로 version을 비교합니다.

평가 항목:

- task 정확도
- schema 준수율
- 금지 내용·hallucination 비율
- latency와 token 비용
- 긴 입력·모호한 입력·prompt injection 견고성

한 번에 여러 요소를 바꾸지 않고 prompt version, model, temperature를 기록합니다. LLM judge는 편향이 있으므로 중요한 표본은 사람이 검토합니다.


---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 요약과 퀴즈

# 요약과 퀴즈

1. Prompt의 핵심 구성은? **목표·입력·제약·출력 계약·성공 기준**
2. Few-shot 예시에 경계 사례가 필요한 이유는? **결정 기준을 명확히 하기 위해**
3. 사용자 입력 속 지시를 신뢰해야 하나요? **아니요**
4. 내부 추론 전체 대신 요청할 것은? **검증 가능한 짧은 근거와 결과**
5. JSON 문자열이면 schema가 보장되나요? **아니요, 검증 필요**
6. Prompt 개선은 무엇으로 비교하나요? **고정 평가셋과 version별 지표**


---

<!-- SOURCE: 05_Practice.md -->

# 실습: 프롬프트 최적화

# 실습: 프롬프트 최적화

고객 문의 분류 prompt의 zero-shot/few-shot 버전을 생성하고 API 응답의 JSON schema 준수율을 비교합니다.

- [안내](examples/05_prompt_optimization_solution/README.md)
- [코드](examples/05_prompt_optimization_solution/prompt_evaluator.py)
- [평가셋](examples/05_prompt_optimization_solution/evaluation.csv)

