# Chapter 14 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 14. GPT

1. [Decoder Only와 Auto Regression](01_GPT_Architecture.md)
2. [Prompting·Text Generation·ChatGPT](02_Prompting_and_Generation.md)
3. [요약과 퀴즈](03_Summary_and_Quiz.md)
4. [실습: GPT API 활용](04_Practice.md)

API 실습은 OpenAI Responses API와 공식 Python SDK를 사용하며 키를 저장소에 저장하지 않습니다.

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 14 원리·수학·실습 가이드

## 1. Decoder-only와 자기회귀

GPT는 이전 토큰만 보고 다음 토큰을 예측한다.

\[
P(x_1,\dots,x_T)=\prod_{t=1}^{T}P(x_t\mid x_{<t})
\]

Causal mask 때문에 학습 중에도 미래 정답을 볼 수 없다. 다음 토큰 교차 엔트로피를 줄이는 과정에서 문법·지식·패턴을 학습한다.

## 2. 생성 제어

Temperature는 로짓을 Softmax에 넣기 전 나눈다.

\[
p_i=\frac{\exp(z_i/\tau)}{\sum_j\exp(z_j/\tau)}
\]

`τ<1`이면 상위 토큰에 집중해 일관성이 커지고, `τ>1`이면 분포가 평평해져 다양성이 커진다. top-k는 상위 k개, top-p는 누적 확률 p까지 후보를 제한한다. 정확성이 중요한 과제는 낮은 변동성과 검증 절차를 우선한다.

## 3. 프롬프트와 API

좋은 요청은 역할보다 `목표, 입력, 제약, 출력 형식, 예시, 실패 처리`가 명확하다. 외부 입력은 지시문과 구분하고 비밀값을 프롬프트에 넣지 않는다.

```python
from openai import OpenAI
client = OpenAI()
response = client.responses.create(
    model="사용할-모델",
    input="아래 문의를 한 문장으로 요약하세요: ...",
)
print(response.output_text)
```

모델명과 API 형식은 실습 시점의 공식 문서를 확인한다. 재현을 위해 모델, 프롬프트 버전, 파라미터, 입력 ID, 출력, 지연시간을 기록한다.

## 4. ChatGPT를 이해하는 관점

대화 모델은 기본 언어모델에 지시 따르기와 안전성 조정이 더해진 시스템이다. 자연스러운 답이 사실성을 보장하지 않으므로 최신·고위험 정보는 검색·도구·사람 검토로 근거를 확인한다.

1. causal mask가 필요한 이유는?
2. temperature를 낮추면 분포는 어떻게 변하는가?
3. API 실험 재현을 위해 무엇을 기록해야 하는가?

---

<!-- SOURCE: 01_GPT_Architecture.md -->

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

CSV의 고객 문의를 읽어 간결한 답변 초안을 생성하고 요청 설정과 결과를 JSONL로 저장합니다.

- [안내](examples/04_gpt_api_solution/README.md)
- [코드](examples/04_gpt_api_solution/gpt_api_example.py)
- [입력](examples/04_gpt_api_solution/questions.csv)

현재 공식 모델 안내의 비용 민감형 모델을 기본값으로 사용하지만 `OPENAI_MODEL` 환경변수로 교체할 수 있습니다.

