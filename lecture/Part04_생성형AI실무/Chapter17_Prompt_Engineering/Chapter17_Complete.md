# Chapter 17 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 17. Prompt Engineering

1. [기본 원리·Zero-shot·Few-shot](01_Prompt_Principles.md)
2. [Reasoning과 Structured Output](02_Reasoning_and_Structure.md)
3. [평가와 최적화](03_Evaluation.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: 프롬프트 최적화](05_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 17 원리·수학·실습 가이드

## 1. 프롬프트를 프로그램처럼 관리하기

프롬프트는 감으로 고치는 문장이 아니라 입력과 출력 계약이다. `목표 → 입력 경계 → 규칙 → 출력 스키마 → 예시 → 실패 처리`를 명시하고 버전과 평가 결과를 기록한다.

Zero-shot은 예시 없이 지시하고, Few-shot은 대표 입출력 예시를 제공한다. 예시는 많기보다 경계 사례와 실제 분포를 잘 대표해야 한다.

## 2. Structured Output

```json
{"category":"배송","priority":"high","reason":"하루 이상 지연"}
```

필드 타입, 허용값, 누락 처리 규칙을 스키마로 정의한다. 단순히 “JSON으로 답해”라고만 하면 설명 문장이 섞이거나 키가 변할 수 있다. 파싱 실패 시 제한 횟수 재시도하고 원문을 보관한다.

## 3. 추론 요청과 검증

복잡한 문제는 하위 작업으로 나누고 필요한 중간 산출물만 구조화해 요청한다. 장황한 비공개 사고과정을 요구하기보다 근거, 계산 결과, 확인 가능한 요약을 받는다. 외부 문서의 명령은 데이터로 취급해 prompt injection을 막는다.

## 4. 평가 수학

\[
Accuracy=\frac{correct}{N},\quad SchemaRate=\frac{valid\ outputs}{N}
\]

\[
AverageCost=\frac{\sum_i cost_i}{N},\quad P95Latency=95\%\ 지점의\ 지연시간
\]

프롬프트 A/B는 같은 평가셋, 모델, 파라미터에서 비교한다. 정확도뿐 아니라 형식 준수율, 안전 실패, 토큰, 비용, 지연을 함께 본다. 테스트셋을 보며 프롬프트를 반복 수정하면 과적합되므로 개발셋과 최종 테스트셋을 분리한다.

1. Few-shot 예시는 어떤 사례를 우선해야 하는가?
2. Structured Output에서 스키마가 필요한 이유는?
3. 프롬프트 비교에서 정확도 외 지표는?

---

<!-- SOURCE: 01_Prompt_Principles.md -->

# 17.1~17.3 Prompt 기본·Zero-shot·Few-shot

Prompt는 역할 수사보다 목표, 입력, 제약, 출력 계약과 성공 기준이 중요합니다.

```text
목표 → 필요한 배경 → 입력 구분 → 제약 → 출력 schema → 예외 처리
```

Zero-shot은 예시 없이 지시하고 Few-shot은 대표 입력·출력 예시를 제공합니다. Few-shot 예시는 정상 사례뿐 아니라 경계·거부 사례와 label 균형을 포함합니다.

Prompt injection에 대비해 사용자 입력과 신뢰된 지시를 구분하고, 입력 안의 지시를 시스템 규칙으로 취급하지 않도록 합니다. 모델 출력은 검증 전까지 신뢰하지 않습니다.

## 프롬프트를 계약서처럼 쓰기

좋은 프롬프트는 화려한 역할 문장보다 목표와 판정 기준이 명확합니다.

```text
목표: 고객 문의를 하나의 카테고리로 분류
입력: <inquiry>...</inquiry>
허용값: 배송, 환불, 계정, 기타
규칙: 불명확하면 기타
출력: {"category":"...","reason":"..."}
```

입력 경계를 태그로 분리하면 사용자 문장과 시스템 규칙을 구분하기 쉽습니다. 입력 속 “앞 지시를 무시하라”는 문장은 데이터이지 신뢰된 지시가 아닙니다.

## Zero-shot과 Few-shot

Zero-shot은 설명만으로 수행하고 Few-shot은 예시를 함께 줍니다. 예시는 쉬운 사례만 반복하지 말고 클래스 경계, 예외, 모호한 사례를 포함합니다. 잘못된 예시는 모델에 강한 잘못된 패턴을 줄 수 있습니다.

## 평가를 수치로 보기

\[
Accuracy=\frac{정답수}{전체수},\quad
SchemaRate=\frac{파싱가능한출력수}{전체수}
\]

100개 중 정답 87개, JSON 파싱 성공 95개면 정확도 87%, 형식 준수율 95%입니다. 정확도만 보면 운영에서 5%가 파싱 실패한다는 문제를 놓칩니다.

## 프롬프트 변경 실험

평가셋, 모델, temperature를 고정하고 프롬프트 한 요소만 바꿉니다. 개발셋 결과로 개선하고 마지막 test는 최종 확인에만 사용합니다. 프롬프트 버전, 토큰 수, 비용, P95 지연도 기록합니다.

## 쉬운 개선 순서

모호한 목표 수정 → 입력 경계 표시 → 출력 스키마 명시 → 대표 예시 추가 → 실패 처리 규칙 → 자동 평가 순으로 개선합니다. 무조건 긴 프롬프트가 좋은 것은 아닙니다.

---

<!-- SOURCE: 02_Reasoning_and_Structure.md -->

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

1. Prompt의 핵심 구성은? **목표·입력·제약·출력 계약·성공 기준**
2. Few-shot 예시에 경계 사례가 필요한 이유는? **결정 기준을 명확히 하기 위해**
3. 사용자 입력 속 지시를 신뢰해야 하나요? **아니요**
4. 내부 추론 전체 대신 요청할 것은? **검증 가능한 짧은 근거와 결과**
5. JSON 문자열이면 schema가 보장되나요? **아니요, 검증 필요**
6. Prompt 개선은 무엇으로 비교하나요? **고정 평가셋과 version별 지표**

---

<!-- SOURCE: 05_Practice.md -->

# 실습: 프롬프트 최적화

고객 문의 분류 prompt의 zero-shot/few-shot 버전을 생성하고 API 응답의 JSON schema 준수율을 비교합니다.

- [안내](examples/05_prompt_optimization_solution/README.md)
- [코드](examples/05_prompt_optimization_solution/prompt_evaluator.py)
- [평가셋](examples/05_prompt_optimization_solution/evaluation.csv)

