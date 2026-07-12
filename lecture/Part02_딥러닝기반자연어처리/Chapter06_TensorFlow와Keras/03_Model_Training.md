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
