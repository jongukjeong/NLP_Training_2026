# 12.3 Multi-Head Attention · 12.4 FFN · 12.5 Layer Normalization

Multi-Head Attention은 표현 공간을 여러 head로 나눠 서로 다른 관계를 병렬 학습합니다. `key_dim × num_heads`와 모델 차원의 관계를 확인합니다.

Position-wise FFN은 각 timestep에 동일한 Dense 변환을 독립 적용합니다.

```text
x → MHA → Dropout → Add & LayerNorm
  → FFN → Dropout → Add & LayerNorm
```

Residual connection은 정보와 gradient 흐름을 돕고 LayerNorm은 샘플 내 feature를 정규화합니다. Pre-Norm과 Post-Norm은 LayerNorm 위치가 다르며 깊은 모델의 안정성에 영향을 줍니다.

Attention 계산량은 기본적으로 sequence 길이의 제곱에 비례하므로 긴 문서에서는 chunking이나 효율적 attention을 검토합니다.

## Transformer 블록을 회사 회의로 비유하기

각 토큰을 회의 참가자라고 생각해 봅시다. Multi-Head Attention에서는 각 참가자가 다른 참가자의 말을 듣습니다. Head마다 관점이 달라 한 head는 주어와 동사 관계, 다른 head는 멀리 떨어진 지시어를 볼 수 있습니다. FFN은 회의에서 얻은 정보를 각 참가자가 자기 자리에서 정리하는 단계입니다.

## Multi-Head Attention 계산 순서

1. 입력에서 Q, K, V를 각각 만듭니다.
2. 여러 head로 차원을 나눕니다.
3. head별 Attention을 계산합니다.
4. head 결과를 이어 붙입니다.
5. 출력 행렬로 다시 `d_model` 차원에 맞춥니다.

`d_model=256`, head 4라면 head당 64차원입니다. 나누어떨어지지 않으면 일반적인 구현에서 오류가 발생합니다.

## FFN은 토큰별 작은 신경망

$$
FFN(x)=W_2\,ReLU(W_1x+b_1)+b_2
$$

Attention이 토큰 사이 정보를 섞는 과정이라면 FFN은 각 토큰 벡터 내부의 특징을 변환합니다. 모든 위치에 같은 FFN 가중치를 사용하지만 위치별 계산은 독립적입니다.

예를 들어 `d_model=512`, 중간 차원 `d_ff=2048`이면 먼저 512차원을 2048차원으로 넓혀 다양한 특징 조합을 만든 뒤 다시 512차원으로 줄입니다.

## Layer Normalization을 성적 표준화로 이해하기

$$
LN(x)=\gamma\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta
$$

`μ`는 한 토큰 특성들의 평균, `σ²`는 분산입니다. 평균을 빼고 표준편차로 나누어 값의 규모를 일정하게 만듭니다. `ε`는 분산이 0에 가까울 때 0으로 나누는 문제를 막는 작은 수입니다. `γ,β`는 정규화 후 필요한 크기와 위치를 다시 학습합니다.

## Pre-Norm과 Post-Norm

LayerNorm을 sublayer 앞에 두는지 뒤에 두는지에 따라 구조가 달라집니다. 둘 중 하나를 무조건 정답이라 하지 말고 사용하는 모델 구현과 논문 설정을 맞춥니다. 직접 구현할 때 블록 순서가 참고 코드와 같은지 확인합니다.

## Dropout 위치

Attention 가중치, Attention 출력, FFN 중간 또는 잔차 합산 전 등에 Dropout이 들어갈 수 있습니다. 학습 때만 무작위로 일부 값을 끄며 평가 때는 꺼집니다. 재현 실험에서는 seed와 `training` 상태를 기록합니다.

## shape 디버깅 표

| 단계 | 예시 shape |
|---|---|
| 입력 | `(B,T,512)` |
| Q/K/V 분할 | `(B,8,T,64)` |
| 점수 | `(B,8,T,T)` |
| head 결합 | `(B,T,512)` |
| FFN 중간 | `(B,T,2048)` |
| 블록 출력 | `(B,T,512)` |

덧셈 직전에 shape가 같고, mask가 점수 행렬로 broadcast되는지 확인합니다.
