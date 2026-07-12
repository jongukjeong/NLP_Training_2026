# Chapter 12 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 12. Transformer

1. [Architecture와 Positional Encoding](01_Architecture_and_Position.md)
2. [Multi-Head Attention·FFN·LayerNorm](02_Transformer_Blocks.md)
3. [요약과 퀴즈](03_Summary_and_Quiz.md)
4. [실습: Transformer 구현](04_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_Transformer_블록_직접검증.md -->

# Chapter 12 Transformer 블록 직접 검증

## 구현 목표를 작은 부품으로 나누기

Transformer 전체를 한 번에 만들면 오류 위치를 찾기 어렵습니다. Positional Encoding, mask, Attention, FFN, LayerNorm을 각각 작은 입력으로 검사한 뒤 블록으로 합칩니다.

## Scaled Dot-Product Attention

```python
def attention(q, k, v, mask=None):
    dk = tf.cast(tf.shape(k)[-1], tf.float32)
    scores = tf.matmul(q, k, transpose_b=True) / tf.sqrt(dk)
    if mask is not None:
        scores += mask * -1e9
    weights = tf.nn.softmax(scores, axis=-1)
    return tf.matmul(weights, v), weights
```

여기서 mask가 1인 위치를 가린다고 정의했습니다. 라이브러리마다 True가 “보존”인지 “차단”인지 다를 수 있으므로 정의를 테스트합니다.

## Attention 단위 테스트

Q와 K가 같은 one-hot 벡터라면 자기 위치 점수가 큽니다. 가중치 행합이 1인지 검사합니다.

```python
tf.debugging.assert_near(
    tf.reduce_sum(weights, axis=-1),
    tf.ones(tf.shape(weights)[:-1]),
)
```

## Head 분할

입력 `(B,T,D)`를 `(B,H,T,D/H)`로 바꿉니다. `D=512`, `H=8`이면 head 차원은 64입니다.

```text
(B,T,512) → reshape (B,T,8,64) → transpose (B,8,T,64)
```

결합할 때 반대 순서로 transpose하고 reshape합니다. transpose를 빠뜨리면 토큰과 head 값이 섞입니다.

## Positional Encoding 검사

위치 0과 위치 1의 벡터가 다른지, 같은 위치는 batch와 관계없이 같은지 확인합니다. Token embedding과 더하려면 마지막 차원이 `d_model`로 같아야 합니다.

## 잔차 연결 검사

Attention과 FFN의 출력은 각각 입력과 더할 수 있도록 `(B,T,D)`를 유지해야 합니다. `Add`에서 오류가 나면 head 결합 또는 FFN 두 번째 Dense 출력 차원을 확인합니다.

## LayerNorm 수치 예

벡터 `[1,2,3]`의 평균은 2, 분산은 약 0.667입니다. 평균을 빼고 표준편차로 나누면 대략 `[-1.225,0,1.225]`가 됩니다. 실제 LayerNorm은 학습 가능한 scale과 bias를 추가합니다.

## Causal mask 직접 보기

길이 4의 mask는 미래 부분이 삼각형으로 가려져야 합니다.

```text
0 1 1 1
0 0 1 1
0 0 0 1
0 0 0 0
```

이 예에서 1은 차단 위치입니다. 첫 토큰은 자신만, 넷째 토큰은 1~4 위치를 볼 수 있습니다.

## 복잡도 체감

길이 100이면 한 head 점수 10,000개, 길이 1,000이면 1,000,000개입니다. 길이가 10배면 점수 원소는 100배입니다. 메모리 부족 시 batch와 길이를 먼저 확인합니다.

## 완료 점검

- 입력과 블록 출력 shape 동일
- 미래 가중치 0
- PAD 가중치 0
- Attention 행합 1
- 같은 seed에서 재현
- 작은 batch 순전파에 NaN 없음

---

<!-- SOURCE: 00_Transformer_성능과_메모리_실험.md -->

# Chapter 12 Transformer 성능과 메모리 실험

## 길이 변화 실험

Batch와 모델을 고정하고 sequence 64, 128, 256에서 메모리와 시간을 측정합니다.

| 길이 | 점수 원소 비율 | Peak memory | ms/batch |
|---:|---:|---:|---:|
| 64 | 1 | 기록 | 기록 |
| 128 | 4 | 기록 | 기록 |
| 256 | 16 | 기록 | 기록 |

Attention의 `T²` 때문에 길이 4배는 점수 행렬 원소 16배가 됩니다.

## Head 수 비교

`d_model`이 같으면 head 수가 늘수록 head당 차원은 작아집니다. Head 4·8을 비교할 때 총 차원, 데이터, seed를 고정합니다. Head가 많다고 항상 더 다양한 관계를 배우는 것은 아닙니다.

## Ablation

위치 인코딩, 잔차 연결, mask 설정의 기여를 확인하되, 누수를 만드는 causal mask 제거 모델은 학습 실험용으로만 사용하고 올바른 생성 모델로 평가하지 않습니다.

## 메모리 부족 순서

Batch 축소 → 최대 길이 축소 → mixed precision → gradient accumulation → 작은 모델을 검토합니다. 여러 설정을 동시에 바꾸면 품질 변화 원인을 알기 어렵습니다.

## Mixed precision

일부 계산을 float16/bfloat16으로 처리해 메모리와 속도를 개선할 수 있습니다. Loss scaling과 지원 하드웨어를 확인하고 NaN 및 최종 지표를 비교합니다.

## 디버깅 기준

- mask 전후 미래 Attention 값
- Q/K/V와 head 결합 shape
- 잔차 덧셈 양쪽 dtype
- 학습/평가 Dropout 상태
- 첫 batch gradient norm

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 12 원리·수학·실습 가이드

## 1. 전체 구조

Transformer는 순환 없이 모든 토큰을 동시에 처리한다. Encoder block은 `Self-Attention → Add & Norm → FFN → Add & Norm`이며 Decoder에는 미래 토큰을 가리는 causal mask와 encoder를 보는 cross-attention이 추가된다.

## 2. 위치 정보

Attention만으로는 순서를 알 수 없어 토큰 임베딩에 위치 벡터를 더한다.

\[
PE(pos,2i)=\sin(pos/10000^{2i/d}),\quad PE(pos,2i+1)=\cos(pos/10000^{2i/d})
\]

서로 다른 주기의 파동을 조합해 각 위치가 구별된다. 학습형 위치 임베딩도 가능하지만 최대 길이와 외삽 특성이 다르다.

## 3. Multi-Head Attention

\[
head_i=Attention(QW_i^Q,KW_i^K,VW_i^V)
\]
\[
MHA=Concat(head_1,\dots,head_h)W^O
\]

`d_model=512`, head 8이면 보통 head당 64차원이다. 여러 head는 구문, 거리, 지시 관계 등 서로 다른 관점을 동시에 학습할 기회를 준다.

## 4. FFN과 LayerNorm

\[
FFN(x)=\operatorname{ReLU}(xW_1+b_1)W_2+b_2
\]

FFN은 각 토큰 위치에 같은 신경망을 독립 적용한다. LayerNorm은 한 토큰의 특성축을 평균 0, 분산 1에 가깝게 정규화한다.

\[
LN(x)=\gamma\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta
\]

잔차 연결 `x+Sublayer(x)`은 원래 정보를 보존하고 기울기 경로를 만든다.

## 5. 복잡도와 마스크

Self-Attention 점수 행렬은 `[T,T]`이므로 시간·메모리가 대략 `O(T²)`다. 길이가 2배면 점수 원소는 4배다. causal mask는 위치 `t`가 `t+1` 이후를 보지 못하게 하며, padding mask와 목적이 다르다.

실습에서는 각 단계 shape, attention 가중치 행합, mask 적용 후 미래 가중치 0, 잔차 전후 shape 동일 여부를 단위 테스트한다.

1. 8-head, `d_model=512`의 head 차원은?
2. 길이 128에서 256으로 늘면 점수 행렬 원소는 몇 배인가?
3. causal mask와 padding mask의 차이는?

---

<!-- SOURCE: 01_Architecture_and_Position.md -->

# 12.1 Transformer Architecture · 12.2 Positional Encoding

Transformer는 recurrence 없이 attention으로 token 관계를 계산합니다. Encoder는 bidirectional self-attention과 FFN을 쌓고, Decoder는 causal self-attention, encoder-decoder attention, FFN을 사용합니다.

Self Attention만으로는 token 순서를 구분하지 못하므로 positional encoding 또는 학습 가능한 position embedding을 더합니다.

```text
token embedding + position encoding → attention block
```

Sinusoidal encoding은 위치와 차원별 sin/cos 함수를 사용하며 학습 파라미터가 없습니다. 최대 sequence 길이와 embedding dimension의 shape를 확인해야 합니다.

## Transformer 한 블록을 따라가기

입력 토큰 ID `(B,T)`는 임베딩을 거쳐 `(B,T,d_model)`이 됩니다. 위치 정보를 더해도 shape는 변하지 않습니다. Multi-Head Attention, 잔차 연결, FFN을 지나도 마지막 shape는 계속 `(B,T,d_model)`로 유지됩니다.

```text
ID [B,T]
 → Embedding+Position [B,T,D]
 → Multi-Head Attention [B,T,D]
 → Add & Norm [B,T,D]
 → FFN [B,T,D]
 → Add & Norm [B,T,D]
```

## 위치 인코딩을 파동으로 이해하기

\[
PE(pos,2i)=\sin(pos/10000^{2i/d}),\quad
PE(pos,2i+1)=\cos(pos/10000^{2i/d})
\]

`pos`는 토큰 위치, `i`는 벡터 성분 번호, `d`는 모델 차원입니다. 빠르게 변하는 파동은 가까운 위치를 구분하고 느리게 변하는 파동은 먼 위치 정보를 제공합니다. 여러 주기의 시계바늘을 함께 읽어 위치를 표현한다고 생각할 수 있습니다.

## Multi-Head의 shape 계산

`B=32`, `T=100`, `d_model=512`, head 8이면 head당 차원은 64입니다. Q/K/V를 `(32,8,100,64)`로 나누고 점수는 `(32,8,100,100)`이 됩니다. head 출력을 다시 합치면 `(32,100,512)`입니다.

## 잔차 연결의 쉬운 의미

\[
y=x+F(x)
\]

층이 새로운 정보를 제대로 배우지 못해도 원래 입력 `x`가 통과할 길을 남깁니다. 덧셈이므로 `x`와 `F(x)`의 shape가 같아야 합니다. 잔차 연결은 “이전 내용을 지우고 새로 쓰기”보다 “이전 내용에 수정분 더하기”에 가깝습니다.

## 계산량

Attention 점수는 토큰 모든 쌍을 비교하므로 원소 수가 `T²`입니다. 길이 512면 한 head에 262,144개, 길이 1,024면 1,048,576개로 4배가 됩니다. 긴 문맥이 메모리를 빠르게 사용하는 이유입니다.

## 구현 검증

1. Attention 행렬 마지막 두 축이 `(T,T)`인지 확인합니다.
2. padding과 causal mask를 구분합니다.
3. 각 행의 Attention 가중치 합이 약 1인지 검사합니다.
4. 미래 위치 가중치가 0인지 작은 행렬로 출력합니다.

---

<!-- SOURCE: 02_Transformer_Blocks.md -->

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

\[
FFN(x)=W_2\,ReLU(W_1x+b_1)+b_2
\]

Attention이 토큰 사이 정보를 섞는 과정이라면 FFN은 각 토큰 벡터 내부의 특징을 변환합니다. 모든 위치에 같은 FFN 가중치를 사용하지만 위치별 계산은 독립적입니다.

예를 들어 `d_model=512`, 중간 차원 `d_ff=2048`이면 먼저 512차원을 2048차원으로 넓혀 다양한 특징 조합을 만든 뒤 다시 512차원으로 줄입니다.

## Layer Normalization을 성적 표준화로 이해하기

\[
LN(x)=\gamma\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}+\beta
\]

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

---

<!-- SOURCE: 03_Summary_and_Quiz.md -->

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

작은 Transformer encoder로 token sequence의 이진 패턴을 분류합니다.

- [안내](examples/04_transformer_solution/README.md)
- [코드](examples/04_transformer_solution/transformer_encoder.py)
- [데이터](examples/04_transformer_solution/sequences.csv)

