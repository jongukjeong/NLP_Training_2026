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

## 다음 토큰 예측으로 문장 전체를 학습하기

\[
P(x_1,\ldots,x_T)=\prod_{t=1}^{T}P(x_t|x_{<t})
\]

문장 “나는 학교에 간다”는 “나는→학교에”, “나는 학교에→간다” 같은 여러 학습 사례를 동시에 제공합니다. 모델은 앞 토큰들로 다음 토큰의 확률 분포를 만듭니다.

정답 토큰 확률이 0.7이면 손실은 `-log(0.7)≈0.357`, 0.01이면 약 4.605입니다. 정답에 낮은 확률을 준 예를 강하게 수정합니다.

## Causal mask

학습 데이터에는 정답 문장 전체가 있지만 위치 `t`가 `t+1` 이후를 보면 정답 누수입니다. 삼각형 mask로 현재와 과거만 보게 합니다.

```text
       1  2  3  4 (Key)
Q 1    O  X  X  X
  2    O  O  X  X
  3    O  O  O  X
  4    O  O  O  O
```

## 생성은 반복 추론이다

프롬프트를 한 번 처리한 뒤 토큰 하나를 선택하고, 그 토큰을 입력에 붙여 다시 다음 토큰을 계산합니다. `<EOS>`나 최대 토큰에서 종료합니다. 그래서 출력이 길수록 지연과 비용이 증가합니다.

## Temperature 숫자 예

로짓 `[2,1]`을 temperature 1로 Softmax하면 약 `[0.73,0.27]`입니다. temperature 0.5에서는 `[0.88,0.12]`로 상위 후보에 집중합니다. 낮은 temperature가 사실을 보장하지는 않고 출력 변동만 줄입니다.

## ChatGPT와 기반 모델

대화형 시스템은 언어모델에 지시 학습, 안전 정책, 도구 사용, 대화 상태 관리 등이 결합된 형태입니다. 자연스러운 문장은 근거의 정확성을 보장하지 않으므로 중요한 답은 출처와 도구 결과로 검증합니다.

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

## 생성 설정을 주사위에 비유하기

모델은 다음 단어 하나를 확정해서 아는 것이 아니라 후보별 점수를 냅니다. Sampling은 이 확률을 바탕으로 주사위를 던지는 과정입니다. Greedy decoding은 가장 높은 후보만 매번 고릅니다.

## Top-k와 Top-p

Top-k는 점수가 높은 후보 k개만 남깁니다. Top-p는 높은 순서대로 확률을 더해 누적합이 p가 될 때까지 남깁니다.

확률이 `[0.5,0.3,0.15,0.05]`일 때 top-k 2는 앞의 두 후보만 사용합니다. top-p 0.8도 앞의 두 후보에서 누적 0.8이 되므로 같은 후보가 남습니다. 다른 분포에서는 후보 수가 달라집니다.

## 반복 제어

긴 생성에서 같은 표현이 반복될 수 있습니다. repetition penalty, frequency penalty, stop sequence를 사용할 수 있지만 너무 강하면 필요한 전문용어 반복도 막습니다. 생성 설정과 실제 실패 사례를 함께 기록합니다.

## 프롬프트 구성의 쉬운 순서

1. 해야 할 일 한 문장
2. 사용할 입력과 범위
3. 지켜야 할 규칙
4. 출력 형식
5. 애매할 때의 처리
6. 필요한 경우 대표 예시

“친절하고 훌륭하게 답하라”보다 “근거 문서에 없는 내용은 모른다고 답하고 문서 ID를 표시하라”가 검증하기 쉽습니다.

## Hallucination

Hallucination은 모델이 문법적으로 자연스럽지만 사실이 아닌 내용을 만드는 현상입니다. 낮은 temperature만으로 해결되지 않습니다. 검색 근거, 도구 호출, 출처 표시, 후처리 검증과 사람 검토가 필요합니다.

## 토큰 비용 계산

\[
요청비용=입력토큰\times입력단가+출력토큰\times출력단가
\]

실제 단가는 모델마다 바뀌므로 공식 가격표를 확인합니다. 예제에서는 입력·출력 토큰을 따로 기록해 프롬프트가 길어졌을 때 비용 변화를 설명합니다.

## 안전한 API 사용

API 키는 코드와 Markdown에 적지 않고 환경변수나 secret manager에 저장합니다. 로그에는 개인정보와 전체 프롬프트를 무조건 남기지 않습니다. timeout, 재시도 횟수, rate limit 처리와 요청 ID를 관리합니다.

## 생성 평가

정답이 하나인 분류와 달리 생성은 여러 좋은 답이 가능합니다. 사실성, 지시 준수, 형식, 유해성, 근거성, 길이, 비용과 지연을 평가표로 분리합니다.

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

