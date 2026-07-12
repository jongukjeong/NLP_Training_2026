# Chapter 14. GPT — 통합 원고

> 이 문서는 Chapter 14. GPT 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 14. GPT — `README.md`
- 14.1 Decoder Only · 14.2 Auto Regression — `01_GPT_Architecture.md`
- 14.3 Prompting · 14.4 Text Generation · 14.5 ChatGPT 이해 — `02_Prompting_and_Generation.md`
- 요약과 퀴즈 — `03_Summary_and_Quiz.md`
- 실습: GPT API 활용 — `04_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 14. GPT

# Chapter 14. GPT

1. [Decoder Only와 Auto Regression](01_GPT_Architecture.md)
2. [Prompting·Text Generation·ChatGPT](02_Prompting_and_Generation.md)
3. [요약과 퀴즈](03_Summary_and_Quiz.md)
4. [실습: GPT API 활용](04_Practice.md)

API 실습은 OpenAI Responses API와 공식 Python SDK를 사용하며 키를 저장소에 저장하지 않습니다.


---

<!-- SOURCE: 01_GPT_Architecture.md -->

# 14.1 Decoder Only · 14.2 Auto Regression

# 14.1 Decoder Only · 14.2 Auto Regression

GPT 계열은 causal self-attention을 사용하는 decoder-only 언어모델입니다. 이전 token을 조건으로 다음 token의 확률을 예측합니다.

```text
P(x) = Π P(x_t | x_1 ... x_(t-1))
```

Causal mask는 학습 중 미래 token을 보지 못하게 합니다. 생성 시 예측 token을 입력 뒤에 붙여 종료 조건까지 반복합니다.

Generation 설정:

- max output tokens: 비용·지연·응답 길이 제한
- temperature/top-p: sampling 다양성
- stop/구조화 출력: 종료와 형식 통제

모델 출력은 사실 검증이 필요하며 확률적으로 그럴듯한 문장이 근거를 보장하지 않습니다.


---

<!-- SOURCE: 02_Prompting_and_Generation.md -->

# 14.3 Prompting · 14.4 Text Generation · 14.5 ChatGPT 이해

# 14.3 Prompting · 14.4 Text Generation · 14.5 ChatGPT 이해

좋은 prompt는 역할, 목표, 입력, 제약, 출력 형식과 평가 기준을 명확히 합니다. 중요한 규칙은 모호한 수사보다 검사 가능한 조건으로 작성합니다.

ChatGPT는 모델 하나의 이름이 아니라 대화형 제품 경험이며, API 애플리케이션은 모델 호출, 상태, 도구, 보안, 평가를 개발자가 구성합니다.

운영 원칙:

- API key는 환경변수·secret manager에 저장
- 사용자 입력과 모델 출력을 신뢰 경계로 취급
- timeout, retry, rate limit과 비용 예산 설정
- model ID, prompt version, request ID, latency 기록
- 개인·기밀정보 전송 정책 확인
- 고위험 결정에는 사람 검토


---

<!-- SOURCE: 03_Summary_and_Quiz.md -->

# 요약과 퀴즈

# 요약과 퀴즈

1. GPT의 기본 구조는? **Decoder-only Transformer**
2. Auto Regression은 무엇을 예측하나요? **이전 token을 조건으로 다음 token**
3. causal mask의 목적은? **미래 token 참조 방지**
4. temperature를 높이면 일반적으로? **출력 다양성이 증가**
5. API key를 코드에 넣어도 되나요? **아니요**
6. ChatGPT와 API 모델은 같은 개념인가요? **제품 경험과 모델/API는 구분됨**
7. 모델 응답이 유창하면 사실인가요? **아니요, 별도 검증 필요**


---

<!-- SOURCE: 04_Practice.md -->

# 실습: GPT API 활용

# 실습: GPT API 활용

CSV의 고객 문의를 읽어 간결한 답변 초안을 생성하고 요청 설정과 결과를 JSONL로 저장합니다.

- [안내](examples/04_gpt_api_solution/README.md)
- [코드](examples/04_gpt_api_solution/gpt_api_example.py)
- [입력](examples/04_gpt_api_solution/questions.csv)

현재 공식 모델 안내의 비용 민감형 모델을 기본값으로 사용하지만 `OPENAI_MODEL` 환경변수로 교체할 수 있습니다.

