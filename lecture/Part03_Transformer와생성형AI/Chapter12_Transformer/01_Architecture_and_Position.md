# 12.1 Transformer Architecture · 12.2 Positional Encoding

Transformer는 recurrence 없이 attention으로 token 관계를 계산합니다. Encoder는 bidirectional self-attention과 FFN을 쌓고, Decoder는 causal self-attention, encoder-decoder attention, FFN을 사용합니다.

Self Attention만으로는 token 순서를 구분하지 못하므로 positional encoding 또는 학습 가능한 position embedding을 더합니다.

```text
token embedding + position encoding → attention block
```

Sinusoidal encoding은 위치와 차원별 sin/cos 함수를 사용하며 학습 파라미터가 없습니다. 최대 sequence 길이와 embedding dimension의 shape를 확인해야 합니다.
