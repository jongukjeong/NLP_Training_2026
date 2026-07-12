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
