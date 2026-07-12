# Chapter 6 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 6. TensorFlow와 Keras

## 학습 목표

- Tensor의 shape, dtype, axis를 해석한다.
- `tf.data.Dataset`으로 shuffle, batch, prefetch 파이프라인을 만든다.
- Sequential API와 Functional API의 선택 기준을 설명한다.
- `compile`, `fit`, `evaluate`, `predict`의 역할을 구분한다.
- callback과 `.keras` 형식으로 학습 결과를 관리한다.

## 구성

1. [Tensor와 Dataset](01_Tensor_and_Dataset.md)
2. [Sequential과 Functional API](02_Keras_APIs.md)
3. [모델 학습](03_Model_Training.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: 첫 번째 딥러닝 모델](05_Practice.md)

> 공식 기준: Keras의 내장 학습 루프는 Sequential, Functional, subclass 모델에서 같은 방식으로 사용할 수 있습니다.

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 6 원리·수학·실습 가이드

## 1. 이 장의 큰 그림

딥러닝은 숫자 배열을 입력받아 예측을 만들고, 정답과의 차이를 줄이도록 배열 속 가중치를 고치는 과정이다. TensorFlow의 `Tensor`는 숫자 배열, `Dataset`은 배열을 공급하는 파이프라인, Keras 모델은 계산 규칙, `fit()`은 반복 학습 절차다.

`문장 → 토큰 ID [B,T] → 임베딩 [B,T,D] → 모델 → 로짓 [B,C] → 손실 스칼라`

여기서 `B`는 배치 크기, `T`는 문장 길이, `D`는 임베딩 차원, `C`는 클래스 수다. 차원을 먼저 적으면 대부분의 구현 오류를 예방할 수 있다.

## 2. Tensor와 행렬 계산

- 스칼라: 값 하나, 예: 손실 `0.42`
- 벡터: 1차원 배열, 예: 한 단어 임베딩 `[D]`
- 행렬: 2차원 배열, 예: 한 배치의 특성 `[B,D]`
- 3차원 텐서: 문장 배치 `[B,T,D]`

행렬 곱은 앞 행렬의 열과 뒤 행렬의 행이 같아야 한다.

\[
C_{ij}=\sum_{k=1}^{D}A_{ik}B_{kj},\qquad [B,D]\times[D,C]=[B,C]
\]

예를 들어 입력 `[2,3]`과 가중치 `[3,4]`를 곱하면 두 샘플에 대한 네 클래스 점수 `[2,4]`가 된다. 원소별 곱 `A*B`와 행렬 곱 `A@B`를 혼동하지 않는다.

```python
import tensorflow as tf
x = tf.constant([[1., 2., 3.], [4., 5., 6.]])
w = tf.ones((3, 4))
print(tf.matmul(x, w).shape)  # (2, 4)
```

브로드캐스팅은 작은 텐서를 큰 텐서의 각 행에 반복 적용한다. `[B,C]+[C]`는 가능하지만, 의도하지 않은 축에 적용될 수 있으므로 연산 전후 `shape`를 출력한다.

## 3. Dataset을 쓰는 이유

전체 데이터를 한 번에 메모리에 올리지 않고 `shuffle → batch → map → prefetch` 순으로 공급한다. 한 에포크의 업데이트 횟수는 대략 다음과 같다.

\[
\text{steps per epoch}=\left\lceil\frac{N}{B}\right\rceil
\]

샘플 1,000개, 배치 32개면 한 에포크는 32스텝이다. 셔플은 학습 데이터에만 적용하고 검증·테스트 데이터에는 적용하지 않는다.

```python
ds = tf.data.Dataset.from_tensor_slices((features, labels))
train_ds = ds.shuffle(len(features), seed=42).batch(32).prefetch(tf.data.AUTOTUNE)
```

## 4. Sequential과 Functional API

층이 한 줄로만 연결되면 Sequential이 읽기 쉽다. 입력이 여러 개이거나 중간 출력을 합치고 잔차 연결을 만들면 Functional API가 적합하다.

```python
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(10,)),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])
```

Dense 층의 계산은 `z=xW+b`, `a=f(z)`다. 입력 `[B,10]`, 가중치 `[10,16]`, 편향 `[16]`이면 출력은 `[B,16]`이다.

## 5. 학습이 일어나는 수학

이진 분류의 교차 엔트로피는 다음과 같다.

\[
L=-\frac1N\sum_i[y_i\log p_i+(1-y_i)\log(1-p_i)]
\]

정답이 1인데 예측 확률이 0.9이면 손실은 `-log(0.9)≈0.105`, 0.1이면 `≈2.303`이다. 확신하며 틀린 예측을 크게 벌한다. 경사하강법은 `w←w-η∂L/∂w`로 손실이 작아지는 방향으로 가중치를 갱신한다.

```python
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
history = model.fit(train_ds, validation_data=valid_ds, epochs=10)
```

훈련 정확도만 상승하고 검증 손실이 상승하면 과적합 신호다. 정확도만 보지 말고 손실 곡선, 클래스별 정밀도·재현율도 함께 본다.

## 6. 실습 점검

1. 입력·레이블의 dtype과 shape를 출력한다.
2. 모델 `summary()`에서 각 층 출력과 파라미터 수를 확인한다.
3. 첫 배치 한 번을 통과시켜 출력 범위를 확인한다.
4. 무작위 기준선 및 다수 클래스 기준선과 비교한다.
5. seed, 데이터 분할, 하이퍼파라미터를 기록한다.

흔한 오류는 정수 레이블에 one-hot용 손실을 쓰는 것, 마지막 활성화와 손실의 `from_logits` 설정이 어긋나는 것, 검증 데이터를 학습에 섞는 것이다.

## 확인 문제

1. `[32,50,128]`에서 각 숫자는 무엇을 뜻하는가?
2. `[32,128]@[128,3]`의 결과 shape는?
3. 검증 손실이 상승할 때 고려할 조치는?

---

<!-- SOURCE: 01_Tensor_and_Dataset.md -->

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

---

<!-- SOURCE: 02_Keras_APIs.md -->

# 6.3 Sequential API · 6.4 Functional API

Sequential은 레이어가 한 줄로 연결되는 단일 입출력 모델에 적합합니다.

```python
from tensorflow import keras
from tensorflow.keras import layers

model = keras.Sequential([
    keras.Input(shape=(4,)),
    layers.Dense(16, activation="relu"),
    layers.Dense(1, activation="sigmoid"),
])
```

Functional API는 다중 입력·출력, 분기, layer sharing처럼 비선형 연결이 필요할 때 사용합니다.

```python
inputs = keras.Input(shape=(4,), name="features")
x = layers.Dense(16, activation="relu")(inputs)
outputs = layers.Dense(1, activation="sigmoid")(x)
model = keras.Model(inputs, outputs)
```

| 조건 | 선택 |
|---|---|
| 단일 입력·출력의 선형 스택 | Sequential |
| 다중 입력·출력 | Functional |
| 분기·병합·공유 레이어 | Functional |
| 동적인 제어 흐름 | Model subclassing 검토 |

`model.summary()`로 출력 shape와 파라미터 수를 확인한 뒤 학습합니다.

## API 선택을 구조로 판단하기

Sequential은 입력 하나가 층을 한 방향으로 지나는 모델에 적합합니다. Functional API는 다중 입력·다중 출력, 층 공유, 잔차 연결처럼 계산 그래프가 갈라지거나 합쳐질 때 사용합니다. Subclassing은 동적 반복이나 조건 분기가 핵심일 때 선택하지만 `summary()`와 저장·직렬화가 더 복잡할 수 있습니다.

```python
title = tf.keras.Input((20,), name="title")
body = tf.keras.Input((100,), name="body")
x1 = tf.keras.layers.Dense(16, activation="relu")(title)
x2 = tf.keras.layers.Dense(32, activation="relu")(body)
x = tf.keras.layers.Concatenate()([x1, x2])
priority = tf.keras.layers.Dense(1, activation="sigmoid", name="priority")(x)
category = tf.keras.layers.Dense(5, name="category")(x)
model = tf.keras.Model([title, body], [priority, category])
```

입력 shape는 batch 축을 제외해 선언합니다. `Input((100,))`은 실제 배치에서 `(B,100)`입니다. `Concatenate` 뒤에는 `(B,48)`이 되며 출력 이름을 지정하면 다중 손실 로그를 읽기 쉽습니다.

## 잔차 연결과 shape

\[
y=x+F(x)
\]

덧셈하려면 `x`와 `F(x)`의 shape가 같아야 합니다. 차원이 다르면 projection 층으로 맞춥니다. 연결은 `Add`와 `Concatenate`가 다릅니다. Add는 차원을 유지하고, Concatenate는 지정 축의 크기를 더합니다.

## 사용자 정의 층의 최소 원칙

가중치는 `build()` 또는 `add_weight()`로 등록하고 계산은 `call()`에 둡니다. Python 리스트에 임의 Tensor를 저장하거나 `call()`에서 매번 층을 새로 만들면 추적과 저장이 깨질 수 있습니다.

```python
class Scale(tf.keras.layers.Layer):
    def build(self, input_shape):
        self.scale = self.add_weight(shape=(), initializer="ones")
    def call(self, inputs):
        return inputs * self.scale
```

## 모델 요약을 읽는 법

`Param #`는 학습 가능한 가중치와 비학습 가중치를 포함합니다. None은 실행 시 정해지는 batch 또는 sequence 길이입니다. 예상 파라미터 수와 summary가 다르면 입력 차원이나 양방향 연결을 다시 봅니다.

## 저장과 재현성

전체 모델 저장은 구조·가중치·일부 optimizer 상태를 함께 보존합니다. 사용자 정의 객체는 직렬화 설정을 추가하고 저장 직후 새 프로세스에서 불러와 같은 입력의 출력을 비교합니다. 파일 생성 성공만으로 복원이 검증된 것은 아닙니다.

---

<!-- SOURCE: 03_Model_Training.md -->

# 6.5 Model Training

```python
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=1e-3),
    loss=keras.losses.BinaryCrossentropy(),
    metrics=[keras.metrics.BinaryAccuracy(name="accuracy")],
)

history = model.fit(train_ds, validation_data=valid_ds, epochs=30, callbacks=callbacks)
test_metrics = model.evaluate(test_ds, return_dict=True)
```

- optimizer: 가중치 갱신 방법
- loss: 모델이 최소화할 목적 함수
- metrics: 해석·보고할 지표
- epoch: 전체 학습 데이터를 반복한 횟수
- batch: 한 번의 갱신에 사용하는 샘플 묶음

필수 callback:

```python
callbacks = [
    keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
    keras.callbacks.ModelCheckpoint("output/best.keras", save_best_only=True),
]
```

테스트 데이터는 최종 평가에만 사용합니다. 모델 선택과 epoch 결정에 테스트 점수를 사용하면 누수가 발생합니다.

## compile 설정의 일관성

| 문제 | 출력층 | 손실 |
|---|---|---|
| 이진 분류 | 1 sigmoid | BinaryCrossentropy |
| 정수 레이블 다중 분류 | C logits | SparseCategoricalCrossentropy(from_logits=True) |
| one-hot 다중 분류 | C logits | CategoricalCrossentropy(from_logits=True) |
| 다중 레이블 | C sigmoid | BinaryCrossentropy |
| 회귀 | 필요한 값 수 | MSE 또는 MAE |

마지막 활성화와 `from_logits`가 중복되거나 빠지면 학습이 왜곡됩니다. 로짓에 Softmax를 적용했다면 `from_logits=False`, 활성화가 없다면 `True`입니다.

## fit 내부에서 일어나는 일

각 배치마다 순전파, 손실 계산, 자동미분, optimizer 갱신, metric 누적이 실행됩니다. epoch가 끝나면 validation은 가중치 갱신 없이 수행됩니다.

```python
callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=3, restore_best_weights=True
    ),
    tf.keras.callbacks.ModelCheckpoint(
        "best.keras", monitor="val_loss", save_best_only=True
    ),
]
```

EarlyStopping의 마지막 epoch와 최고 epoch는 다를 수 있습니다. `restore_best_weights=True`가 없으면 마지막 상태가 남습니다.

## 학습 곡선 진단

- 첫 epoch부터 손실이 NaN: 비정상 입력, 과도한 학습률, 잘못된 손실
- train/val 모두 변화 없음: gradient 단절, 레이블 오류, 너무 작은 학습률
- train만 계속 개선: 과적합 또는 분할 차이
- validation이 심하게 출렁임: 검증셋이 작거나 클래스 불균형

## evaluate와 predict의 차이

`evaluate()`는 정답이 있는 데이터에서 loss와 metric을 계산합니다. `predict()`는 모델 출력만 만듭니다. 로짓을 바로 확률로 오해하지 말고 문제에 맞는 Sigmoid 또는 Softmax를 적용합니다.

## 실험 기록표

데이터 버전, split seed, 모델 구조, optimizer, 학습률, batch, 최고 epoch, val/test metric, 실행 시간, 커밋 ID를 한 행으로 기록합니다. 한 번에 변수 하나만 바꿔야 개선 원인을 설명할 수 있습니다.

---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 요약과 퀴즈

## 요약

Tensor → Dataset → Model → compile → fit → evaluate → save 순서로 첫 학습 파이프라인을 구성합니다.

## 퀴즈

1. Tensor의 세 가지 핵심 속성은 무엇인가요?
2. 학습 Dataset에서 shuffle을 batch보다 먼저 적용하는 이유는 무엇인가요?
3. 다중 입력 모델에 적합한 Keras API는 무엇인가요?
4. loss와 metric의 역할 차이는 무엇인가요?
5. EarlyStopping의 `restore_best_weights=True`는 무엇을 보존하나요?

## 정답

1. shape, dtype, rank입니다.
2. batch마다 데이터가 충분히 섞이도록 하기 위해서입니다.
3. Functional API입니다.
4. loss는 최적화 대상이고 metric은 평가·보고 지표입니다.
5. 검증 성능이 가장 좋았던 epoch의 가중치입니다.

---

<!-- SOURCE: 05_Practice.md -->

# 실습: 첫 번째 딥러닝 모델

수치 특징 4개로 이진 클래스를 예측합니다. 학습/검증/테스트 분리, Dataset 파이프라인, Sequential 학습, best model 저장과 평가 JSON 생성을 구현합니다.

- [실습 안내](examples/05_first_model_solution/README.md)
- [완성 코드](examples/05_first_model_solution/first_model.py)
- [데이터셋](examples/05_first_model_solution/samples.csv)

