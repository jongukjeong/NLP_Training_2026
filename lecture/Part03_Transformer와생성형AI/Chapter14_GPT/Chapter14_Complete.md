# Chapter 14 통합 강의 원고

---

<!-- SOURCE: README.md -->

# Chapter 14. GPT

1. [Decoder Only와 Auto Regression](01_GPT_Architecture.md)
2. [Prompting·Text Generation·ChatGPT](02_Prompting_and_Generation.md)
3. [퀴즈](03_Summary_and_Quiz.md)
4. [실습: GPT API 활용](04_Practice.md)

API 실습은 OpenAI Responses API와 공식 Python SDK를 사용하며 키를 저장소에 저장하지 않습니다.

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

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
