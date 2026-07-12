# Chapter 8 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 8. 순환신경망(RNN)

1. [Sequence Data와 Vanilla RNN](01_Sequence_and_RNN.md)
2. [BPTT와 Vanishing Gradient](02_BPTT_and_Gradient.md)
3. [문장 분류 설계](03_Sentence_Classification.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: 문장 분류](05_Practice.md)

목표는 timestep, hidden state, padding/masking과 RNN의 gradient 한계를 이해하고 문장 분류 모델을 완성하는 것입니다.

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 8 원리·수학·실습 가이드

## 1. 순서가 중요한 데이터

“개가 사람을 물었다”와 “사람이 개를 물었다”는 단어 집합이 같아도 의미가 다르다. RNN은 현재 입력과 직전까지의 요약인 은닉 상태를 함께 사용한다.

\[
h_t=\tanh(W_{xh}x_t+W_{hh}h_{t-1}+b_h),\qquad y_t=W_{hy}h_t+b_y
\]

입력은 `[B,T,D]`, 은닉 상태는 매 시점 `[B,H]`다. 문장 분류에서는 마지막 유효 상태나 전체 상태를 풀링해 `[B,C]` 로짓을 만든다.

## 2. 시간축으로 펼쳐 보기

같은 RNN 셀이 `t=1…T`에서 반복되며 모든 시점이 같은 가중치를 공유한다. 따라서 문장 길이가 늘어도 파라미터 수는 늘지 않지만 계산 경로는 길어진다.

```python
rnn = tf.keras.layers.SimpleRNN(64, return_sequences=True)
x = tf.random.normal((32, 20, 128))
print(rnn(x).shape)  # (32, 20, 64)
```

`return_sequences=False`이면 마지막 출력 `[32,64]`, `True`이면 모든 시점 `[32,20,64]`을 반환한다.

## 3. BPTT와 기울기 문제

BPTT는 마지막 손실에서 시간축을 거슬러 미분한다. 먼 시점의 영향에는 반복적인 미분 곱이 들어간다.

\[
\frac{\partial L}{\partial h_t}=\frac{\partial L}{\partial h_T}
\prod_{k=t+1}^{T}\frac{\partial h_k}{\partial h_{k-1}}
\]

각 곱이 0.5라면 10단계 뒤 영향은 `0.5^10≈0.001`로 작아진다. 1.5라면 `1.5^10≈57.7`로 폭증한다. 전자는 장기 기억을 잃는 기울기 소실, 후자는 학습이 불안정한 기울기 폭주다.

대응책은 LSTM/GRU, 짧은 구간 학습, 적절한 초기화, gradient clipping이다.

```python
optimizer = tf.keras.optimizers.Adam(clipnorm=1.0)
```

## 4. 패딩과 마스크

배치 안 문장 길이를 맞추려고 0을 붙이지만 0은 실제 단어가 아니다. `Embedding(mask_zero=True)`로 패딩 위치가 RNN 상태에 영향을 주지 않게 한다. 전처리에서 패딩 ID와 실제 어휘 ID가 겹치지 않아야 한다.

## 5. 문장 분류 설계

```python
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 128, mask_zero=True),
    tf.keras.layers.SimpleRNN(64),
    tf.keras.layers.Dense(num_classes),
])
```

검증 시 길이 구간별 성능을 따로 본다. 짧은 문장만 잘 맞고 긴 문장에서 급락한다면 장기 의존성이나 truncation을 의심한다.

## 흔한 오류와 확인 문제

- 문장축 `T`와 특성축 `D`를 바꾸어 입력함
- 패딩을 실제 토큰처럼 학습함
- 긴 문장을 모두 같은 최대 길이로 만들어 메모리를 낭비함
- 양방향 RNN을 실시간 다음 토큰 예측에 사용해 미래 정보가 누수됨

1. `[16,30,100]`을 `SimpleRNN(64)`에 넣으면 기본 출력 shape는?
2. `0.5^20`이 장기 기억에 의미하는 것은?
3. `mask_zero=True`가 필요한 이유는?

---

<!-- SOURCE: 01_Sequence_and_RNN.md -->

# 8.1 Sequence Data · 8.2 Vanilla RNN

Sequence data는 순서가 의미를 가집니다. 문장은 길이가 다르므로 정수 토큰을 padding해 `(batch, timesteps)` 형태로 만들고 Embedding을 거쳐 `(batch, timesteps, features)`로 변환합니다.

RNN은 현재 입력과 이전 hidden state로 새 hidden state를 계산합니다.

```text
h_t = tanh(W_x x_t + W_h h_(t-1) + b)
```

```python
layers.Embedding(vocab_size, 32, mask_zero=True)
layers.SimpleRNN(32)
```

`mask_zero=True`는 0 padding timestep을 후속 mask 지원 layer가 무시하도록 돕습니다. 0은 실제 단어 ID로 사용하지 않습니다.

`return_sequences=False`는 마지막 출력만, `True`는 모든 timestep 출력을 반환합니다. 다음 recurrent layer나 attention에 전체 sequence가 필요하면 `True`를 사용합니다.

## RNN 셀 내부를 단계별로 계산하기

\[
h_t=\tanh(W_xx_t+W_hh_{t-1}+b)
\]

입력과 이전 기억을 각각 선형 변환해 더한 뒤 Tanh로 `-1~1` 범위의 새 상태를 만듭니다. 단순한 스칼라 예에서 `x_t=1`, `h_{t-1}=0.5`, `W_x=0.8`, `W_h=0.4`, `b=0`이면 Tanh 입력은 `1.0`, 새 상태는 약 `0.762`입니다.

다음 시점은 이 `0.762`를 다시 사용합니다. 같은 가중치가 모든 시점에 공유되므로 길이가 늘어도 파라미터 수는 그대로지만 계산 횟수와 기억 경로는 늘어납니다.

## 입력과 출력 shape 변형

| 설정 | 출력 shape | 사용 예 |
|---|---|---|
| `return_sequences=False` | `(B,H)` | 문장 전체 분류 |
| `return_sequences=True` | `(B,T,H)` | 토큰 분류, 다음 RNN, Attention |
| `return_state=True` | 출력과 마지막 상태 | Encoder-Decoder 상태 전달 |
| Bidirectional | 마지막 차원 보통 `2H` | 전체 문맥 분류 |

```python
layer = tf.keras.layers.SimpleRNN(
    64, return_sequences=True, return_state=True
)
sequence, final_state = layer(x)
print(sequence.shape)     # (B, T, 64)
print(final_state.shape)  # (B, 64)
```

## BPTT를 직관적으로 이해하기

마지막 분류 손실은 마지막 상태에 영향을 주고, 마지막 상태는 그 이전 상태에 의존합니다. 따라서 미분은 시간축을 거꾸로 통과합니다.

\[
\frac{\partial L}{\partial h_t}
=\frac{\partial L}{\partial h_T}
\prod_{k=t+1}^{T}\frac{\partial h_k}{\partial h_{k-1}}
\]

각 단계의 미분 크기가 평균 0.8이면 20단계 전 영향은 `0.8²⁰≈0.0115`입니다. 1.2이면 `1.2²⁰≈38.3`입니다. 앞은 기울기 소실, 뒤는 기울기 폭주입니다.

## 긴 문장의 실제 문제

문장 앞의 부정어가 뒤의 평가를 뒤집거나, 대명사가 오래전 명사를 가리키는 경우 긴 의존성이 필요합니다. SimpleRNN이 긴 문장에서 실패한다면 다음을 비교합니다.

1. 문장 길이 구간별 F1
2. truncation으로 잘린 비율
3. LSTM/GRU 교체 효과
4. gradient norm 분포
5. 양방향 사용 가능 여부

## Mask 전달 확인

`mask_zero=True`가 있어도 중간 사용자 정의 층이 mask를 버리면 RNN이 패딩을 읽을 수 있습니다.

```python
embedding = tf.keras.layers.Embedding(vocab_size, 64, mask_zero=True)
vectors = embedding(token_ids)
mask = embedding.compute_mask(token_ids)
print(mask[0])  # 실제 토큰 True, padding False
```

문장 끝 패딩과 앞쪽 패딩은 상태에 다른 영향을 줄 수 있습니다. 기본적인 RNN 실습에서는 뒤쪽 패딩과 명시적 mask를 권장합니다.

## Gradient clipping

Global norm이 임계값을 넘을 때 전체 기울기의 방향은 유지하면서 크기를 줄입니다.

\[
g' = g\times\frac{c}{\|g\|}\quad (\|g\|>c)
\]

norm 10인 기울기를 임계값 1로 자르면 크기가 1이 됩니다. clipping은 폭주를 완화하지만 소실된 기울기를 되살리지는 않습니다.

## 오류 분석 실습

- 길이 1~10, 11~30, 31 이상으로 평가를 나눕니다.
- 부정, 반전 접속사, 반복 표현, 미등록어 사례를 태깅합니다.
- 오분류가 전처리 문제인지 순서 모델 문제인지 구분합니다.
- 같은 파라미터 예산에서 평균 풀링 기준선과 비교합니다.

## 확인 문제

1. 모든 시점 출력이 필요한 두 가지 작업을 제시하세요.
2. `0.9³⁰`을 계산하고 기울기 흐름을 해석하세요.
3. clipping이 해결하는 문제와 해결하지 못하는 문제는 무엇입니까?

---

<!-- SOURCE: 02_BPTT_and_Gradient.md -->

# 8.3 BPTT · 8.4 Vanishing Gradient

BPTT(Backpropagation Through Time)는 펼쳐진 timestep을 따라 gradient를 역전파합니다. 긴 sequence에서는 같은 변환이 반복되며 gradient가 매우 작아지거나 커질 수 있습니다.

- vanishing gradient: 먼 과거 정보 학습 어려움
- exploding gradient: 학습 불안정·NaN

대응:

- LSTM/GRU 사용
- gradient clipping
- 적절한 sequence 길이
- normalization과 초기화
- validation curve와 gradient 이상 감시

```python
optimizer = keras.optimizers.Adam(clipnorm=1.0)
```

clip은 exploding gradient를 완화하지만 vanishing gradient의 근본 해결책은 아닙니다.

## 연쇄법칙의 시간 전개

RNN 가중치는 모든 시점에 공유되므로 한 가중치의 gradient에는 각 시점의 기여가 더해집니다.

\[
\frac{\partial L}{\partial W_h}=\sum_t\frac{\partial L}{\partial h_t}\frac{\partial h_t}{\partial W_h}
\]

긴 문장은 계산 그래프가 깊어져 메모리와 시간이 증가합니다. Truncated BPTT는 일정 구간마다 상태를 분리해 계산 부담을 줄이지만 구간보다 먼 의존성은 직접 학습하기 어렵습니다.

## gradient norm 기록

```python
with tf.GradientTape() as tape:
    pred = model(x, training=True)
    loss = loss_fn(y, pred)
grads = tape.gradient(loss, model.trainable_variables)
print(float(tf.linalg.global_norm(grads)))
```

매우 큰 norm이 반복되면 clipping과 학습률을 검토합니다. 거의 0이면 activation 포화, 지나치게 긴 경로, gradient 단절 가능성을 봅니다.

## 상태 초기화

일반적인 독립 문장 배치는 각 문장을 0 상태에서 시작합니다. `stateful=True`는 배치 사이 상태를 유지하므로 샘플 순서와 batch 크기를 엄격히 관리해야 합니다. 서로 무관한 문장의 상태가 섞이면 누수가 됩니다.

## 해결책 비교

LSTM/GRU는 덧셈 기억 경로, gradient clipping은 폭주 제한, normalization은 분포 안정화, residual 연결은 짧은 gradient 경로를 제공합니다. 각 방법이 해결하는 문제가 다릅니다.

---

<!-- SOURCE: 03_Sentence_Classification.md -->

# 문장 분류 설계

```text
문장 → TextVectorization(output_sequence_length=N)
→ Embedding(mask_zero=True) → SimpleRNN → Dense
```

최대 길이가 너무 짧으면 정보가 잘리고 너무 길면 계산량과 padding이 증가합니다. training data의 길이 분위수를 기준으로 정하고 잘린 비율을 기록합니다.

비교 실험:

- multi-hot MLP 기준선
- SimpleRNN
- sequence 길이 변화
- 단방향과 양방향 RNN

양방향 모델은 전체 문장을 본 뒤 분류하는 작업에는 적합하지만 미래 token을 볼 수 없는 실시간 생성에는 사용할 수 없습니다.

## 대표 벡터 선택

마지막 상태는 짧은 문장에는 간단하지만 앞쪽 정보가 희석될 수 있습니다. 전체 상태의 mean/max pooling은 모든 위치를 직접 요약하고, Attention은 입력에 따라 중요한 위치의 가중치를 학습합니다.

패딩을 포함한 max/mean pooling은 결과를 왜곡하므로 mask-aware 구현을 사용합니다.

## 양방향 RNN

정방향과 역방향 상태를 연결하면 각 토큰이 양쪽 문맥을 반영합니다. 문장 분류에는 유용하지만 파라미터·지연이 늘고 미래가 없는 스트리밍에는 사용할 수 없습니다.

## 길이별 배치

비슷한 길이의 문장을 같은 배치로 묶으면 패딩 계산을 줄입니다. 최대 길이는 무조건 데이터 최댓값보다 길이 분포의 상위 백분위와 잘린 샘플의 중요도를 보고 정합니다.

## 평가 실험

평균 풀링, SimpleRNN, Bidirectional RNN을 동일 임베딩 크기와 데이터 분할에서 비교합니다. 전체 F1뿐 아니라 길이 구간별 F1, 추론시간, 파라미터 수를 기록합니다.

## 오분류 읽기

부정어가 먼 문장, 핵심어가 처음에만 있는 문장, 중의적 표현, 과도하게 잘린 문장을 별도 태그로 분류합니다. 모델 변경 전에 반복되는 오류 유형이 전처리로 해결 가능한지 봅니다.

---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 요약과 퀴즈

1. RNN의 state는 무엇을 요약하나요? **이전 timestep까지의 정보**
2. Embedding 입력 shape는? **batch, timesteps**
3. `mask_zero=True`의 목적은? **0 padding 무시 지원**
4. BPTT는 어느 방향으로 gradient를 계산하나요? **시간축을 거슬러 역전파**
5. clipnorm이 주로 완화하는 문제는? **exploding gradient**
6. `return_sequences=True`가 필요한 경우는? **후속 layer가 전체 timestep 출력을 사용할 때**

---

<!-- SOURCE: 05_Practice.md -->

# 실습: 문장 분류

- [안내](examples/05_sentence_classification_solution/README.md)
- [완성 코드](examples/05_sentence_classification_solution/rnn_sentence_classifier.py)
- [데이터셋](examples/05_sentence_classification_solution/sentences.csv)

