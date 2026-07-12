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

