# 실습: 프롬프트 최적화

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

고객 문의 분류 prompt의 zero-shot/few-shot 버전을 생성하고 API 응답의 JSON schema 준수율을 비교합니다.

- [안내](examples/05_prompt_optimization_solution/README.md)
- [코드](examples/05_prompt_optimization_solution/prompt_evaluator.py)
- [평가셋](examples/05_prompt_optimization_solution/evaluation.csv)

## 실습 목표

하나의 업무 Prompt를 Zero-shot에서 시작해 Few-shot과 Structured Output으로 개선하고 같은 평가셋에서 비교합니다.

## 단계

1. 평가 질문 30개와 기대 결과 작성
2. Zero-shot 기준 Prompt 실행
3. 오류 유형 분류
4. 판단 경계 예시 3~5개 추가
5. JSON schema 적용
6. 정확도·형식·토큰·P95 비교

## 결과 파일

```text
prompt_version,input_id,output,parsed,correct,latency,input_tokens,output_tokens,error_type
```

## Prompt 버전

Prompt 파일에 `v01`, `v02`를 붙이고 변경 이유를 기록합니다. 결과가 나빠진 버전도 삭제하지 않아 반복 실험을 방지합니다.

## 안전 사례

입력 내부에 지시 무시 문구, 개인정보, 범위 밖 요청을 포함합니다. 외부 입력은 데이터로 취급하고 민감정보는 전송 전 제거합니다.

## 완료 기준

기준선과 개선 버전, 30개 이상 평가, 자동 파서, 오류 분석, 비용·지연, 최종 채택 이유를 제출합니다.
