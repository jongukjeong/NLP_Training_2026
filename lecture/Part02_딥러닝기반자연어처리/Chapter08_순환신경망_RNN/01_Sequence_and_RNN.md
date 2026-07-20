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

$$
h_t=\tanh(W_xx_t+W_hh_{t-1}+b)
$$

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

$$
\frac{\partial L}{\partial h_t}
=\frac{\partial L}{\partial h_T}
\prod_{k=t+1}^{T}\frac{\partial h_k}{\partial h_{k-1}}
$$

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

$$
g' = g\times\frac{c}{\|g\|}\quad (\|g\|>c)
$$

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
