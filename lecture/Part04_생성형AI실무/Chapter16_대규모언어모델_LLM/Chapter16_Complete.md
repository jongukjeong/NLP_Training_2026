# Chapter 16 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 16. 대규모 언어모델(LLM)

1. [LLM 개요와 모델 계열](01_LLM_and_Model_Families.md)
2. [로컬 실행과 운영 판단](02_Local_LLM_Operations.md)
3. [요약과 퀴즈](03_Summary_and_Quiz.md)
4. [실습: 로컬 LLM 실행](04_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 16 원리·수학·실습 가이드

## 1. LLM을 비교하는 기준

LLM은 대규모 텍스트에서 다음 토큰 예측을 학습한 언어모델이다. GPT, Llama, Gemma, Mistral, Qwen은 라이선스, 지원 언어, 문맥 길이, 도구 사용, 배포 방식이 다르다. 이름이나 파라미터 수만으로 선택하지 말고 실제 업무 평가셋으로 품질·지연·비용을 비교한다.

## 2. 메모리의 기초 계산

가중치만 저장하는 최소 메모리는 대략 다음과 같다.

\[
Memory\approx Parameters\times Bits/8
\]

70억 파라미터 모델은 FP16이면 약 `7B×2 byte=14GB`, 4-bit이면 이론상 약 3.5GB다. 실제 실행에는 KV cache, 활성값, 런타임 버퍼가 추가된다.

## 3. Quantization과 문맥 비용

양자화는 가중치를 적은 비트로 표현해 메모리와 전송량을 줄인다. 속도가 항상 같은 비율로 빨라지지는 않으며 작은 값 구분이 줄어 품질이 하락할 수 있다. 긴 문맥은 KV cache를 늘리고 일반 Attention 계산은 길이에 대해 대략 제곱으로 증가한다.

## 4. 로컬 실행 실험

```text
고정할 것: 모델/리비전, 양자화, 프롬프트, seed, 최대 토큰
측정할 것: 첫 토큰 지연, tokens/s, peak memory, 정답률, 형식 준수율
```

동일 질문 20개 이상으로 모델별 결과를 저장한다. 라이선스, 모델 카드, 데이터 외부 전송 금지 요구, GPU 메모리를 선택표에 포함한다. 모델 파일은 저장소에 커밋하지 않는다.

1. 8B 모델 FP16 가중치의 이론상 최소 메모리는?
2. 4-bit 양자화의 장점과 위험은?
3. 모델 선택에서 파라미터 수 외에 무엇을 측정할까?

---

<!-- SOURCE: 01_LLM_and_Model_Families.md -->

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

## 큰 모델을 숫자로 비교하기

파라미터는 모델이 학습한 숫자의 개수입니다. 가중치만 저장하는 이론상 메모리는 다음처럼 추정합니다.

\[
Memory\approx Parameters\times\frac{bits}{8}
\]

8B 모델은 FP16에서 약 `80억×2 byte=16GB`, 4-bit에서 약 4GB입니다. 실제 실행에는 KV cache와 런타임 버퍼가 더 필요하므로 GPU 메모리와 정확히 같지 않습니다.

## 모델 계열을 보는 공통 기준

GPT, Llama, Gemma, Mistral, Qwen을 이름으로 서열화하지 않습니다. 지원 언어, 라이선스, 문맥 길이, 도구 호출, 양자화 지원, 하드웨어, 실제 평가 정확도와 지연을 표로 비교합니다. 같은 계열에서도 버전과 크기에 따라 조건이 달라집니다.

## 토큰과 문맥 길이

문맥 길이는 글자 수가 아니라 토큰 수입니다. 한국어는 tokenizer에 따라 같은 문장이 다른 토큰 수가 될 수 있습니다. 입력, 시스템 지시, 검색 문맥, 출력 토큰이 모두 문맥 예산을 사용합니다.

## KV cache의 직관

생성할 때 과거 모든 토큰의 Key와 Value를 매번 다시 계산하지 않도록 저장한 것이 KV cache입니다. 문맥과 batch가 길어질수록 메모리가 증가합니다. 가중치가 들어간다고 실행 가능한 것이 아닌 이유입니다.

## Quantization 해석

4-bit 양자화는 연속적인 가중치를 제한된 단계로 근사합니다. 메모리는 줄지만 작은 값 차이가 사라져 품질이 낮아질 수 있습니다. 속도 향상은 하드웨어와 커널 지원에 따라 달라 실제 측정이 필요합니다.

## 선택 실험

최소 20~50개의 업무 질문으로 정답성, 형식 준수율, 첫 토큰 지연, tokens/s, peak memory를 동일 조건에서 측정합니다. 모델이 크다는 이유만으로 업무 품질이 높다고 결론 내리지 않습니다.

---

<!-- SOURCE: 02_Local_LLM_Operations.md -->

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

1. LLM 선택에서 모델 크기만 보면 되나요? **아니요**
2. 공개 weight 모델의 라이선스는 모두 같나요? **아니요**
3. 로컬 실행의 대표 장점은? **데이터 경계와 실험 통제**
4. 로컬 실행 시 새로 생기는 책임은? **hardware·배포·패치·모델 관리**
5. 양자화는 무엇을 줄이는 데 주로 쓰나요? **메모리 사용량**
6. 모델 비교 시 고정할 것은? **평가셋·prompt·generation 설정·hardware 등**

---

<!-- SOURCE: 04_Practice.md -->

# 실습: 로컬 LLM 실행

- [안내](examples/04_local_llm_solution/README.md)
- [코드](examples/04_local_llm_solution/local_llm_runner.py)
- [입력](examples/04_local_llm_solution/prompts.csv)

Ollama 모델명을 환경변수로 받아 응답과 성능 metadata를 JSONL로 기록합니다.

