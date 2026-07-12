# Chapter 9 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 9. LSTM과 GRU

1. [LSTM 구조와 세 Gate](01_LSTM_Gates.md)
2. [GRU와 모델 선택](02_GRU_and_Selection.md)
3. [감성 분석 설계](03_Sentiment_Analysis.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: 감성 분석](05_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 9 원리·수학·실습 가이드

## 1. LSTM의 핵심 직관

LSTM은 기억 통로 `c_t`와 세 개의 문을 둔다. 문 값은 Sigmoid를 지나 0~1이 되며, 0은 막고 1은 통과시킨다는 뜻이다.

\[
f_t=\sigma(W_f[x_t,h_{t-1}]+b_f)
\]
\[
i_t=\sigma(W_i[x_t,h_{t-1}]+b_i),\quad \tilde c_t=\tanh(W_c[x_t,h_{t-1}]+b_c)
\]
\[
c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t
\]
\[
o_t=\sigma(W_o[x_t,h_{t-1}]+b_o),\quad h_t=o_t\odot\tanh(c_t)
\]

`f_t`는 이전 기억을 얼마나 남길지, `i_t`는 새 정보를 얼마나 쓸지, `o_t`는 기억을 현재 출력에 얼마나 보여줄지 정한다. `⊙`는 같은 위치끼리 곱하는 연산이다.

이전 기억 0.8, forget 0.9, 후보 기억 0.5, input 0.4라면 새 기억은 `0.9×0.8+0.4×0.5=0.92`다.

## 2. 왜 기울기가 덜 사라지는가

기억 상태가 덧셈 경로로 이어지므로 매 시점마다 비선형 변환만 연속해서 곱하는 SimpleRNN보다 정보와 기울기가 흐르기 쉽다. 완전히 해결되는 것은 아니며, 매우 긴 문장·부적절한 학습률에서는 여전히 문제가 생긴다.

## 3. GRU

GRU는 기억과 은닉 상태를 합치고 update/reset 두 문을 사용한다.

\[
z_t=\sigma(W_z[x_t,h_{t-1}]),\quad r_t=\sigma(W_r[x_t,h_{t-1}])
\]
\[
\tilde h_t=\tanh(W_h[x_t,r_t\odot h_{t-1}])
\]
\[
h_t=(1-z_t)\odot h_{t-1}+z_t\odot\tilde h_t
\]

GRU는 보통 파라미터와 계산량이 적고, LSTM은 기억을 더 세밀하게 제어한다. 성능 우열은 데이터에 따라 달라 동일 분할과 예산으로 비교한다.

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

LSTM은 hidden state와 별도의 cell state를 유지해 긴 의존성 학습을 돕습니다.

- Forget Gate: 이전 cell state에서 무엇을 유지할지 결정
- Input Gate: 새 후보 정보를 얼마나 기록할지 결정
- Output Gate: cell state에서 현재 hidden state로 무엇을 노출할지 결정

Gate는 sigmoid 값 0~1로 정보 흐름을 조절하고 후보 state는 주로 tanh를 사용합니다. “기억한다”는 설명은 직관이며 실제로는 데이터에서 학습된 연속값 연산입니다.

```python
layers.Bidirectional(layers.LSTM(64, dropout=0.2))
```

전체 문장을 이용하는 감성 분류에서는 Bidirectional이 유용할 수 있지만 latency와 파라미터 수가 증가합니다.

## LSTM의 두 상태

LSTM은 외부로 보이는 단기 표현 `h_t`와 비교적 곧게 흐르는 기억 통로 `c_t`를 구분합니다. `c_t`는 오래 보존할 내용, `h_t`는 현재 단계에서 사용할 내용을 담는다고 이해할 수 있습니다.

## 세 게이트의 전체 식

\[
f_t=\sigma(W_f[x_t;h_{t-1}]+b_f)
\]
\[
i_t=\sigma(W_i[x_t;h_{t-1}]+b_i),\quad
\tilde c_t=\tanh(W_c[x_t;h_{t-1}]+b_c)
\]
\[
c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t
\]
\[
o_t=\sigma(W_o[x_t;h_{t-1}]+b_o),\quad
h_t=o_t\odot\tanh(c_t)
\]

세 Sigmoid 게이트는 각 기억 차원마다 0~1 값을 냅니다. 하나의 스위치가 아니라 64유닛이면 64개의 연속적인 조절 손잡이가 있는 셈입니다.

## 숫자로 게이트 계산하기

한 차원만 보겠습니다.

- 이전 기억 `c_{t-1}=0.6`
- forget gate `f_t=0.8`
- input gate `i_t=0.3`
- 후보 기억 `c̃_t=-0.5`

\[
c_t=0.8\times0.6+0.3\times(-0.5)=0.33
\]

이전 기억 0.48을 남기고 새 부정 정보 -0.15를 반영했습니다. output gate가 0.7이면 `h_t=0.7×tanh(0.33)≈0.223`입니다.

## 파라미터 수 계산

입력 차원 `D`, 은닉 크기 `H`인 LSTM은 네 종류의 계산을 하므로 대략 다음 파라미터를 가집니다.

\[
4H(D+H+1)
\]

`D=128`, `H=64`이면 `4×64×(128+64+1)=49,408`개입니다. 같은 크기의 SimpleRNN `H(D+H+1)=12,352`개보다 약 4배입니다. Bidirectional이면 방향별 층이 따로 있어 약 2배가 됩니다.

## Forget gate와 기울기

기억 상태에 대한 직접 미분에는 `f_t`가 나타납니다.

\[
\frac{\partial c_t}{\partial c_{t-1}}=f_t
\]

필요한 구간에서 forget 값이 1에 가까우면 기억과 기울기가 비교적 잘 유지됩니다. 항상 1이면 불필요한 기억까지 쌓이므로 입력에 따라 학습되어야 합니다.

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
2. `D=100`, `H=32`인 LSTM의 파라미터 수를 계산하세요.
3. 양방향 LSTM을 사용할 수 없는 운영 사례를 제시하세요.

---

<!-- SOURCE: 02_GRU_and_Selection.md -->

# 9.5 GRU와 모델 선택

GRU는 cell state와 hidden state를 통합하고 update/reset gate를 사용합니다. LSTM보다 구조가 단순해 파라미터가 적고 빠를 수 있지만 항상 성능이 우수하거나 열등한 것은 아닙니다.

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

\[
z_t=\sigma(W_zx_t+U_zh_{t-1}),\quad
r_t=\sigma(W_rx_t+U_rh_{t-1})
\]
\[
\tilde h_t=\tanh(W_hx_t+U_h(r_t\odot h_{t-1}))
\]
\[
h_t=(1-z_t)\odot h_{t-1}+z_t\odot\tilde h_t
\]

update gate는 과거와 후보 상태의 혼합 비율, reset gate는 후보를 만들 때 과거를 얼마나 사용할지 정합니다. 구현 문헌에 따라 update 식의 두 항 배치가 반대로 표기될 수 있으므로 사용 라이브러리 정의를 확인합니다.

## 파라미터 비교

GRU는 대략 `3H(D+H+1)`, LSTM은 `4H(D+H+1)`입니다. `D=128,H=64`이면 GRU는 약 37,056개, LSTM은 약 49,408개입니다. 실제 수는 bias 구현에 따라 조금 다를 수 있으므로 `model.summary()`로 확인합니다.

## 공정한 선택 실험

동일 tokenizer, embedding, split, seed, batch와 비슷한 파라미터 예산을 사용합니다. 최고 validation F1, test F1, epoch당 시간, peak memory, 긴 문장 성능을 비교합니다. 한 번 실행의 작은 차이보다 여러 seed의 평균과 변동을 봅니다.

## 선택 기준

GRU는 제한된 자원과 빠른 반복에서 좋은 출발점입니다. LSTM은 더 세밀한 기억 제어가 도움이 되는지 실험합니다. Transformer와도 비교하되 데이터 크기, 지연 요구와 설명 가능성을 포함합니다.

---

<!-- SOURCE: 03_Sentiment_Analysis.md -->

# 감성 분석 설계

감성 label은 주관적일 수 있으므로 annotation 기준과 불일치 사례를 기록합니다. 부정어, 반어, 복합 감정과 도메인 표현을 오류 분석에서 별도로 확인합니다.

```text
TextVectorization → Embedding(mask_zero=True)
→ Bidirectional LSTM/GRU → Dropout → sigmoid
```

평가 시 accuracy와 함께 precision, recall, F1, confusion matrix를 봅니다. 같은 상품·사용자의 거의 동일한 리뷰가 train/test에 나뉘지 않도록 중복 그룹을 고려합니다.

작은 데이터의 높은 점수는 일반화를 의미하지 않습니다. 실제 배포 전 시간·도메인 기준 holdout이 필요합니다.

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

---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 요약과 퀴즈

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

같은 데이터와 설정에서 LSTM과 GRU를 학습하고 테스트 지표를 비교합니다.

- [안내](examples/05_sentiment_solution/README.md)
- [완성 코드](examples/05_sentiment_solution/sentiment_compare.py)
- [데이터셋](examples/05_sentiment_solution/reviews.csv)

