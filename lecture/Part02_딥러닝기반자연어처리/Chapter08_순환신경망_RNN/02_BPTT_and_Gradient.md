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
