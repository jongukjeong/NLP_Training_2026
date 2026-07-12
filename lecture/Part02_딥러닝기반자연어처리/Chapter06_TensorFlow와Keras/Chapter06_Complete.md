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

