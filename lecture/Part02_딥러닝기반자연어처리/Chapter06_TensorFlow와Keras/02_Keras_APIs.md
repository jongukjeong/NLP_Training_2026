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

$$
y=x+F(x)
$$

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
