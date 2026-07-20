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

$$
\frac{\partial L}{\partial W_h}=\sum_t\frac{\partial L}{\partial h_t}\frac{\partial h_t}{\partial W_h}
$$

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
