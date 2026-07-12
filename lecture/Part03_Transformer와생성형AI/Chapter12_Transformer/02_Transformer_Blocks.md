# 12.3 Multi-Head Attention · 12.4 FFN · 12.5 Layer Normalization

Multi-Head Attention은 표현 공간을 여러 head로 나눠 서로 다른 관계를 병렬 학습합니다. `key_dim × num_heads`와 모델 차원의 관계를 확인합니다.

Position-wise FFN은 각 timestep에 동일한 Dense 변환을 독립 적용합니다.

```text
x → MHA → Dropout → Add & LayerNorm
  → FFN → Dropout → Add & LayerNorm
```

Residual connection은 정보와 gradient 흐름을 돕고 LayerNorm은 샘플 내 feature를 정규화합니다. Pre-Norm과 Post-Norm은 LayerNorm 위치가 다르며 깊은 모델의 안정성에 영향을 줍니다.

Attention 계산량은 기본적으로 sequence 길이의 제곱에 비례하므로 긴 문서에서는 chunking이나 효율적 attention을 검토합니다.
