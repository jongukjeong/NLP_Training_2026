# Chapter 6. TensorFlow와 Keras — 통합 원고

> 이 문서는 Chapter 6. TensorFlow와 Keras 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 6. TensorFlow와 Keras — `README.md`
- 6.1 Tensor · 6.2 Dataset — `01_Tensor_and_Dataset.md`
- 6.3 Sequential API · 6.4 Functional API — `02_Keras_APIs.md`
- 6.5 Model Training — `03_Model_Training.md`
- 요약과 퀴즈 — `04_Summary_and_Quiz.md`
- 실습: 첫 번째 딥러닝 모델 — `05_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 6. TensorFlow와 Keras

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


---

<!-- SOURCE: 01_Tensor_and_Dataset.md -->

# 6.1 Tensor · 6.2 Dataset

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

# 실습: 첫 번째 딥러닝 모델

수치 특징 4개로 이진 클래스를 예측합니다. 학습/검증/테스트 분리, Dataset 파이프라인, Sequential 학습, best model 저장과 평가 JSON 생성을 구현합니다.

- [실습 안내](examples/05_first_model_solution/README.md)
- [완성 코드](examples/05_first_model_solution/first_model.py)
- [데이터셋](examples/05_first_model_solution/samples.csv)

