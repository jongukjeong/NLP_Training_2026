# Chapter 12. Transformer — 통합 원고

> 이 문서는 Chapter 12. Transformer 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 12. Transformer — `README.md`
- 12.1 Transformer Architecture · 12.2 Positional Encoding — `01_Architecture_and_Position.md`
- 12.3 Multi-Head Attention · 12.4 FFN · 12.5 Layer Normalization — `02_Transformer_Blocks.md`
- 요약과 퀴즈 — `03_Summary_and_Quiz.md`
- 실습: Transformer 구현 — `04_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 12. Transformer

# Chapter 12. Transformer

1. [Architecture와 Positional Encoding](01_Architecture_and_Position.md)
2. [Multi-Head Attention·FFN·LayerNorm](02_Transformer_Blocks.md)
3. [요약과 퀴즈](03_Summary_and_Quiz.md)
4. [실습: Transformer 구현](04_Practice.md)


---

<!-- SOURCE: 01_Architecture_and_Position.md -->

# 12.1 Transformer Architecture · 12.2 Positional Encoding

# 12.1 Transformer Architecture · 12.2 Positional Encoding

Transformer는 recurrence 없이 attention으로 token 관계를 계산합니다. Encoder는 bidirectional self-attention과 FFN을 쌓고, Decoder는 causal self-attention, encoder-decoder attention, FFN을 사용합니다.

Self Attention만으로는 token 순서를 구분하지 못하므로 positional encoding 또는 학습 가능한 position embedding을 더합니다.

```text
token embedding + position encoding → attention block
```

Sinusoidal encoding은 위치와 차원별 sin/cos 함수를 사용하며 학습 파라미터가 없습니다. 최대 sequence 길이와 embedding dimension의 shape를 확인해야 합니다.


---

<!-- SOURCE: 02_Transformer_Blocks.md -->

# 12.3 Multi-Head Attention · 12.4 FFN · 12.5 Layer Normalization

# 12.3 Multi-Head Attention · 12.4 FFN · 12.5 Layer Normalization

Multi-Head Attention은 표현 공간을 여러 head로 나눠 서로 다른 관계를 병렬 학습합니다. `key_dim × num_heads`와 모델 차원의 관계를 확인합니다.

Position-wise FFN은 각 timestep에 동일한 Dense 변환을 독립 적용합니다.

```text
x → MHA → Dropout → Add & LayerNorm
  → FFN → Dropout → Add & LayerNorm
```

Residual connection은 정보와 gradient 흐름을 돕고 LayerNorm은 샘플 내 feature를 정규화합니다. Pre-Norm과 Post-Norm은 LayerNorm 위치가 다르며 깊은 모델의 안정성에 영향을 줍니다.

Attention 계산량은 기본적으로 sequence 길이의 제곱에 비례하므로 긴 문서에서는 chunking이나 효율적 attention을 검토합니다.


---

<!-- SOURCE: 03_Summary_and_Quiz.md -->

# 요약과 퀴즈

# 요약과 퀴즈

1. Transformer가 recurrence 대신 사용하는 핵심 연산은? **Attention**
2. 위치 정보가 필요한 이유는? **Self Attention 자체는 순서를 구분하지 못함**
3. Multi-Head의 목적은? **여러 표현 공간의 관계 병렬 학습**
4. FFN은 timestep마다 같은 변환을 적용하나요? **예**
5. Residual connection의 역할은? **정보·gradient 흐름 지원**
6. LayerNorm과 BatchNorm의 기준 축은 같은가요? **아니요**
7. 긴 sequence의 주요 비용 문제는? **Attention의 O(n²) 계산·메모리**


---

<!-- SOURCE: 04_Practice.md -->

# 실습: Transformer 구현

# 실습: Transformer 구현

작은 Transformer encoder로 token sequence의 이진 패턴을 분류합니다.

- [안내](examples/04_transformer_solution/README.md)
- [코드](examples/04_transformer_solution/transformer_encoder.py)
- [데이터](examples/04_transformer_solution/sequences.csv)

