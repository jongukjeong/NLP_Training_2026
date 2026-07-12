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
