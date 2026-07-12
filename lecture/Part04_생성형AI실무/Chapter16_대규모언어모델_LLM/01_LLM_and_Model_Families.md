# 16.1~16.6 LLM과 주요 계열

LLM은 대규모 말뭉치와 파라미터로 다음 token 예측 등을 학습한 언어모델입니다. 모델 이름만으로 품질을 판단하지 않고 task, 언어, context, tool use, 라이선스, hardware와 평가 결과를 비교합니다.

| 계열 | 검토 관점 |
|---|---|
| GPT | API 기반 frontier·도구 사용과 관리형 서비스 |
| Llama | 공개 weight 생태계와 다양한 fine-tune |
| Gemma | Google 계열 공개 모델과 크기 선택 |
| Mistral | 효율적인 공개·상용 모델 선택지 |
| Qwen | 다국어·코딩 등 폭넓은 크기와 task 계열 |

“오픈 모델”은 라이선스가 모두 같다는 뜻이 아닙니다. 상업 이용, 재배포, 파생 모델과 acceptable-use 조건을 모델별로 확인합니다.

평가 축: task 품질, 한국어, latency, throughput, memory, context 길이, hallucination, 안전성, 총비용.
