# Chapter 9 통합 강의 원고

---

<!-- SOURCE: README.md -->

# Chapter 9. LSTM과 GRU

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **장단기 메모리(Long Short-Term Memory, LSTM): Gate로 장기 정보를 선택적으로 보존하는 RNN**
- **셀 상태(Cell State): LSTM이 긴 시간 동안 전달하는 핵심 기억**
- **게이트(Gate): 정보를 얼마나 보존·추가·출력할지 조절하는 장치**
- **게이트 순환 유닛(Gated Recurrent Unit, GRU): LSTM보다 단순한 Gate 구조를 사용하는 RNN**

1. [9.1~9.4 LSTM 구조와 세 Gate](01_LSTM_Gates.md)
2. [9.5 GRU와 모델 선택](02_GRU_and_Selection.md)
3. [9.6 감성 분석 파이프라인](03_Sentiment_Analysis.md)
4. [퀴즈](04_Summary_and_Quiz.md)
5. [실습: 감성 분석](05_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: LEARNING_PATH.md -->

# Chapter 9 비전공자 학습 경로

## 기본 도달 목표

같은 문장을 LSTM과 GRU로 실행해 결과 비교

완성형 코드를 처음부터 모두 이해하거나 다시 작성하는 것은 기본 목표가 아닙니다.

## 1. Step by Step — 강사와 함께

1. 입력 시퀀스를 확인한다
2. LSTM 출력 shape를 본다
3. GRU 출력 shape를 본다
4. 두 모델의 예측과 학습 시간을 비교한다

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

[05_Practice.md](05_Practice.md)의 기본 요구사항을 먼저 수행합니다. 막히면 전체 solution 대신 필요한 단계의 힌트만 확인합니다.

## 4. Solution — 피드백 후 공개

[examples/05_sentiment_solution/README.md](examples/05_sentiment_solution/README.md)은 다수의 수강생이 기본 요구사항을 시도하고 공통 오류를 함께 확인한 뒤 공개합니다. 자신의 코드와 다음 항목을 비교합니다.

1. 반복되는 처리를 어떻게 묶었는가
2. 잘못된 입력을 어디에서 검사하는가
3. 결과를 어떻게 검증하고 기록하는가

## 선택 확장

- 게이트 계산
- 양방향 모델
- 모델 선택
- 세부 평가

선택 확장은 기본 완료 기준에 포함하지 않습니다.

---

<!-- SOURCE: 00_LSTM_GRU_게이트_그림없이_이해하기.md -->

# Chapter 9 LSTM·GRU 게이트를 그림 없이 이해하기

## 게이트는 0과 1 사이의 수도꼭지다

LSTM의 gate는 완전히 열림/닫힘만 있는 스위치가 아니라 0~1 사이로 정보량을 조절하는 수도꼭지입니다. hidden size가 64라면 하나의 gate 값이 아니라 64개 값이 각각 다른 기억을 조절합니다.

## Forget gate

이전 기억 중 얼마나 남길지 결정합니다.

$$
f_t=\sigma(W_f[x_t,h_{t-1}]+b_f)
$$

이전 기억이 `[0.8,-0.4]`, forget gate가 `[0.9,0.2]`라면 남는 기억은 `[0.72,-0.08]`입니다. 첫 정보는 대부분 유지하고 둘째는 대부분 잊습니다.

## Input gate

새 후보 기억을 얼마나 기록할지 결정합니다.

$$
i_t=\sigma(...),\qquad \tilde c_t=\tanh(...)
$$

후보가 `[0.5,-0.7]`, input gate가 `[0.4,0.8]`이면 새로 쓰는 양은 `[0.2,-0.56]`입니다.

## Cell state 갱신

$$
c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t
$$

앞의 두 계산을 더하면 새 기억은 `[0.92,-0.64]`입니다. 곱셈으로 버릴 양과 쓸 양을 조절하고, 덧셈으로 기억 통로를 이어 갑니다.

## Output gate

기억 전체를 바로 밖으로 보여주지 않고 현재 단계에서 사용할 부분만 정합니다.

$$
h_t=o_t\odot\tanh(c_t)
$$

Cell state는 내부 장기 메모, hidden state는 현재 공개하는 요약이라고 이해할 수 있습니다.

## GRU는 무엇을 합쳤는가

GRU는 별도의 cell state 없이 hidden state 하나를 관리하고, update와 reset gate를 사용합니다. 문이 하나 적어 보통 파라미터와 계산량이 LSTM보다 작습니다.

```text
LSTM: forget + input + output + candidate
GRU:  update + reset + candidate
```

## 파라미터 수 비교

입력 차원 `D=128`, hidden `H=64`라면 대략:

$$
LSTM=4H(D+H+1)=49,408
$$

$$
GRU=3H(D+H+1)=37,056
$$

GRU가 약 25% 적습니다. 실제 구현의 bias 방식에 따라 조금 달라질 수 있습니다.

## 어느 모델을 선택할까

GRU는 빠른 기준선과 제한된 자원에서 좋은 출발점입니다. LSTM은 기억 제어가 더 세밀합니다. 데이터에 따라 결과가 달라 이름만으로 선택하지 않습니다.

| 항목 | SimpleRNN | GRU | LSTM |
|---|---|---|---|
| 파라미터 | 적음 | 중간 | 많음 |
| 장기 의존 | 약함 | 개선 | 개선 |
| 학습 속도 | 빠름 | 중간 | 상대적으로 느림 |
| 최종 선택 | 실제 검증 결과로 결정 | 실제 검증 결과로 결정 | 실제 검증 결과로 결정 |

## 감성 문장을 따라가기

“초반은 지루했지만 마지막은 정말 좋았다”에서 앞의 부정 감정만 기억하면 오분류합니다. gate는 뒤의 반전 표현을 새 기억으로 쓰고 이전 판단을 얼마나 남길지 학습합니다. 실제 gate가 사람이 기대한 방식과 정확히 일치한다고 단정하지는 않습니다.

## 비교 실험 규칙

동일 데이터 분할, tokenizer, 임베딩 차원, 비슷한 파라미터 예산, 같은 epoch 제한을 사용합니다. F1뿐 아니라 학습시간, 추론시간, 긴 문장 F1을 기록합니다.

## 확인 문제

1. forget gate 0은 어떤 뜻입니까?
2. cell state와 hidden state의 차이는?
3. GRU가 LSTM보다 가벼운 이유는?
4. 모델 이름만으로 성능을 결정할 수 없는 이유는?

---

<!-- SOURCE: 00_감성분석_평가와_모델선택.md -->

# Chapter 9 감성 분석 평가와 모델 선택

## 감성 레이블부터 점검하기

별점 1~2를 부정, 4~5를 긍정으로 만들 수 있지만 별점 3 처리와 리뷰 내용 불일치를 확인합니다. “배송은 별로지만 제품은 좋다”처럼 대상별 감성이 다를 수 있습니다.

## Challenge set

일반 test 외에 언어 현상별 작은 평가셋을 만듭니다.

| 유형 | 예문 |
|---|---|
| 부정 | 전혀 좋지 않다 |
| 반전 | 느리지만 결과는 만족 |
| 풍자 | 참 잘도 만들었다 |
| 강도 | 정말 너무 좋다 |
| 대상 혼합 | 배송은 나쁘고 제품은 좋다 |

유형별 Recall을 보면 모델이 어떤 표현에 약한지 알 수 있습니다.

## Threshold 조정

Sigmoid 확률 0.5는 기본값입니다. 부정 리뷰를 놓치는 비용이 크다면 validation PR curve에서 Recall 목표를 만족하는 threshold를 선택합니다.

## Calibration

모델이 0.9라고 예측한 사례 100개 중 실제 긍정이 약 90개인지 확인합니다. 과신 모델은 사용자에게 확률을 그대로 보여주면 위험합니다.

## LSTM과 GRU 비교

같은 hidden size는 파라미터 수가 다르므로 “같은 유닛” 비교와 “비슷한 파라미터” 비교를 구분합니다.

| 모델 | Hidden | Params | Val F1 | Challenge F1 | 시간 |
|---|---:|---:|---:|---:|---:|
| GRU | 기록 | 기록 | 기록 | 기록 | 기록 |
| LSTM | 기록 | 기록 | 기록 | 기록 | 기록 |

## Bidirectional 비용

두 방향 모델은 보통 출력과 파라미터가 늘어납니다. 완성 문장 분류에는 도움이 될 수 있지만 latency와 메모리를 측정합니다.

## Dropout 위치

Embedding 뒤, recurrent 출력 뒤, Dense 앞에 Dropout을 넣을 수 있습니다. `recurrent_dropout`은 GPU 최적화 경로에 영향을 줄 수 있으므로 무조건 켜지 않습니다.

## 긴 문장 오류

최대 길이로 잘린 비율과 잘린 위치를 확인합니다. 마지막 결론이 잘리는 리뷰는 앞부분만 보고 반대 감성을 예측할 수 있습니다.

## 도메인 이동

영화 리뷰로 학습한 모델을 상품 리뷰에 바로 적용하면 “무겁다”, “가볍다”의 의미가 달라질 수 있습니다. 새 도메인 라벨 샘플로 재평가합니다.

## 설명 가능한 결과 보고

전체 F1, 부정 Recall, challenge 유형별 성능, P95, 파라미터와 실제 오분류 문장 5개를 함께 보고합니다.

## 완료 기준

레이블 규칙, challenge set, threshold, calibration, LSTM/GRU 공정 비교, 도메인 이동 평가를 기록합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 9 원리·수학·실습 가이드

## 1. LSTM의 핵심 직관

LSTM은 기억 통로 `c_t`와 세 개의 문을 둔다. 문 값은 Sigmoid를 지나 0~1이 되며, 0은 막고 1은 통과시킨다는 뜻이다.

$$
f_t=\sigma(W_f[x_t,h_{t-1}]+b_f)
$$
$$
i_t=\sigma(W_i[x_t,h_{t-1}]+b_i),\quad \tilde c_t=\tanh(W_c[x_t,h_{t-1}]+b_c)
$$
$$
c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t
$$
$$
o_t=\sigma(W_o[x_t,h_{t-1}]+b_o),\quad h_t=o_t\odot\tanh(c_t)
$$

`f_t`는 이전 기억을 얼마나 남길지, `i_t`는 새 정보를 얼마나 쓸지, `o_t`는 기억을 현재 출력에 얼마나 보여줄지 정한다. `⊙`는 같은 위치끼리 곱하는 연산이다.

이전 기억 0.8, forget 0.9, 후보 기억 0.5, input 0.4라면 새 기억은 `0.9×0.8+0.4×0.5=0.92`다.

## 2. 왜 기울기가 덜 사라지는가

기억 상태가 덧셈 경로로 이어지므로 매 시점마다 비선형 변환만 연속해서 곱하는 SimpleRNN보다 정보와 기울기가 흐르기 쉽다. 완전히 해결되는 것은 아니며, 매우 긴 문장·부적절한 학습률에서는 여전히 문제가 생긴다.

## 3. GRU

GRU는 기억과 은닉 상태를 합치고 update/reset 두 문을 사용한다.

$$
z_t=\sigma(W_z[x_t,h_{t-1}]),\quad r_t=\sigma(W_r[x_t,h_{t-1}])
$$
$$
\tilde h_t=\tanh(W_h[x_t,r_t\odot h_{t-1}])
$$
$$
h_t=z_t\odot h_{t-1}+(1-z_t)\odot\tilde h_t
$$

여기서는 `z_t`를 이전 상태를 유지하는 비율로 정의한다. GRU는 보통
파라미터와 계산량이 적고, LSTM은 기억을 더 세밀하게 제어한다. 성능 우열은
데이터에 따라 달라 동일 분할과 예산으로 비교한다.

## 4. 감성 분석 구현

```python
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 128, mask_zero=True),
    tf.keras.layers.Bidirectional(tf.keras.layers.GRU(64)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])
```

양방향이면 출력 차원은 보통 `2H`가 된다. “재미는 있지만 다시 보진 않겠다”처럼 반전 접속사가 있는 문장을 따로 수집해 오류를 분석한다. 운영 입력이 실시간 스트림이면 미래 문맥을 쓰는 양방향 구조가 가능한지도 확인한다.

## 실험표

| 모델 | 은닉 크기 | 파라미터 | 검증 F1 | 긴 문장 F1 | 추론시간 |
|---|---:|---:|---:|---:|---:|
| SimpleRNN | 64 | 기록 | 기록 | 기록 | 기록 |
| GRU | 64 | 기록 | 기록 | 기록 | 기록 |
| LSTM | 64 | 기록 | 기록 | 기록 | 기록 |

1. forget gate가 0에 가까우면 이전 기억은 어떻게 되는가?
2. 양방향 64유닛의 출력 차원은 보통 얼마인가?
3. 모델 비교에서 정확도 외에 무엇을 기록해야 하는가?

---

<!-- SOURCE: 01_LSTM_Gates.md -->

# 9.1 LSTM 구조 · 9.2~9.4 Gate

## 9.1 LSTM이 필요한 이유

기본 RNN은 문장을 왼쪽에서 오른쪽으로 읽으면서 이전 hidden state를 계속
갱신합니다. 문장이 길어지면 오래전 정보가 여러 번의 연산을 거쳐야 하므로
정보와 기울기가 작아지는 **기울기 소실(vanishing gradient)** 문제가 생길 수
있습니다.

LSTM(Long Short-Term Memory)은 기본 RNN에 다음 두 장치를 추가합니다.

1. 오래 전달할 정보를 담는 별도의 **cell state**를 둡니다.
2. 세 개의 **gate**가 정보를 지울지, 쓸지, 보여 줄지를 조절합니다.

예를 들어 “이 영화는 중간까지 지루했지만 **마지막은 정말 좋았다**”라는
문장을 읽는다고 생각해 봅시다. LSTM은 앞부분의 부정 정보와 뒷부분의 긍정
정보를 모두 상태에 반영하고, 학습된 gate를 통해 최종 판단에 필요한 정보를
선택합니다. Gate가 문법 규칙을 직접 아는 것은 아니며, 학습 과정에서 유용한
값을 내도록 파라미터가 조정됩니다.

## LSTM의 두 상태

| 상태 | 역할 | 직관 |
|---|---|---|
| cell state `c_t` | 비교적 긴 시간 전달되는 내부 기억 | 메모장 |
| hidden state `h_t` | 현재 시점의 출력이자 다음 시점의 입력 | 지금 보여 주는 요약 |

기본 RNN이 하나의 hidden state에 기억과 출력을 모두 담는다면, LSTM은
`c_t`와 `h_t`로 역할을 나눕니다. 여기서 “장기 기억”과 “단기 기억”은 이해를
돕는 표현입니다. 실제 상태는 사람이 읽을 수 있는 문장이 아니라 학습된
실수 벡터입니다.

한 시점 `t`에서 LSTM은 이전 상태 `h_{t-1}`, `c_{t-1}`와 현재 입력 `x_t`를
받아 새 상태 `h_t`, `c_t`를 만듭니다.

```text
(현재 입력 x_t, 이전 출력 h_{t-1}, 이전 기억 c_{t-1})
                         │
                         ▼
              forget → input → output gate
                         │
                         ▼
                   (새 출력 h_t, 새 기억 c_t)
```

## 세 Gate의 역할

- Forget Gate: 이전 cell state에서 무엇을 유지할지 결정
- Input Gate: 새 후보 정보를 얼마나 기록할지 결정
- Output Gate: cell state에서 현재 hidden state로 무엇을 노출할지 결정

Gate는 sigmoid 값 0~1로 정보 흐름을 조절하고 후보 state는 주로 tanh를 사용합니다. “기억한다”는 설명은 직관이며 실제로는 데이터에서 학습된 연속값 연산입니다.

## 세 게이트의 전체 식

$$
f_t=\sigma(W_f[x_t;h_{t-1}]+b_f)
$$
$$
i_t=\sigma(W_i[x_t;h_{t-1}]+b_i),\quad
\tilde c_t=\tanh(W_c[x_t;h_{t-1}]+b_c)
$$
$$
c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t
$$
$$
o_t=\sigma(W_o[x_t;h_{t-1}]+b_o),\quad
h_t=o_t\odot\tanh(c_t)
$$

세 Sigmoid 게이트는 각 기억 차원마다 0~1 값을 냅니다. 하나의 스위치가 아니라 64유닛이면 64개의 연속적인 조절 손잡이가 있는 셈입니다.

계산 순서를 말로 풀면 다음과 같습니다.

1. `f_t`로 이전 기억 `c_{t-1}` 중 남길 양을 정합니다.
2. `i_t`로 새 후보 기억 `c̃_t` 중 기록할 양을 정합니다.
3. 두 결과를 더해 새 cell state `c_t`를 만듭니다.
4. `o_t`로 새 기억 중 현재 hidden state `h_t`로 보여 줄 양을 정합니다.

## 9.2 Forget Gate: 이전 기억을 얼마나 남길까?

Forget Gate(망각 게이트)는 이전 cell state에 곱할 비율 `f_t`를 만듭니다.

$$
f_t=\sigma(W_f[x_t;h_{t-1}]+b_f)
$$

`f_t`는 이름과 달리 “잊을 양”이 아니라 **남길 양**입니다.

- `f_t ≈ 0`: 이전 기억을 거의 지웁니다.
- `f_t ≈ 1`: 이전 기억을 거의 그대로 유지합니다.
- `f_t ≈ 0.5`: 이전 기억의 절반 정도를 전달합니다.

예를 들어 이전 기억이 `[0.8, -0.4, 0.2]`이고 gate가
`[0.9, 0.1, 0.5]`라면 유지되는 기억은 `[0.72, -0.04, 0.10]`입니다.
Gate는 벡터의 모든 값을 한꺼번에 켜고 끄는 스위치가 아니라, 각 차원을
서로 다른 비율로 조절합니다.

[02_forget_gate.py](02_forget_gate.py)를 실행하면 같은 기억에 0.1, 0.5,
0.9를 각각 곱했을 때의 차이를 확인할 수 있습니다.

```bash
python 02_forget_gate.py
```

기억 상태에 대한 직접 미분에는 `f_t`가 나타납니다.

$$
\frac{\partial c_t}{\partial c_{t-1}}=f_t
$$

필요한 구간에서 `f_t`가 1에 가까우면 기억과 기울기가 비교적 잘
유지됩니다. 항상 1이면 불필요한 기억까지 쌓이므로 입력에 따라 적절한 값을
내도록 학습되어야 합니다.

## 9.3 Input Gate: 새 정보를 얼마나 기록할까?

Input Gate(입력 게이트)는 새 후보 기억 중 실제 cell state에 기록할 양을
정합니다.

$$
i_t=\sigma(W_i[x_t;h_{t-1}]+b_i)
$$

$$
\tilde c_t=\tanh(W_c[x_t;h_{t-1}]+b_c)
$$

여기에는 역할이 다른 두 값이 있습니다.

- 후보 기억 `c̃_t`: 새로 기록할 **내용**이며, 보통 -1~1의 값을 가집니다.
- input gate `i_t`: 그 내용을 기록할 **비율**이며, 0~1의 값을 가집니다.

따라서 `i_t` 자체가 새 기억은 아닙니다. 실제로 추가되는 정보는
`i_t ⊙ c̃_t`입니다. 예를 들어 후보 기억이 `-0.5`일 때 `i_t=0.3`이면
cell state에는 `-0.15`만 추가됩니다.

[03_input_gate.py](03_input_gate.py)는 같은 후보 기억에 input gate를
0.0, 0.3, 1.0으로 바꾸어 적용합니다.

```bash
python 03_input_gate.py
```

Forget Gate와 Input Gate의 결과를 합치면 새 cell state가 됩니다.

$$
c_t=\underbrace{f_t\odot c_{t-1}}_{\text{남긴 이전 기억}}
    +\underbrace{i_t\odot\tilde c_t}_{\text{기록할 새 기억}}
$$

## 9.4 Output Gate: 기억 중 무엇을 보여 줄까?

Output Gate(출력 게이트)는 갱신된 cell state 중 현재 hidden state로
노출할 양을 정합니다.

$$
o_t=\sigma(W_o[x_t;h_{t-1}]+b_o)
$$

$$
h_t=o_t\odot\tanh(c_t)
$$

cell state를 `tanh`로 -1~1 범위에 놓고 output gate를 곱합니다. 따라서
cell state에 정보가 남아 있어도 `o_t`가 0에 가까우면 현재 출력에는 거의
보이지 않습니다. 정보가 삭제된 것은 아니므로 다음 시점의 cell state로는
계속 전달될 수 있습니다.

[04_output_gate.py](04_output_gate.py)는 동일한 cell state에서 output
gate만 변경했을 때 hidden state가 어떻게 달라지는지 보여 줍니다.

```bash
python 04_output_gate.py
```

> **헷갈리기 쉬운 차이:** Forget Gate는 이전 `cell`을 바꾸고, Input
> Gate는 새 `cell`을 만드는 데 참여합니다. Output Gate는 완성된 `cell`을
> 삭제하지 않고 현재 `hidden`으로 보여 줄 양만 조절합니다.

## 세 Gate를 숫자로 함께 계산하기

한 차원만 보겠습니다.

- 이전 기억 `c_{t-1}=0.6`
- forget gate `f_t=0.8`
- input gate `i_t=0.3`
- 후보 기억 `c̃_t=-0.5`

$$
c_t=0.8\times0.6+0.3\times(-0.5)=0.33
$$

이전 기억 0.48을 남기고 새 부정 정보 -0.15를 반영했습니다. output gate가 0.7이면 `h_t=0.7×tanh(0.33)≈0.223`입니다.

## 예제 코드: 한 단계씩 상태 추적하기

[01_lstm_state.py](01_lstm_state.py)는 외부 라이브러리 없이 스칼라 하나로
forget/input/output gate와 두 상태의 변화를 출력합니다.

```bash
python 01_lstm_state.py
```

```python
forget = sigmoid(value + hidden + 1.0)
input_gate = sigmoid(value - hidden)
candidate = math.tanh(value + hidden)
output_gate = sigmoid(value + hidden)

cell = forget * cell + input_gate * candidate
hidden = output_gate * math.tanh(cell)
```

실제 LSTM은 위 값들이 스칼라가 아니라 벡터이고, 각 식에 서로 다른
가중치 행렬과 bias를 사용합니다. 예제는 학습 모델을 대신하는 코드가 아니라
`c_t = f_t c_{t-1} + i_t c̃_t`가 어떤 순서로 실행되는지 확인하기 위한
축소 모형입니다.

출력에서 다음을 확인합니다.

- `forget`이 1에 가까울수록 이전 `cell`이 많이 남습니다.
- `input`이 1에 가까울수록 `candidate`가 새 기억에 많이 반영됩니다.
- `output`은 `cell` 전체가 아니라 현재 `hidden`으로 노출할 양을 정합니다.

## Keras에서 LSTM 사용하기

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=10_000, output_dim=128, mask_zero=True),
    tf.keras.layers.LSTM(64, dropout=0.2),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])
```

입력 shape이 `(batch, time)`이면 Embedding을 거쳐 `(batch, time, 128)`이
되고, `LSTM(64)`의 최종 출력은 `(batch, 64)`가 됩니다. 이 예에서는 마지막
Dense 층이 그 64차원 문장 표현으로 긍정 확률 하나를 예측합니다.

전체 문장을 이용하는 감성 분류에서는 다음과 같이 Bidirectional LSTM도
사용할 수 있습니다.

```python
tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, dropout=0.2))
```

양방향 모델은 앞뒤 문맥을 모두 보지만 latency와 파라미터 수가 증가합니다.

## 파라미터 수 계산

입력 차원 `D`, 은닉 크기 `H`인 LSTM은 네 종류의 계산을 하므로 대략 다음 파라미터를 가집니다.

$$
4H(D+H+1)
$$

`D=128`, `H=64`이면 `4×64×(128+64+1)=49,408`개입니다. 같은 크기의 SimpleRNN `H(D+H+1)=12,352`개보다 약 4배입니다. Bidirectional이면 방향별 층이 따로 있어 약 2배가 됩니다.

## LSTM 출력 설정

```python
lstm = tf.keras.layers.LSTM(
    64,
    return_sequences=True,
    return_state=True,
    dropout=0.2,
    recurrent_dropout=0.0,
)
sequence, h, c = lstm(vectors, mask=mask)
```

`sequence`는 `(B,T,64)`, `h`와 `c`는 `(B,64)`입니다. GPU 최적화 경로는 설정에 따라 달라질 수 있으므로 `recurrent_dropout`을 무조건 켜기보다 속도와 성능을 측정합니다.

## 양방향 모델의 정보 누수 판단

완성된 리뷰의 감성 분류는 미래 토큰을 봐도 되므로 양방향이 자연스럽습니다. 반면 타이핑 중 다음 단어 예측이나 실시간 스트림 판단은 미래 입력이 없으므로 양방향 결과를 그대로 사용할 수 없습니다. 학습 성능보다 운영 시점에 실제로 이용 가능한 정보인지 먼저 확인합니다.

## 감성 분석 오류 유형

| 유형 | 예문 | 점검 |
|---|---|---|
| 부정 | 재미있지 않다 | 부정어 범위 |
| 반전 | 느리지만 결과는 좋다 | 뒤 절의 영향 |
| 강도 | 정말 매우 좋다 | 정도 부사 |
| 풍자 | 참 잘도 만들었다 | 표면과 의도 차이 |
| 도메인 | 배터리가 가볍다 | 도메인별 의미 |

전체 정확도뿐 아니라 이 도전 세트의 정확도를 따로 기록합니다.

## 확인 문제

1. LSTM이 `h`와 `c`를 구분하는 이유를 설명하세요.
2. Forget Gate 값이 0과 1에 가까울 때 이전 기억은 각각 어떻게 됩니까?
3. 후보 기억 `c̃_t`와 Input Gate `i_t`의 역할 차이를 설명하세요.
4. Output Gate가 0에 가까우면 cell state의 정보도 삭제되는지 설명하세요.
5. `D=100`, `H=32`인 LSTM의 파라미터 수를 계산하세요.
6. 양방향 LSTM을 사용할 수 없는 운영 사례를 제시하세요.

---

<!-- SOURCE: 02_GRU_and_Selection.md -->

# 9.5 GRU와 모델 선택

## GRU는 LSTM과 무엇이 다른가?

GRU(Gated Recurrent Unit)는 LSTM처럼 긴 문맥을 다루기 위해 gate를
사용하지만, 별도의 cell state 없이 hidden state 하나만 관리합니다.

| LSTM | GRU |
|---|---|
| hidden state와 cell state | hidden state 하나 |
| forget, input, output gate | update, reset gate |
| 네 종류의 주요 변환 | 세 종류의 주요 변환 |

구조가 단순한 GRU는 같은 입력·은닉 크기의 LSTM보다 파라미터가 적고 빠를
수 있습니다. 그러나 데이터에 따라 결과가 달라 항상 더 우수하거나 열등한
모델은 아닙니다.

## 두 Gate의 역할

- **Update Gate `z_t`**: 이전 상태를 얼마나 유지할지 정합니다.
- **Reset Gate `r_t`**: 후보 상태를 만들 때 이전 상태를 얼마나 참고할지
  정합니다.

LSTM의 forget/input gate가 이전 기억과 새 기억을 나누어 조절한다면,
GRU의 update gate는 하나의 비율로 이전 상태와 후보 상태를 섞습니다.

비교 기준:

- validation 성능과 반복 간 분산
- 학습·추론 시간
- 모델 크기와 메모리
- sequence 길이
- 운영 latency

동일한 split, vocabulary, embedding dimension, seed와 평가 지표를 사용해 비교합니다.

```python
rnn = layers.GRU(64)       # 또는 layers.LSTM(64)
```

모델 이름보다 데이터와 평가 설계가 중요합니다.

## GRU 전체 계산

$$
z_t=\sigma(W_zx_t+U_zh_{t-1}),\quad
r_t=\sigma(W_rx_t+U_rh_{t-1})
$$
$$
\tilde h_t=\tanh(W_hx_t+U_h(r_t\odot h_{t-1}))
$$
$$
h_t=z_t\odot h_{t-1}+(1-z_t)\odot\tilde h_t
$$

이 문서에서는 `z_t`를 **이전 상태를 유지하는 비율**로 정의합니다.
따라서 `z_t`가 1에 가까우면 이전 상태를 많이 남기고, 0에 가까우면 후보
상태를 많이 반영합니다. 문헌에 따라 `z_t`와 `1-z_t`의 이름을 반대로
정의하기도 하므로 식을 함께 확인해야 합니다.

Reset Gate는 후보 상태를 계산하는 과정에 먼저 사용됩니다.

- `r_t ≈ 0`: 이전 상태를 거의 무시하고 현재 입력 중심으로 후보를 만듭니다.
- `r_t ≈ 1`: 이전 상태를 충분히 참고하여 후보를 만듭니다.

## 파라미터 비교

GRU는 대략 `3H(D+H+1)`, LSTM은 `4H(D+H+1)`입니다. `D=128,H=64`이면 GRU는 약 37,056개, LSTM은 약 49,408개입니다. 실제 수는 bias 구현에 따라 조금 다를 수 있으므로 `model.summary()`로 확인합니다.

## 공정한 선택 실험

동일 tokenizer, embedding, split, seed, batch와 비슷한 파라미터 예산을 사용합니다. 최고 validation F1, test F1, epoch당 시간, peak memory, 긴 문장 성능을 비교합니다. 한 번 실행의 작은 차이보다 여러 seed의 평균과 변동을 봅니다.

## 선택 기준

GRU는 제한된 자원과 빠른 반복에서 좋은 출발점입니다. LSTM은 더 세밀한 기억 제어가 도움이 되는지 실험합니다. Transformer와도 비교하되 데이터 크기, 지연 요구와 설명 가능성을 포함합니다.

## Update gate 숫자 예

GRU의 새 상태는 과거 상태와 후보 상태를 섞습니다.

$$
h_t=z_t\odot h_{t-1}+(1-z_t)\odot\tilde h_t
$$

이전 상태가 0.8, 후보가 -0.2, update gate가 0.75이면 새 상태는
`0.75×0.8+0.25×(-0.2)=0.55`입니다. 과거 정보를 더 많이 유지했습니다.

## Reset gate

후보 상태를 만들 때 과거 상태를 얼마나 참고할지 조절합니다. Reset이 0에 가까우면 과거를 거의 무시하고 현재 입력 중심의 후보를 만듭니다.

## 예제 코드: Update와 Reset Gate 비교

[05_gru.py](05_gru.py)는 다음 두 실험을 차례로 수행합니다.

1. 후보 상태를 고정하고 update gate에 따라 이전 상태가 얼마나 남는지
   비교합니다.
2. 현재 입력을 고정하고 reset gate에 따라 후보 상태가 어떻게 달라지는지
   비교합니다.

```bash
python 05_gru.py
```

첫 번째 결과에서는 update gate가 커질수록 새 hidden state가 이전 상태
`0.7`에 가까워집니다. 두 번째 결과에서는 reset gate가 커질수록 후보 상태를
만들 때 이전 hidden state의 영향이 커집니다. 이 코드는 gate의 역할을
확인하기 위한 스칼라 축소 모형이며, 실제 GRU는 학습된 행렬로 벡터 전체를
계산합니다.

## 실제 파라미터 확인

```python
lstm = tf.keras.Sequential([
    layers.Embedding(vocab_size, 128),
    layers.LSTM(64),
])
gru = tf.keras.Sequential([
    layers.Embedding(vocab_size, 128),
    layers.GRU(64),
])
lstm.build((None, max_length))
gru.build((None, max_length))
print(lstm.count_params(), gru.count_params())
```

Embedding 파라미터가 공통으로 포함되므로 recurrent 층만 비교할 때는 `layer.count_params()`를 확인합니다.

## 공정한 예산 비교

같은 hidden size 비교와 비슷한 파라미터 수 비교를 둘 다 수행합니다. GRU hidden을 조금 늘리면 LSTM과 유사한 총 파라미터가 될 수 있습니다.

## 선택 기준표

| 상황 | 먼저 시도할 후보 | 확인 |
|---|---|---|
| 빠른 기준선 | GRU | 속도·F1 |
| 긴 의존성 | LSTM·GRU 모두 | 긴 문장 F1 |
| 매우 낮은 지연 | 작은 GRU/평균풀링 | P95 |
| 완성 문장 분류 | Bidirectional 후보 | 미래 정보 허용 여부 |

최종 선택은 이름이 아니라 동일 평가셋 결과로 합니다.

---

<!-- SOURCE: 03_Sentiment_Analysis.md -->

# 9.6 감성 분석 파이프라인

감성 label은 주관적일 수 있으므로 annotation 기준과 불일치 사례를 기록합니다. 부정어, 반어, 복합 감정과 도메인 표현을 오류 분석에서 별도로 확인합니다.

```text
TextVectorization → Embedding(mask_zero=True)
→ Bidirectional LSTM/GRU → Dropout → sigmoid
```

평가 시 accuracy와 함께 precision, recall, F1, confusion matrix를 봅니다. 같은 상품·사용자의 거의 동일한 리뷰가 train/test에 나뉘지 않도록 중복 그룹을 고려합니다.

작은 데이터의 높은 점수는 일반화를 의미하지 않습니다. 실제 배포 전 시간·도메인 기준 holdout이 필요합니다.

[06_sentiment_pipeline.py](06_sentiment_pipeline.py)는 9.1~9.5에서 살펴본
순차 상태 갱신을 두 개의 짧은 감성 문장에 적용합니다.

```bash
python 06_sentiment_pipeline.py
```

“배송이 느리지만 제품은 좋아요”와 “제품은 좋지만 배송이 느려요”처럼
비슷한 단어가 들어 있어도 순서와 마지막 정보에 따라 상태와 예측이 달라지는
것을 확인합니다. 이 코드는 Gate의 직관을 위한 규칙 기반 축소 모형이며,
학습된 LSTM·GRU 감성 분류기는 아닙니다. 실제 모델 구조는 아래 Keras
예제를 사용합니다.

## 데이터 설계

평점으로 감성 레이블을 자동 생성할 때 중간 평점 처리와 반어적 리뷰를 점검합니다. 동일 사용자의 반복 리뷰나 거의 같은 문장이 분할을 넘어가면 누수됩니다.

## 전처리의 균형

느낌표, 이모지, 반복 문자, 부정 표현은 감성 신호일 수 있으므로 일괄 제거하지 않습니다. 미등록어 비율과 truncation 비율을 train/validation/test별로 기록합니다.

## 확률과 calibration

Sigmoid 0.9가 실제로 약 90% 정확한지를 calibration curve로 확인할 수 있습니다. 확률이 과신되어 있다면 임계값과 사용자 표시 정책에 영향을 줍니다.

## 도전 평가셋

부정, 반전, 풍자, 도메인 용어, 매우 긴 문장으로 작은 challenge set을 만듭니다. 일반 test F1과 함께 보고 모델이 어떤 언어 현상을 아직 못 다루는지 설명합니다.

## 운영 관점

오분류 비용이 대칭인지 확인합니다. 부정 리뷰 누락과 긍정 리뷰 오탐의 업무 비용이 다르면 PR 곡선에서 임계값을 정하고 모호한 구간은 사람 검토로 보냅니다.

## 데이터 준비 흐름

```text
리뷰 원문 → 중복 제거 → 레이블 규칙 → 그룹 분할
→ tokenizer fit(train만) → padding → 모델 학습 → 오류 분석
```

별점에서 레이블을 만들면 별점 3의 처리와 내용·별점 불일치를 표본 검사합니다.

## 모델 코드

```python
model = tf.keras.Sequential([
    layers.Embedding(vocab_size, 128, mask_zero=True),
    layers.Bidirectional(layers.GRU(64)),
    layers.Dropout(0.3),
    layers.Dense(1, activation="sigmoid"),
])
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"],
)
```

양방향 GRU의 출력은 보통 정방향·역방향을 연결해 128차원입니다.

## 임계값 선택

```python
from sklearn.metrics import precision_recall_curve

precision, recall, thresholds = precision_recall_curve(y_valid, prob_valid)
```

부정 리뷰를 놓치지 않는 것이 중요하면 목표 Recall을 만족하는 threshold를 validation에서 찾습니다. Test에서 고르면 성능이 과대평가됩니다.

## Challenge set 평가

부정, 반전, 풍자, 대상 혼합, 긴 문장을 각 20개 이상 준비합니다. 전체 test가 좋아도 “느리지만 결과는 좋다” 같은 반전 문장에서 실패할 수 있습니다.

## 확신하며 틀린 사례

예측 확률이 0.9 이상인데 오답인 리뷰를 먼저 읽습니다. 잘못된 레이블, 데이터 누수, 특정 키워드 편향을 찾기 쉽습니다.

## 운영 출력

확률이 모호한 구간은 `uncertain`으로 보내 사람 검토를 받을 수 있습니다. 긍정/부정만 강제로 반환하는 것보다 업무 위험을 줄일 수 있습니다.

---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 퀴즈
1. LSTM이 hidden state 외에 유지하는 state는? **cell state**
2. Forget Gate의 역할은? **이전 cell 정보 유지량 결정**
3. Input Gate의 역할은? **새 정보 기록량 결정**
4. Output Gate의 역할은? **현재 hidden state 노출량 결정**
5. GRU의 대표 장점은? **구조와 파라미터가 상대적으로 단순함**
6. LSTM과 GRU 비교 시 고정할 조건은? **split, 전처리, 차원, seed, 지표 등**
7. 반어가 감성 분석에서 어려운 이유는? **표면 단어와 실제 감정 방향이 다를 수 있음**

---

<!-- SOURCE: 05_Practice.md -->

# 실습: 감성 분석

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

같은 데이터와 설정에서 LSTM과 GRU를 학습하고 테스트 지표를 비교합니다.

- [안내](examples/05_sentiment_solution/README.md)
- [완성 코드](examples/05_sentiment_solution/sentiment_compare.py)
- [데이터셋](examples/05_sentiment_solution/reviews.csv)
