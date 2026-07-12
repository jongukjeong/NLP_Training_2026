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
