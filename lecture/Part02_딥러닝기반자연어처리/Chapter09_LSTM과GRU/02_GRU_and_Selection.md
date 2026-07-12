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
