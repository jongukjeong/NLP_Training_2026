# 7.1 Perceptron · 7.2 Multi Layer Perceptron

Perceptron은 입력의 가중합과 bias를 activation에 통과시켜 출력을 만듭니다.

```text
z = xW + b
y = activation(z)
```

단일 선형 경계로 분리할 수 없는 문제는 hidden layer를 추가한 MLP로 표현합니다.

```python
model = keras.Sequential([
    keras.Input(shape=(vocabulary_size,)),
    layers.Dense(64, activation="relu"),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation="softmax"),
])
```

레이어와 unit을 늘리면 표현력과 함께 과적합·계산 비용도 증가합니다. training loss만 감소하고 validation loss가 상승하면 과적합을 의심합니다.
