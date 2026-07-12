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
