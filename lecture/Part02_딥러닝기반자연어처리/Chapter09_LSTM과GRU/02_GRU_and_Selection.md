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
