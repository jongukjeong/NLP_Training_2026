# 6.1 Tensor · 6.2 Dataset

Tensor는 다차원 배열이며 `shape`, `dtype`, `rank`가 핵심입니다.

```python
import tensorflow as tf

x = tf.constant([[1.0, 2.0], [3.0, 4.0]])
print(x.shape, x.dtype, tf.rank(x))
print(tf.reduce_mean(x, axis=0))
```

첫 번째 차원은 일반적으로 batch입니다. 모델 입력 shape에는 batch 크기를 제외한 샘플 하나의 shape를 지정합니다.

`tf.data.Dataset`은 입력과 정답을 묶어 효율적으로 공급합니다.

```python
dataset = tf.data.Dataset.from_tensor_slices((features, labels))
dataset = dataset.shuffle(len(labels), seed=42)
dataset = dataset.batch(16).prefetch(tf.data.AUTOTUNE)
```

권장 순서는 데이터 특성에 따라 달라지지만 학습에서는 shuffle 뒤 batch를 적용합니다. 검증·테스트 데이터는 순서 재현을 위해 일반적으로 shuffle하지 않습니다.

확인 항목:

- feature와 label의 첫 차원 길이
- batch 이후 shape
- dtype과 결측·무한값
- 마지막 batch 크기
- shuffle seed와 재현성

## Tensor를 눈으로 읽는 연습

Tensor를 볼 때 값보다 먼저 `rank`, `shape`, `dtype`을 확인합니다. 자연어처리에서는 다음 형태가 반복해서 등장합니다.

| 단계 | 대표 shape | 의미 |
|---|---|---|
| 토큰 ID | `(batch, sequence)` | 각 문장을 정수 ID로 표현 |
| 임베딩 | `(batch, sequence, embedding)` | 각 토큰을 실수 벡터로 변환 |
| 문장 표현 | `(batch, hidden)` | 문장 전체를 하나의 벡터로 요약 |
| 분류 로짓 | `(batch, classes)` | 클래스별 정규화 전 점수 |

예를 들어 `(32, 50, 128)`은 문장 32개, 문장당 최대 50토큰, 토큰당 128개 특성입니다. `axis=0`은 문장들 사이, `axis=1`은 문장 내부의 시간축, `axis=2`는 특성축입니다.

```python
x = tf.random.normal((32, 50, 128))
sentence_vector = tf.reduce_mean(x, axis=1)
print(sentence_vector.shape)  # (32, 128)
```

시간축 평균을 냈으므로 토큰축 50이 사라졌습니다. 패딩이 있다면 단순 평균은 패딩까지 포함하므로 mask를 적용해야 합니다.

## 행렬 곱을 직접 계산하기

Dense 층의 핵심은 다음 한 줄입니다.

\[
Y=XW+b
\]

`X`가 `(B,D)`, `W`가 `(D,H)`, `b`가 `(H,)`이면 결과는 `(B,H)`입니다. 작은 예를 계산해 봅니다.

\[
X=[1,2],\quad W=\begin{bmatrix}1&0\\0.5&-1\end{bmatrix},\quad b=[0.1,0.2]
\]

첫 출력은 `1×1+2×0.5+0.1=2.1`, 둘째 출력은 `1×0+2×(-1)+0.2=-1.8`입니다. shape 오류가 나면 곱셈 경계의 두 차원 `D`가 같은지 확인합니다.

## dtype과 수치 안정성

토큰 ID는 보통 `int32`, 신경망 계산은 `float32`를 사용합니다. 정수 텐서를 Dense 층에 직접 넣거나 `float64` 데이터와 `float32` 가중치를 섞으면 오류 또는 불필요한 메모리 사용이 생깁니다.

```python
ids = tf.constant([[1, 2, 0]], dtype=tf.int32)
embedding = tf.keras.layers.Embedding(1000, 64, mask_zero=True)
vectors = embedding(ids)
tf.debugging.assert_all_finite(vectors, "NaN 또는 Inf 발견")
```

확률에 직접 `log(0)`을 적용하면 무한대가 됩니다. Keras 손실은 안정적인 구현을 제공하므로 로짓을 임의로 확률로 바꾼 뒤 다시 로그를 취하지 않습니다.

## Dataset 파이프라인을 단계별로 보기

```python
raw = tf.data.Dataset.from_tensor_slices((features, labels))
train = (
    raw
    .shuffle(buffer_size=len(features), seed=42,
             reshuffle_each_iteration=True)
    .batch(32, drop_remainder=False)
    .prefetch(tf.data.AUTOTUNE)
)
for xb, yb in train.take(1):
    print(xb.shape, yb.shape)
```

`shuffle`을 `batch`보다 먼저 해야 샘플 단위로 잘 섞입니다. `buffer_size`가 데이터보다 매우 작으면 근처 데이터끼리 남을 수 있습니다. `cache()`는 전처리 결과가 메모리나 디스크에 들어갈 때만 사용하며, 무한 반복 데이터 앞뒤에 잘못 놓으면 메모리 문제가 생길 수 있습니다.

## 데이터 개수와 학습 스텝

\[
steps=\left\lceil\frac{N}{B}\right\rceil
\]

샘플 103개, 배치 32라면 4스텝이고 마지막 배치는 7개입니다. `drop_remainder=True`이면 마지막 7개가 버려집니다. 고정 shape가 반드시 필요한 분산 학습이 아니라면 데이터 손실 여부를 먼저 고려합니다.

## 디버깅 체크리스트

1. `element_spec`으로 파이프라인 출력 dtype과 shape를 확인합니다.
2. 첫 배치를 꺼내 최소·최대값과 레이블 범위를 봅니다.
3. train/validation 분할 뒤 중복 ID가 없는지 검사합니다.
4. 작은 샘플 20개를 과적합시켜 모델과 손실 연결이 정상인지 확인합니다.
5. NaN이 생기면 입력값, 학습률, 손실 설정 순으로 추적합니다.

```python
print(train.element_spec)
tf.debugging.assert_greater_equal(labels, 0)
tf.debugging.assert_less(labels, num_classes)
```

## 미니 확인 실습

1. `(16, 40, 128)` 텐서를 시간축 평균 내면 shape는 무엇입니까?
2. 샘플 1,001개를 배치 64로 학습하면 한 epoch는 몇 step입니까?
3. 토큰 ID와 임베딩 벡터의 dtype이 다른 이유를 설명해 보세요.
