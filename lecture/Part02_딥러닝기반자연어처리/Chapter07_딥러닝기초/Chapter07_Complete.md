# Chapter 7 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 7. 딥러닝 기초

Perceptron에서 Multi Layer Perceptron으로 확장하며 activation, loss, optimizer가 텍스트 분류 학습에서 맡는 역할을 이해합니다.

1. [Perceptron과 MLP](01_Perceptron_and_MLP.md)
2. [Activation·Loss·Optimizer](02_Training_Components.md)
3. [텍스트 분류 설계](03_Text_Classification.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: 텍스트 분류](05_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 7 원리·수학·실습 가이드

## 1. 퍼셉트론에서 MLP까지

퍼셉트론은 여러 단서에 중요도인 가중치를 곱해 합산한 뒤 임계값을 넘는지 판단한다.

\[
z=\sum_i w_ix_i+b,\qquad \hat y=f(z)
\]

`x=[1,0]`, `w=[0.8,-0.3]`, `b=-0.2`이면 `z=0.6`이다. 계단 함수라면 양성으로 분류한다. 하나의 직선으로 나눌 수 없는 XOR 문제는 은닉층을 둔 MLP가 필요하다.

Dense 층의 파라미터 수는 `(입력 차원+1)×출력 차원`이다. 입력 100, 은닉 유닛 32면 `(100+1)×32=3,232`개다.

## 2. 활성화 함수

\[
\sigma(z)=\frac1{1+e^{-z}},\quad \operatorname{ReLU}(z)=\max(0,z)
\]

\[
\operatorname{softmax}(z_i)=\frac{e^{z_i}}{\sum_j e^{z_j}}
\]

Sigmoid는 이진 확률, Softmax는 상호 배타적 다중 클래스 확률에 주로 사용한다. ReLU는 양수 영역에서 기울기가 유지되어 은닉층 학습에 유리하다. 로짓 `[2,1,0]`의 Softmax는 약 `[0.665,0.245,0.090]`이며 합은 1이다.

## 3. 손실과 최적화

다중 분류 교차 엔트로피는 정답 클래스 확률만 읽어 `L=-log(p_y)`로 계산할 수 있다. 정답 확률이 0.8이면 손실 0.223, 0.2이면 1.609다.

\[
w_{t+1}=w_t-\eta\nabla_wL
\]

학습률 `η`가 너무 크면 최솟값을 건너뛰고, 너무 작으면 학습이 느리다. SGD는 단순하고, Adam은 파라미터별 이동 크기를 조절해 초기 실습에 안정적이다. 옵티마이저보다 먼저 데이터 누수, 레이블 오류, 출력층과 손실 조합을 확인한다.

## 4. 텍스트 분류 흐름

`문장 → 토큰화 → 정수 ID [B,T] → Embedding [B,T,D] → Pooling [B,D] → Dense [B,C]`

```python
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 64, mask_zero=True),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(num_classes),
])
model.compile(optimizer="adam",
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=["accuracy"])
```

`from_logits=True`는 마지막 층에 Softmax가 없다는 뜻이다. 레이블이 `0,1,2` 정수면 Sparse 손실, one-hot이면 Categorical 손실을 사용한다.

## 5. 결과를 읽는 법

클래스 불균형에서는 정확도만으로 부족하다.

\[
Precision=\frac{TP}{TP+FP},\quad Recall=\frac{TP}{TP+FN},\quad F1=\frac{2PR}{P+R}
\]

긴급 문의 탐지라면 놓치지 않는 Recall이 중요할 수 있다. 오분류 문장을 클래스별로 최소 10개 읽고 토큰화 문제, 애매한 레이블, 부족한 사례를 구분한다.

## 실습 체크

- 다수 클래스만 예측하는 기준선보다 좋은가?
- 학습/검증/테스트에 중복 문장이 없는가?
- `model.summary()`의 shape가 설계와 같은가?
- 혼동 행렬에서 반복되는 오류가 무엇인가?

## 확인 문제

1. 입력 20, 출력 5인 Dense 층의 파라미터 수는?
2. 로짓 출력과 `from_logits`는 어떻게 맞추는가?
3. 불균형 데이터에서 정확도 외에 무엇을 볼 것인가?

---

<!-- SOURCE: 01_Perceptron_and_MLP.md -->

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

---

<!-- SOURCE: 02_Training_Components.md -->

# 7.3 Activation · 7.4 Loss · 7.5 Optimizer

| 작업 | 출력 | activation | loss |
|---|---:|---|---|
| 이진 분류 | 1 | sigmoid | BinaryCrossentropy |
| 단일 레이블 다중 분류 | 클래스 수 | softmax | SparseCategoricalCrossentropy |
| 회귀 | 1 | linear | MSE/MAE |

ReLU는 hidden layer의 일반적인 시작점입니다. sigmoid는 큰 절댓값 구간에서 gradient가 작아질 수 있어 깊은 hidden layer의 기본 선택으로는 잘 쓰지 않습니다.

Optimizer는 gradient로 가중치를 갱신합니다. Adam은 좋은 기준선이지만 learning rate가 너무 크면 발산하고 너무 작으면 학습이 느립니다.

분류에서는 label 형식과 loss가 맞아야 합니다. 정수 클래스 ID는 SparseCategoricalCrossentropy, one-hot label은 CategoricalCrossentropy를 사용합니다.

---

<!-- SOURCE: 03_Text_Classification.md -->

# 실무 텍스트 분류 설계

```text
원문 → TextVectorization → multi-hot/TF-IDF → MLP → 클래스 확률
```

`TextVectorization.adapt()`는 training text에만 적용합니다. validation/test의 어휘가 vocabulary에 반영되면 누수입니다.

클래스 불균형에서는 accuracy만으로 충분하지 않습니다. confusion matrix, macro F1, 클래스별 recall을 함께 확인합니다.

오분류 검토 항목:

- label 오류
- 너무 짧거나 긴 문장
- 부정어·도메인 용어
- OOV 비율
- 중복 데이터의 split 간 누수

작은 데이터에서는 단순 TF-IDF+선형 모델도 강한 기준선이므로 딥러닝 결과와 비교합니다.

---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 요약과 퀴즈

1. Perceptron이 표현하지 못하는 대표적인 논리 문제는? **XOR**
2. hidden layer에 비선형 activation이 필요한 이유는? **선형층만 쌓으면 하나의 선형 변환과 같기 때문**
3. 정수 다중 클래스 label에 맞는 loss는? **SparseCategoricalCrossentropy**
4. validation loss가 상승하고 train loss만 감소하면? **과적합 가능성**
5. 불균형 분류에서 accuracy 외에 볼 지표는? **macro F1, 클래스별 recall 등**
6. TextVectorization은 어느 데이터에 adapt해야 하나요? **training data**

---

<!-- SOURCE: 05_Practice.md -->

# 실습: 텍스트 분류

고객 문의를 배송·환불·계정 세 클래스로 분류합니다.

- [안내](examples/05_text_classification_solution/README.md)
- [완성 코드](examples/05_text_classification_solution/text_classifier.py)
- [데이터셋](examples/05_text_classification_solution/inquiries.csv)

