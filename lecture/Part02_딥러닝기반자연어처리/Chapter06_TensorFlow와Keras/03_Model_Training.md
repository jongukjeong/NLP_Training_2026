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
