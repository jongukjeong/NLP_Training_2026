# 11.1~11.4 Attention

고정 길이 context 하나에 입력 전체를 압축하는 Seq2Seq의 병목을 줄이기 위해 decoder가 매 timestep마다 encoder state를 선택적으로 참조합니다.

```text
score(query, key) → softmax → attention weights
weights × values의 가중합 → context
```

| 방식 | score 특징 |
|---|---|
| Bahdanau | query와 key를 작은 신경망에 넣는 additive attention |
| Luong | dot 또는 학습된 행렬을 사용하는 multiplicative attention |
| Self Attention | 같은 sequence에서 query, key, value를 생성 |

scaled dot-product attention은 `QKᵀ / sqrt(d_k)` 뒤 softmax를 적용합니다. 차원이 커질 때 dot product가 커져 softmax가 포화되는 것을 완화하기 위해 scale합니다.

Mask 종류:

- padding mask: padding token 참조 방지
- causal mask: 미래 token 참조 방지

Attention weight는 모델 내부 계산의 단서이지만 인간의 설명이나 인과적 근거와 동일하지 않습니다.
