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
