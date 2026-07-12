# 프롬프트 평가와 최적화

좋아 보이는 예시 하나가 아니라 고정 평가셋으로 version을 비교합니다.

평가 항목:

- task 정확도
- schema 준수율
- 금지 내용·hallucination 비율
- latency와 token 비용
- 긴 입력·모호한 입력·prompt injection 견고성

한 번에 여러 요소를 바꾸지 않고 prompt version, model, temperature를 기록합니다. LLM judge는 편향이 있으므로 중요한 표본은 사람이 검토합니다.
