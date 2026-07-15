# Chapter 6 통합 강의 원고

---

<!-- SOURCE: README.md -->

# Chapter 6. TensorFlow와 Keras

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **텐서(Tensor): 딥러닝 계산에 사용하는 다차원 숫자 배열**
- **배치(Batch): 한 번의 계산에서 함께 처리하는 데이터 묶음**
- **로짓(Logit): Sigmoid·Softmax로 확률을 만들기 전 클래스별 원점수**
- **잔차 연결(Residual Connection): 원래 입력을 변환 결과에 다시 더하는 연결**
- **에포크(Epoch): 전체 학습 데이터를 한 번 모두 사용한 단위**

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
4. [퀴즈](04_Summary_and_Quiz.md)
5. [실습: 첫 번째 딥러닝 모델](05_Practice.md)

> 공식 기준: Keras의 내장 학습 루프는 Sequential, Functional, subclass 모델에서 같은 방식으로 사용할 수 있습니다.

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: LEARNING_PATH.md -->

# Chapter 6 비전공자 학습 경로

## 기본 도달 목표

Tensor의 shape를 확인하고 작은 Keras 모델 실행

완성형 코드를 처음부터 모두 이해하거나 다시 작성하는 것은 기본 목표가 아닙니다.

## 1. Step by Step — 강사와 함께

1. Tensor를 만들고 shape를 출력한다
2. Dataset에서 배치 하나를 확인한다
3. 층 하나의 모델을 만든다
4. 한 번 학습하고 예측값을 본다

각 단계가 끝날 때 입력, 출력 또는 중간 결과를 화면에서 확인합니다. 설명할 수 없는 줄은 다음 단계로 넘어가기 전에 질문합니다.

## 2. Basic Practice — 짧은 흐름 연결

Step by Step의 네 단계를 한 흐름으로 연결합니다. 처음에는 함수 분리, 타입 힌트, 복잡한 예외 처리와 자동 보고서를 요구하지 않습니다.

완료 확인:

- 입력이 무엇인지 설명한다.
- 핵심 처리 한 단계를 찾아 수정한다.
- 출력이 예상과 다른 이유를 한 가지 찾는다.
- 실행 결과를 짧게 기록한다.

## 3. Practice·Assignment — 먼저 시도

[05_Practice.md](05_Practice.md)의 기본 요구사항을 먼저 수행합니다. 막히면 전체 solution 대신 필요한 단계의 힌트만 확인합니다.

## 4. Solution — 피드백 후 공개

[examples/05_first_model_solution/README.md](examples/05_first_model_solution/README.md)은 다수의 수강생이 기본 요구사항을 시도하고 공통 오류를 함께 확인한 뒤 공개합니다. 자신의 코드와 다음 항목을 비교합니다.

1. 반복되는 처리를 어떻게 묶었는가
2. 잘못된 입력을 어디에서 검사하는가
3. 결과를 어떻게 검증하고 기록하는가

## 선택 확장

- 콜백
- 재현성 설정
- 성능 개선
- 저장·복원

선택 확장은 기본 완료 기준에 포함하지 않습니다.

---

<!-- SOURCE: 00_실습_코드_읽기와_오류해결.md -->

# Chapter 6 실습 코드 읽기와 오류 해결

## 코드를 외우지 말고 데이터 흐름을 읽자

딥러닝 코드가 어려운 가장 큰 이유는 한 줄마다 데이터 모양이 바뀌기 때문입니다. 모델을 읽을 때는 층 이름보다 입력과 출력 shape를 종이에 적는 습관이 중요합니다.

```text
특성 10개를 가진 샘플 32개: (32,10)
Dense 16:                  (32,16)
Dense 1:                   (32,1)
```

32는 한 번에 처리하는 샘플 수, 10과 16은 샘플 하나를 표현하는 숫자 개수입니다.

## 첫 모델을 한 줄씩 읽기

```python
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(10,)),
    tf.keras.layers.Dense(16, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])
```

- Input: 샘플 하나가 숫자 10개라고 선언
- Dense 16: 10개 단서를 조합해 새로운 특징 16개 생성
- ReLU: 음수 점수를 0으로 바꾸어 비선형 판단 가능
- Dense 1: 최종 점수 하나 생성
- Sigmoid: 점수를 0~1 확률로 변환

## 파라미터 수 확인

첫 Dense 층은 가중치 `10×16=160`개와 편향 16개로 총 176개입니다. 마지막 층은 `16×1+1=17`개입니다. 전체 학습 파라미터는 193개입니다.

```python
model.summary()
```

summary의 값과 손계산이 다르면 입력 차원이나 층 연결을 다시 확인합니다.

## compile을 쉬운 말로

```python
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"],
)
```

- optimizer: 틀린 정도를 보고 가중치를 고치는 방법
- loss: 얼마나 틀렸는지 숫자로 계산하는 규칙
- metric: 사람이 결과를 읽기 위한 평가 기준

Loss는 학습에 직접 사용되지만 accuracy는 관찰용일 수 있습니다.

## fit 결과 읽기

```text
loss: 0.42 - accuracy: 0.81 - val_loss: 0.55 - val_accuracy: 0.74
```

훈련 데이터 정확도 81%, 검증 데이터 정확도 74%입니다. 한 epoch만 보고 결론 내리지 말고 곡선의 방향을 봅니다. train loss는 계속 줄지만 val loss가 다시 올라가면 과적합 가능성이 큽니다.

## 작은 데이터 과적합 테스트

샘플 20개만 골라 여러 epoch 학습했을 때 거의 완벽히 맞추지 못하면 일반화 이전에 코드 연결 문제를 의심합니다.

```python
small_x, small_y = x_train[:20], y_train[:20]
model.fit(small_x, small_y, epochs=100, verbose=0)
```

이 테스트의 목표는 좋은 성능이 아니라 모델·손실·레이블이 제대로 연결됐는지 확인하는 것입니다.

## 대표 오류 해석

### shape mismatch

모델은 `(B,10)`을 기대하지만 데이터가 `(B,8)`이면 발생합니다. `x.shape`와 `model.input_shape`를 비교합니다.

### label 범위 오류

3개 클래스인데 레이블에 3 또는 4가 들어 있으면 범위를 벗어납니다. 정수 클래스는 보통 `0~C-1`입니다.

### logits 설정 오류

마지막 층에 Softmax가 없으면 `from_logits=True`, 이미 Softmax가 있으면 `False`입니다. 중복 Softmax나 잘못된 설정은 손실 계산을 왜곡합니다.

### NaN loss

입력의 NaN/Inf, 너무 큰 학습률, 잘못된 로그 계산을 확인합니다.

```python
tf.debugging.assert_all_finite(x_train, "입력에 NaN/Inf 존재")
```

## predict 결과 읽기

Sigmoid 출력 `[[0.82],[0.31]]`은 첫 샘플이 양성일 가능성을 0.82로, 둘째는 0.31로 본다는 뜻입니다. 0.5는 기본 임계값일 뿐 업무 비용에 따라 validation에서 조정할 수 있습니다.

## 실습 완료 체크

1. 첫 batch의 shape와 dtype을 출력했는가?
2. 파라미터 수를 손으로 계산해 보았는가?
3. 다수 클래스 기준선과 비교했는가?
4. train/validation 곡선을 함께 보았는가?
5. 저장 모델을 다시 불러와 같은 결과가 나오는가?

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

<!-- SOURCE: 00_학습성능_개선과_재현성.md -->

# Chapter 6 학습 성능 개선과 재현성

## 성능 개선은 원인을 찾는 과정

정확도가 낮다고 층을 무조건 늘리면 원인을 알 수 없습니다. 데이터, 학습 과정, 모델 용량, 평가 방법을 순서대로 확인합니다.

```text
데이터 정상 여부 → 단순 기준선 → 작은 데이터 과적합
→ 학습 곡선 → 오류 사례 → 한 가지 변경 실험
```

## 재현 가능한 seed

```python
import random
import numpy as np
import tensorflow as tf

random.seed(42)
np.random.seed(42)
tf.keras.utils.set_random_seed(42)
```

Seed를 고정해도 GPU 연산과 라이브러리 버전에 따라 완전히 같은 결과가 보장되지 않을 수 있습니다. Python·TensorFlow·CUDA 버전과 데이터 분할 ID도 기록합니다.

## Batch 크기의 의미

Batch 1은 샘플 하나마다 가중치를 고쳐 방향이 흔들리지만 메모리를 적게 씁니다. 큰 batch는 평균 gradient가 안정적이지만 메모리와 일반화 특성이 달라집니다.

샘플 1,024개에서 batch 32면 epoch당 32회, batch 128이면 8회 업데이트합니다. Batch를 바꾸면 학습률과 총 업데이트 횟수도 함께 해석합니다.

## 학습률 찾기

손실이 처음부터 크게 출렁이거나 NaN이면 학습률을 낮춥니다. 너무 천천히 줄면 학습률이 작거나 gradient가 약할 수 있습니다.

```python
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
```

`1e-3`은 0.001입니다. 후보 `1e-2, 1e-3, 1e-4`를 같은 조건에서 비교합니다.

## Callback을 안전장치로 이해하기

- EarlyStopping: 검증 성능이 개선되지 않으면 중단
- ModelCheckpoint: 최고 상태 저장
- ReduceLROnPlateau: 정체 시 학습률 감소
- TensorBoard/CSVLogger: 학습 기록 보존

```python
callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=3, restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss", factor=0.5, patience=1
    ),
]
```

## 과적합 대응의 순서

데이터 누수 확인 → 중복 제거 → 더 많은 대표 데이터 → 모델 축소 → Dropout/규제 → EarlyStopping 순으로 검토합니다. 검증셋 자체가 작거나 편향되면 규제만으로 해결되지 않습니다.

## L2 규제

\[
L_{total}=L_{data}+\lambda\sum_iw_i^2
\]

큰 가중치에 추가 비용을 줍니다. `λ`가 너무 크면 모델이 충분히 배우지 못합니다.

## 실험 결과표

| ID | 변경 | Best epoch | Val loss | Val F1 | 시간 |
|---|---|---:|---:|---:|---:|
| base | 기준 | 기록 | 기록 | 기록 | 기록 |
| e01 | dropout 0.3 | 기록 | 기록 | 기록 | 기록 |
| e02 | lr 1e-4 | 기록 | 기록 | 기록 | 기록 |

한 번에 한 항목만 바꾸고 개선이 우연인지 여러 seed로 확인합니다.

## 저장 모델 검증

저장 직전 입력 하나의 예측을 보관하고 새 프로세스에서 모델을 불러와 오차 범위 안에서 같은지 확인합니다. 파일 존재만 확인하면 사용자 정의 층이나 tokenizer 누락을 놓칠 수 있습니다.

## 완료 기준

1. 기준선과 작은 데이터 과적합 테스트
2. train/validation 곡선 저장
3. 최고 epoch 복원
4. 변경 한 가지씩 실험
5. 모델·데이터·환경 버전 기록
6. 재로딩 예측 비교

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

# 퀴즈
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

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

수치 특징 4개로 이진 클래스를 예측합니다. 학습/검증/테스트 분리, Dataset 파이프라인, Sequential 학습, best model 저장과 평가 JSON 생성을 구현합니다.

- [실습 안내](examples/05_first_model_solution/README.md)
- [완성 코드](examples/05_first_model_solution/first_model.py)
- [데이터셋](examples/05_first_model_solution/samples.csv)
