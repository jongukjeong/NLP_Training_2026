# Chapter 16. 대규모 언어모델(LLM) — 통합 원고

> 이 문서는 Chapter 16. 대규모 언어모델(LLM) 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 16. 대규모 언어모델(LLM) — `README.md`
- 16.1~16.6 LLM과 주요 계열 — `01_LLM_and_Model_Families.md`
- 로컬 LLM 실행과 운영 판단 — `02_Local_LLM_Operations.md`
- 요약과 퀴즈 — `03_Summary_and_Quiz.md`
- 실습: 로컬 LLM 실행 — `04_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 16. 대규모 언어모델(LLM)

# Chapter 16. 대규모 언어모델(LLM)

1. [LLM 개요와 모델 계열](01_LLM_and_Model_Families.md)
2. [로컬 실행과 운영 판단](02_Local_LLM_Operations.md)
3. [요약과 퀴즈](03_Summary_and_Quiz.md)
4. [실습: 로컬 LLM 실행](04_Practice.md)


---

<!-- SOURCE: 01_LLM_and_Model_Families.md -->

# 16.1~16.6 LLM과 주요 계열

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


---

<!-- SOURCE: 02_Local_LLM_Operations.md -->

# 로컬 LLM 실행과 운영 판단

# 로컬 LLM 실행과 운영 판단

로컬 실행 장점은 데이터 경계와 실험 통제이며, 단점은 hardware·배포·보안 패치·모델 관리 책임입니다.

Ollama 기본 흐름:

```text
모델 pull → local API 실행 → prompt 요청 → token/latency 기록
```

정량 기록:

- prompt/output token 수
- load/prompt evaluation/generation 시간
- tokens per second
- peak memory
- model tag와 digest
- generation parameters

양자화는 memory를 줄일 수 있지만 품질과 속도 변화가 있으므로 동일 평가셋으로 비교합니다. 민감 데이터가 로컬이라는 이유만으로 안전한 것은 아니며 로그, cache, model access와 OS 권한을 관리해야 합니다.


---

<!-- SOURCE: 03_Summary_and_Quiz.md -->

# 요약과 퀴즈

# 요약과 퀴즈

1. LLM 선택에서 모델 크기만 보면 되나요? **아니요**
2. 공개 weight 모델의 라이선스는 모두 같나요? **아니요**
3. 로컬 실행의 대표 장점은? **데이터 경계와 실험 통제**
4. 로컬 실행 시 새로 생기는 책임은? **hardware·배포·패치·모델 관리**
5. 양자화는 무엇을 줄이는 데 주로 쓰나요? **메모리 사용량**
6. 모델 비교 시 고정할 것은? **평가셋·prompt·generation 설정·hardware 등**


---

<!-- SOURCE: 04_Practice.md -->

# 실습: 로컬 LLM 실행

# 실습: 로컬 LLM 실행

- [안내](examples/04_local_llm_solution/README.md)
- [코드](examples/04_local_llm_solution/local_llm_runner.py)
- [입력](examples/04_local_llm_solution/prompts.csv)

Ollama 모델명을 환경변수로 받아 응답과 성능 metadata를 JSONL로 기록합니다.

