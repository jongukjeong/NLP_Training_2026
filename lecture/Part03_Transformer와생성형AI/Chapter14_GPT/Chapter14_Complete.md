# Chapter 14 통합 강의 원고

---

<!-- SOURCE: README.md -->

# Chapter 14. GPT

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **디코더 전용 모델(Decoder-only Model): Decoder 블록만 사용해 다음 토큰을 생성하는 모델**
- **자기회귀(Autoregression): 이전 출력들을 조건으로 다음 값을 순서대로 예측하는 방식**
- **프롬프트(Prompt): 모델에 전달하는 목표·입력·제약·출력 형식**
- **구조화 출력(Structured Output): JSON처럼 프로그램이 검사할 수 있는 정해진 형식**
- **환각(Hallucination): 근거 없이 그럴듯한 사실을 생성하는 현상**

1. [Decoder Only와 Auto Regression](01_GPT_Architecture.md)
2. [Prompting·Text Generation·ChatGPT](02_Prompting_and_Generation.md)
3. [퀴즈](03_Summary_and_Quiz.md)
4. [실습: GPT API 활용](04_Practice.md)

API 실습은 OpenAI Responses API와 공식 Python SDK를 사용하며 키를 저장소에 저장하지 않습니다.

## 먼저 읽을 상세 가이드

- [비전공자용 GPT 생성 워크북](00_비전공자_GPT_생성워크북.md): 자기회귀 확률, 생성 설정, 구조화 출력과 오류 검증을 쉽게 설명합니다.

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: LEARNING_PATH.md -->

# Chapter 14 비전공자 학습 경로

## 기본 도달 목표

같은 질문에 두 프롬프트를 적용하고 결과 비교

완성형 코드를 처음부터 모두 이해하거나 다시 작성하는 것은 기본 목표가 아닙니다.

## 1. Step by Step — 강사와 함께

1. 짧은 질문 하나를 정한다
2. 기본 프롬프트 결과를 기록한다
3. 조건을 한 가지 추가한다
4. 두 결과를 기준표로 비교한다

각 단계가 끝날 때 입력, 출력 또는 중간 결과를 화면에서 확인합니다. 설명할 수 없는 줄은 다음 단계로 넘어가기 전에 질문합니다.

## 2. Basic Practice — 짧은 흐름 연결

Step by Step의 네 단계를 한 흐름으로 연결합니다. 처음에는 함수 분리, 타입 힌트, 복잡한 예외 처리와 자동 보고서를 요구하지 않습니다.

완료 확인:

- 입력이 무엇인지 설명한다.
- 핵심 처리 한 단계를 찾아 수정한다.
- 출력이 예상과 다른 이유를 한 가지 찾는다.
- 실행 결과를 짧게 기록한다.

## 실행 코드 위치

- [Step by Step](examples/01_step_by_step/README.md)
- [Basic Practice](examples/02_basic_practice/README.md)
- [Practice Starter](examples/03_practice_starter/README.md)

세 자료는 외부 모델이나 API 없이 핵심 흐름을 먼저 이해하도록 구성했습니다. 실제 라이브러리와 완성형 구조는 기존 solution에서 비교합니다.

## 3. Practice·Assignment — 먼저 시도

[04_Practice.md](04_Practice.md)의 기본 요구사항을 먼저 수행합니다. 막히면 전체 solution 대신 필요한 단계의 힌트만 확인합니다.

## 4. Solution — 피드백 후 공개

[examples/04_gpt_api_solution/README.md](examples/04_gpt_api_solution/README.md)은 다수의 수강생이 기본 요구사항을 시도하고 공통 오류를 함께 확인한 뒤 공개합니다. 자신의 코드와 다음 항목을 비교합니다.

1. 반복되는 처리를 어떻게 묶었는가
2. 잘못된 입력을 어디에서 검사하는가
3. 결과를 어떻게 검증하고 기록하는가

## 선택 확장

- API 재시도
- 회귀 시험
- 비용 기록
- 안전 필터

선택 확장은 기본 완료 기준에 포함하지 않습니다.

---

<!-- SOURCE: 00_GPT_API와_생성결과_검증.md -->

# Chapter 14 GPT API와 생성 결과 검증

## API 호출을 네 단계로 보기

```text
요청 구성 → 모델 호출 → 출력 추출 → 검증·기록
```

성공 응답을 화면에 출력하는 것만으로 실습을 끝내지 않고, timeout·재시도·비용·형식 오류를 처리합니다.

## 입력을 명확히 나누기

```text
목표: 문의를 세 문장 이내로 요약
규칙: 원문에 없는 사실을 추가하지 않음
입력: <inquiry>...</inquiry>
출력: {"summary":"..."}
```

외부 입력의 “앞 규칙을 무시하라”는 문장은 데이터이지 신뢰할 지시가 아닙니다.

## 구조화 출력 검증

```python
import json

try:
    result = json.loads(text)
    assert isinstance(result.get("summary"), str)
except (json.JSONDecodeError, AssertionError):
    result = {"summary": None, "status": "needs_review"}
```

JSON처럼 보이는 문자열과 실제 파싱 가능한 JSON은 다릅니다. 필수 필드와 타입도 검사합니다.

## 재시도 원칙

네트워크 timeout과 rate limit은 제한 횟수 재시도할 수 있습니다. 잘못된 요청이나 인증 실패를 무한 재시도하면 해결되지 않습니다. 지수 backoff와 요청 ID를 기록합니다.

## 생성 결과의 세 종류 오류

1. 사실 오류: 원문에 없는 배송 날짜 추가
2. 형식 오류: JSON 밖에 설명 문장 포함
3. 지시 오류: 세 문장 제한 위반

각 오류는 해결책이 다르므로 한 개의 “정확도”로만 묶지 않습니다.

## 평가표

| ID | 사실성 | 형식 | 지시 준수 | 지연 | 토큰 |
|---|---:|---:|---:|---:|---:|
| q01 | 1 | 1 | 1 | 기록 | 기록 |
| q02 | 0 | 1 | 1 | 기록 | 기록 |

최소 30~50개의 고정 질문으로 프롬프트 버전을 비교합니다.

## Temperature 실험

같은 질문을 temperature 0과 높은 값에서 여러 번 실행해 변동성을 비교합니다. 낮은 temperature가 사실성을 보장하지는 않으며, 정확성이 필요한 과제는 근거와 검증 도구가 필요합니다.

## 비용과 길이

입력에 긴 예시와 문서를 계속 추가하면 품질이 좋아질 수도 있지만 비용과 지연도 증가합니다. 사용하지 않는 지시와 중복 문맥을 제거하고 입력·출력 토큰을 따로 측정합니다.

## 개인정보

고객 이름·전화번호·주문번호가 필요한지 먼저 판단하고 불필요하면 마스킹합니다. API 키, 전체 요청 원문, 민감한 출력이 로그에 남지 않도록 합니다.

## ChatGPT 설명 시 주의

ChatGPT를 “인터넷의 모든 정보를 기억하는 데이터베이스”로 설명하지 않습니다. 주어진 문맥과 학습 패턴으로 다음 토큰을 생성하며 최신성과 사실성은 별도 도구로 확인해야 합니다.

---

<!-- SOURCE: 00_GPT_프롬프트회귀시험과_안전.md -->

# Chapter 14 GPT 프롬프트 회귀시험과 안전

## 회귀시험

프롬프트나 모델을 바꿀 때 예전에 통과한 질문이 다시 실패하지 않는지 고정 테스트셋으로 확인합니다.

```text
입력 ID | 기대 조건 | 실제 출력 | 사실성 | 형식 | 통과
```

문장 전체 일치보다 필수 키, 허용값, 근거 포함, 금지 표현 같은 검증 가능한 조건을 사용합니다.

## 비결정성

같은 입력도 sampling 설정에서 달라질 수 있습니다. 중요한 과제는 여러 번 실행한 통과율을 기록하거나 변동성을 낮추고 구조화 검증을 적용합니다.

## Prompt injection 시험

입력에 “앞 지시를 무시하라”, 가짜 시스템 메시지, 문서 속 도구 호출 요청을 포함해 정책이 유지되는지 확인합니다. Prompt만 믿지 않고 도구 권한과 실행 계층에서 차단합니다.

## 근거성 평가

답변의 각 핵심 주장이 제공 문맥에서 확인되는지 표시합니다. 인용 문자열이 존재하는 것과 실제 근거가 일치하는 것은 다릅니다.

## 안전 실패 대응

- 민감정보 출력: 마스킹·차단
- 외부 쓰기: 사용자 승인
- 근거 없음: 답변 보류
- 형식 실패: 제한 재시도
- 반복 실패: 사람 검토

## 버전 관리

모델 ID, Prompt hash, tool schema, 평가셋, 파라미터와 날짜를 함께 기록합니다. 모델 이름만으로 같은 결과를 재현할 수 없습니다.

---

<!-- SOURCE: 00_비전공자_GPT_생성워크북.md -->

# Chapter 14 비전공자용 GPT 생성 워크북

## GPT는 한 토큰씩 이어 쓰는 모델이다

GPT는 Decoder-only Transformer로, 앞에서 주어진 토큰을 조건으로 다음 토큰 확률을 계산합니다. 선택된 토큰을 입력 뒤에 붙이고 같은 과정을 반복하면 문장이 됩니다.

$$
P(x_1,\ldots,x_T)=\prod_{t=1}^{T}P(x_t\mid x_{<t})
$$

긴 식처럼 보이지만 “첫 단어부터 마지막 단어까지, 매 순간 앞부분을 보고 다음 단어를 고른다”는 뜻입니다.

## Causal Mask는 정답 미리 보기를 막는다

학습 데이터에는 문장 전체가 있지만 현재 위치가 미래 토큰을 보면 다음 토큰 예측 문제가 너무 쉬워집니다. Causal Mask는 현재 위치보다 오른쪽을 가려 실제 생성 조건과 맞춥니다.

## Temperature는 점수 차이를 조절한다

$$
P_i=\frac{e^{z_i/T}}{\sum_j e^{z_j/T}}
$$

- (T<1): 높은 점수를 더 강조해 결과가 안정적이 됩니다.
- (T>1): 점수 차이가 완만해져 다양한 토큰이 선택될 수 있습니다.
- (T=0)은 구현마다 Greedy 선택으로 별도 처리될 수 있습니다.

사실 확인이나 분류처럼 일관성이 중요하면 낮게, 아이디어 탐색처럼 다양성이 중요하면 조금 높게 설정하고 고정 평가 질문으로 비교합니다.

## Top-k와 Top-p는 후보를 줄인다

Top-k는 확률이 높은 상위 (k)개만 남깁니다. Top-p는 누적 확률이 (p)에 도달할 때까지 후보를 남깁니다. 두 설정은 답의 정확도를 보장하지 않으며 생성 다양성을 조절하는 장치입니다.

## 프롬프트는 작업 계약서처럼 쓴다

```text
역할: 고객 문의 분류 담당자
목표: 문의를 배송/환불/결제/기타 중 하나로 분류
입력: 사용자 문의 한 문장
제약: 입력에 없는 사실을 추가하지 않음
출력: {"label": "...", "reason": "..."}
```

좋은 프롬프트는 긴 문장이 아니라 목표·입력·제약·출력 형식이 분명한 문장입니다.

## 구조화 출력도 검증이 필요하다

모델이 JSON처럼 보이는 문자열을 반환해도 필수 Key, 자료형, 허용 Label을 프로그램에서 확인해야 합니다. 검증 실패는 무조건 같은 요청을 반복하지 말고 오류 유형에 따라 재시도하거나 사용자에게 알립니다.

## Hallucination을 세 종류로 나누기

- 사실 오류: 존재하지 않는 사실을 생성
- 근거 오류: 제시된 문서와 다른 내용 생성
- 형식 오류: 요청한 Schema나 제한을 위반

오류 종류를 구분해야 프롬프트, 검색, 검증 코드 중 어디를 고칠지 판단할 수 있습니다.

## API 실습에서 남길 기록

- 모델과 프롬프트 버전
- Temperature 등 생성 설정
- 입력·출력 토큰 수
- 응답 시간과 오류 유형
- 민감정보 제거 여부

API Key는 코드와 CSV에 기록하지 않고 환경 변수에서 읽습니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 14 원리·수학·실습 가이드

## 1. Decoder-only와 자기회귀

GPT는 이전 토큰만 보고 다음 토큰을 예측한다.

$$
P(x_1,\dots,x_T)=\prod_{t=1}^{T}P(x_t\mid x_{<t})
$$

Causal mask 때문에 학습 중에도 미래 정답을 볼 수 없다. 다음 토큰 교차 엔트로피를 줄이는 과정에서 문법·지식·패턴을 학습한다.

## 2. 생성 제어

Temperature는 로짓을 Softmax에 넣기 전 나눈다.

$$
p_i=\frac{\exp(z_i/\tau)}{\sum_j\exp(z_j/\tau)}
$$

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

$$
P(x_1,\ldots,x_T)=\prod_{t=1}^{T}P(x_t|x_{<t})
$$

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

$$
요청비용=입력토큰\times입력단가+출력토큰\times출력단가
$$

실제 단가는 모델마다 바뀌므로 공식 가격표를 확인합니다. 예제에서는 입력·출력 토큰을 따로 기록해 프롬프트가 길어졌을 때 비용 변화를 설명합니다.

## 안전한 API 사용

API 키는 코드와 Markdown에 적지 않고 환경변수나 secret manager에 저장합니다. 로그에는 개인정보와 전체 프롬프트를 무조건 남기지 않습니다. timeout, 재시도 횟수, rate limit 처리와 요청 ID를 관리합니다.

## 생성 평가

정답이 하나인 분류와 달리 생성은 여러 좋은 답이 가능합니다. 사실성, 지시 준수, 형식, 유해성, 근거성, 길이, 비용과 지연을 평가표로 분리합니다.

---

<!-- SOURCE: 03_Summary_and_Quiz.md -->

# 퀴즈
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

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

CSV의 고객 문의를 읽어 간결한 답변 초안을 생성하고 요청 설정과 결과를 JSONL로 저장합니다.

- [안내](examples/04_gpt_api_solution/README.md)
- [코드](examples/04_gpt_api_solution/gpt_api_example.py)
- [입력](examples/04_gpt_api_solution/questions.csv)

현재 공식 모델 안내의 비용 민감형 모델을 기본값으로 사용하지만 `OPENAI_MODEL` 환경변수로 교체할 수 있습니다.

## 실습 목표

CSV 질문을 API에 보내 구조화된 답을 받고, 성공·실패·토큰·지연을 파일로 저장합니다. API 키는 환경변수로만 관리합니다.

## 요청 함수

```python
import os
import time
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def ask(question):
    started = time.perf_counter()
    response = client.responses.create(
        model=os.environ.get("OPENAI_MODEL", "사용할-모델"),
        input=f"질문에 간결히 답하세요.\n질문: {question}",
    )
    return response.output_text, time.perf_counter() - started
```

모델 이름과 API 형식은 실습 시점 공식 문서를 확인합니다.

## 질문 CSV

```csv
id,question,expected_keyword
q01,배송 기간은?,영업일
q02,환불 절차는?,취소
```

정답 문장 전체 일치보다 필수 키워드·JSON schema·근거 포함처럼 평가 가능한 조건을 둡니다.

## 실패 처리

- 인증·잘못된 요청: 재시도하지 않고 설정 수정
- timeout·일시적 rate limit: 제한 횟수 backoff
- JSON 실패: 파싱 오류 기록 후 한 번 재요청
- 근거 없음: 답변 보류

## 결과 파일

```text
id,model,prompt_version,output,passed,latency,error
```

개인정보와 API 키가 결과 파일에 들어가지 않게 합니다.

## 프롬프트 비교

Zero-shot과 Few-shot을 같은 질문으로 비교합니다. 정확도·형식 준수율·평균 입력 토큰·P95를 함께 봅니다.

## 완료 기준

최소 20개 질문, 오류 사례, 재시도 한도, 결과 CSV, 비용 추정, Prompt 버전과 안전 점검을 제출합니다.
