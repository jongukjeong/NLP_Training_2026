# Chapter 7 통합 강의 원고

---

<!-- SOURCE: README.md -->

# Chapter 7. 딥러닝 기초


## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **퍼셉트론(Perceptron): 입력의 가중합으로 값을 판단하는 가장 단순한 인공 신경망**
- **활성화 함수(Activation Function): 신경망에 비선형성을 더하는 함수**
- **손실 함수(Loss Function): 예측과 정답의 차이를 계산하는 함수**
- **옵티마이저(Optimizer): 손실이 줄도록 가중치를 수정하는 방법**
- **그래디언트(Gradient, 기울기): 가중치를 바꿀 방향과 크기를 나타내는 값**

Perceptron에서 Multi Layer Perceptron으로 확장하며 activation, loss, optimizer가 텍스트 분류 학습에서 맡는 역할을 이해합니다.

1. [Perceptron과 MLP](01_Perceptron_and_MLP.md)
2. [Activation·Loss·Optimizer](02_Training_Components.md)
3. [텍스트 분류 설계](03_Text_Classification.md)
4. [퀴즈](04_Summary_and_Quiz.md)
5. [실습: 텍스트 분류](05_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_손실과_최적화_실험워크북.md -->

# Chapter 7 손실과 최적화 실험 워크북

## 손실은 모델에게 주는 채점표

같은 예측도 채점 방식에 따라 수정 방향이 달라집니다. 문제 유형에 맞는 손실을 선택해야 합니다.

## 이진 교차 엔트로피 숫자 비교

정답이 1일 때:

\[
L=-\log(p)
\]

| 예측 p | 손실 |
|---:|---:|
| 0.9 | 0.105 |
| 0.5 | 0.693 |
| 0.1 | 2.303 |

확신하며 틀린 0.1 예측에 큰 벌점을 줍니다.

## 다중 분류 손실

정답 클래스가 2이고 Softmax 결과가 `[0.1,0.2,0.7]`이면 손실은 `-log(0.7)≈0.357`입니다. 정수 레이블이면 Sparse, one-hot이면 Categorical 손실을 사용합니다.

## 다중 레이블

“배송 지연”과 “환불 요청”을 동시에 표시할 수 있다면 클래스마다 독립 Sigmoid를 사용합니다. 레이블 `[1,1,0]`, 예측 `[0.8,0.6,0.2]`처럼 각 클래스의 Binary CE를 계산합니다.

## Gradient descent를 산길로 이해하기

현재 위치에서 가장 가파르게 올라가는 방향이 gradient입니다. 손실을 줄이려면 반대 방향으로 이동합니다.

\[
w_{new}=w-\eta\frac{\partial L}{\partial w}
\]

`w=1.0`, gradient 0.4, 학습률 0.1이면 새 값은 0.96입니다.

## Momentum

매 단계 방향을 조금씩 기억해 작은 요철에 흔들리지 않고 이동합니다. 관성 때문에 최솟값을 지나칠 수 있어 학습률과 함께 조정합니다.

## Adam

최근 gradient 평균과 제곱 평균을 사용해 파라미터별 이동 크기를 조절합니다. 초기 실험에 편리하지만 모든 데이터에서 최종 일반화가 가장 좋다는 보장은 없습니다.

## Gradient 확인

```python
with tf.GradientTape() as tape:
    predictions = model(x, training=True)
    loss = loss_fn(y, predictions)
grads = tape.gradient(loss, model.trainable_variables)
print(float(tf.linalg.global_norm(grads)))
```

`None` gradient는 연결이 끊겼거나 손실에 사용되지 않는 변수일 수 있습니다. 매우 큰 값은 폭주, 거의 0인 값은 포화나 단절을 의심합니다.

## Class weight

희소 클래스 손실에 더 큰 가중치를 줄 수 있습니다. 하지만 Recall이 증가하면서 Precision이 크게 떨어질 수 있으므로 혼동 행렬을 함께 봅니다.

## 실험표

| Optimizer | LR | Val Macro F1 | 희소 Recall | 최고 epoch |
|---|---:|---:|---:|---:|
| SGD | 기록 | 기록 | 기록 | 기록 |
| Adam | 기록 | 기록 | 기록 | 기록 |

동일 초기화 또는 여러 seed 평균으로 비교합니다.

## 흔한 오해

- Loss가 낮으면 항상 업무 지표가 좋다: 임계값과 클래스 비용이 다를 수 있음
- Accuracy가 높으면 충분하다: 불균형에서 희소 클래스를 무시할 수 있음
- Adam이면 학습률이 필요 없다: 기본 학습률도 중요한 설정
- epoch를 늘리면 좋아진다: 과적합될 수 있음

## 완료 기준

손실-출력층 조합, gradient norm, 기준선, 클래스별 지표, optimizer 비교와 오류 사례를 모두 기록합니다.

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

<!-- SOURCE: 00_텍스트분류_실험과_결과해석.md -->

# Chapter 7 텍스트 분류 실험과 결과 해석

## 분류 문제부터 명확히 하기

모델을 만들기 전에 한 문장이 하나의 클래스만 갖는지 확인합니다. “배송이 늦어서 환불하고 싶다”는 배송과 환불이 함께 있습니다. 반드시 하나만 고른다면 우선순위 규칙이 필요하고, 둘 다 허용한다면 다중 레이블 문제입니다.

## 단일 클래스와 다중 레이블

| 문제 | 출력 | 활성화 | 손실 |
|---|---|---|---|
| 이진 단일 | 1개 | Sigmoid | Binary CE |
| C개 중 하나 | C개 | Softmax 또는 logits | Categorical CE |
| C개 중 여러 개 | C개 | 각자 Sigmoid | Binary CE |

다중 레이블에서 Softmax를 쓰면 클래스 확률 합이 1로 묶여 독립적으로 여러 의도를 선택하기 어렵습니다.

## 기준선

데이터 1,000개 중 배송 클래스가 600개라면 아무 문장도 읽지 않고 배송만 예측해도 accuracy 60%입니다. 모델 accuracy 65%는 숫자만 보면 좋아 보이지만 기준선보다 5%p 높은 수준입니다.

## 혼동 행렬 손계산

긴급 문의 100개 중 80개를 긴급으로 찾고 20개를 놓쳤다고 합시다. 일반 문의 100개 중 10개를 잘못 긴급으로 분류했습니다.

```text
TP=80, FN=20, FP=10, TN=90
```

\[
Precision=\frac{80}{80+10}=0.889
\]

\[
Recall=\frac{80}{80+20}=0.8
\]

긴급 문의를 놓치는 비용이 크다면 Recall을 높이는 쪽으로 임계값을 낮출 수 있지만 FP도 늘어납니다.

## F1 계산

\[
F1=\frac{2\times Precision\times Recall}{Precision+Recall}
\]

위 값에서는 약 0.842입니다. F1은 Precision과 Recall 중 하나만 매우 높은 모델을 경계하는 균형 지표입니다.

## Macro와 Micro

Macro F1은 클래스별 F1을 동일 비중으로 평균내 희소 클래스도 중요하게 봅니다. Micro F1은 전체 TP/FP/FN을 합쳐 큰 클래스의 영향이 큽니다. 불균형 데이터에서는 둘을 함께 봅니다.

## 데이터 누수 사례

- 같은 문의의 복사본이 train과 test에 있음
- 고객 ID를 보고 레이블을 맞춤
- 전체 데이터로 tokenizer 어휘를 만듦
- 답변 결과나 처리 상태가 입력 특성에 포함됨
- 시간상 미래 데이터를 과거 학습에 사용

누수가 있으면 test 성능은 높지만 실제 서비스에서 급락합니다.

## 오류 분석 표 만들기

| 문장 | 실제 | 예측 | 확률 | 오류 유형 |
|---|---|---|---:|---|
| 배송은 늦고 환불 원함 | 환불 | 배송 | 0.91 | 복합 의도 |
| 결제가 안 돼요 | 계정 | 기타 | 0.54 | 경계 모호 |

확신하며 틀린 사례부터 읽으면 레이블 오류와 반복 패턴을 빨리 찾을 수 있습니다.

## 실험 원칙

한 번에 한 요소만 바꿉니다. 임베딩 차원과 dropout, 학습률을 동시에 바꾸면 무엇이 효과를 냈는지 알 수 없습니다.

| 실험 | 변경 | Val Macro F1 | 시간 | 결론 |
|---|---|---:|---:|---|
| baseline | 평균 임베딩 | 기록 | 기록 | 기준 |
| exp-01 | Dense 32 추가 | 기록 | 기록 | 비교 |
| exp-02 | dropout 0.3 | 기록 | 기록 | 비교 |

## 비전공자가 결과를 설명하는 문장

“정확도가 높았다”보다 “100건 중 약 84건을 맞혔고, 긴급 문의 100건 중 80건을 찾았으며 20건은 놓쳤다”처럼 실제 개수로 설명하면 이해하기 쉽습니다.

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

## 결정 경계를 수식으로 이해하기

퍼셉트론의 판단 기준은 `w·x+b=0`입니다. 특성이 두 개면 평면 위의 직선, 세 개면 공간의 평면이 됩니다. 가중치는 경계의 방향, 편향은 경계의 위치를 결정합니다.

\[
z=w_1x_1+w_2x_2+b
\]

문의 분류에서 `x₁=환불 단어 빈도`, `x₂=배송 단어 빈도`, `w=[1.5,-0.7]`, `b=-0.2`라고 합시다. `[1,0]`은 `z=1.3`으로 환불 쪽, `[0,1]`은 `z=-0.9`로 반대쪽입니다. 실제 신경망은 사람이 정한 빈도 대신 학습된 고차원 표현을 사용합니다.

## XOR가 은닉층을 요구하는 이유

XOR의 양성점 `(0,1),(1,0)`과 음성점 `(0,0),(1,1)`은 직선 하나로 나눌 수 없습니다. 은닉층의 여러 뉴런이 서로 다른 경계를 만들고, 출력층이 이 경계를 조합하면 비선형 영역을 표현할 수 있습니다. 이것이 층을 쌓는 가장 기본적인 이유입니다.

## 활성화 함수의 선택

| 함수 | 범위 | 주 사용 위치 | 주의점 |
|---|---|---|---|
| ReLU | `[0,∞)` | 은닉층 | 음수 영역의 기울기 0 |
| Sigmoid | `(0,1)` | 이진 분류 출력 | 큰 절댓값에서 기울기 감소 |
| Tanh | `(-1,1)` | 고전 RNN 상태 | 긴 경로에서 기울기 소실 |
| Softmax | 합이 1 | 단일 정답 다중 분류 | 다중 레이블에는 부적절 |

Sigmoid의 미분은 `σ(z)(1-σ(z))`이며 최댓값도 0.25입니다. 여러 층에서 이 값이 계속 곱해지면 앞쪽 층의 기울기가 작아질 수 있습니다.

## 파라미터 수와 용량

Dense 층의 파라미터 수는 다음과 같습니다.

\[
(D+1)H
\]

입력 300차원, 은닉 128유닛이면 `(300+1)×128=38,528`개입니다. 다음 출력층이 5개 클래스면 `(128+1)×5=645`개이며 전체는 39,173개입니다. 모델 용량을 늘릴 때 데이터 크기와 검증 오차를 함께 봅니다.

## 순전파와 역전파 한 단계

순전파는 입력에서 예측까지 값을 계산합니다. 역전파는 연쇄법칙으로 손실이 각 파라미터에 얼마나 민감한지 계산합니다.

\[
\frac{\partial L}{\partial w}
=\frac{\partial L}{\partial \hat y}
\frac{\partial \hat y}{\partial z}
\frac{\partial z}{\partial w}
\]

기울기가 `0.4`, 학습률이 `0.01`, 현재 가중치가 `0.8`이면 새 가중치는 `0.8-0.01×0.4=0.796`입니다. 부호가 양수라는 것은 그 가중치를 줄일 때 현재 배치 손실이 감소한다는 뜻입니다.

## 과소적합과 과적합 구분

- train과 validation 성능이 모두 낮음: 표현력 부족, 학습 부족, 잘못된 특성 가능성
- train은 높고 validation은 낮음: 과적합, 데이터 누수 여부도 확인
- 둘 다 높지만 test만 낮음: 분할 차이 또는 테스트 분포 변화

Dropout은 학습 중 일부 활성값을 무작위로 0으로 만들어 특정 경로 의존을 줄입니다. 평가 시에는 자동으로 꺼지므로 직접 출력 비교 시 `training` 플래그를 주의합니다.

```python
hidden = layers.Dense(128, activation="relu")
dropout = layers.Dropout(0.3)
x = dropout(hidden(x), training=True)
```

## 작은 데이터 과적합 테스트

20~50개 샘플에서 훈련 정확도가 거의 100%가 되지 않는다면 일반화보다 구현 문제를 먼저 의심합니다. 레이블, 손실, 출력 활성화, 학습률, gradient가 연결되어 있는지 확인합니다. 이 테스트는 좋은 모델을 만드는 것이 아니라 학습 파이프라인이 작동하는지 확인하는 진단입니다.

## 확인 실습

1. 입력 50, 은닉 32인 Dense 층의 파라미터 수를 계산하세요.
2. 이진 분류와 상호 배타적 4분류의 출력층을 각각 설계하세요.
3. train loss는 감소하고 validation loss는 증가하는 그래프를 해석하세요.

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

## 손실함수는 학습 목표다

MSE는 오차를 제곱하므로 큰 오차를 강하게 벌하고, MAE는 절댓값을 써 이상치에 상대적으로 덜 민감합니다.

\[
MSE=\frac1N\sum_i(y_i-\hat y_i)^2,\qquad MAE=\frac1N\sum_i|y_i-\hat y_i|
\]

분류의 교차 엔트로피는 정답 클래스 확률이 낮을수록 급격히 커집니다. 정확도는 미분할 수 없는 최종 평가 지표이고, 손실은 학습에 사용할 수 있는 연속적인 신호입니다.

## SGD, Momentum, Adam

SGD는 현재 gradient만 사용합니다. Momentum은 이전 이동 방향을 누적해 좁고 흔들리는 골짜기를 통과하도록 돕습니다. Adam은 gradient의 1차·2차 모멘트를 추정해 파라미터별 크기를 조절합니다. Adam이 언제나 최고의 일반화 성능을 보장하지는 않습니다.

## 학습률 관찰

너무 큰 학습률은 손실을 발산시키고 너무 작은 값은 제한된 epoch 안에 충분히 이동하지 못합니다. learning-rate warmup과 decay는 초반 불안정성을 줄이고 후반에 세밀하게 조정합니다.

## 불균형 데이터

클래스 가중치는 희소 클래스의 손실 기여를 높입니다. 그러나 너무 큰 가중치는 오탐을 늘릴 수 있으므로 precision-recall 곡선과 업무 비용을 함께 봅니다. 데이터 증강이나 재표집은 test 분포를 바꾸지 않도록 train에만 적용합니다.

## 진단 순서

레이블 샘플 확인 → 단순 기준선 → 작은 데이터 과적합 → gradient norm → 학습 곡선 → 하이퍼파라미터 순으로 점검합니다. optimizer 변경은 데이터와 연결 오류를 해결하지 못합니다.

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

## 분류 파이프라인 설계

먼저 레이블 정의를 사람이 일관되게 적용할 수 있는지 확인합니다. “기타” 클래스가 지나치게 크거나 한 문장에 여러 의도가 공존한다면 단일 클래스 분류 가정부터 재검토합니다.

`TextVectorization` 또는 tokenizer는 train 데이터에만 적합시킵니다. 전체 데이터로 어휘를 만들면 test의 단어 존재 여부가 학습 단계에 누수됩니다.

## 기준선 세우기

다수 클래스 정확도, TF-IDF+선형 분류기, 평균 임베딩+Dense 모델을 차례로 비교합니다. 복잡한 모델이 단순 기준선을 넘지 못하면 먼저 데이터와 평가 방식을 고칩니다.

## 혼동 행렬 읽기

행을 실제, 열을 예측으로 두었는지 확인합니다. 특정 두 클래스가 서로 자주 혼동되면 레이블 경계가 모호한지, 학습 예제가 부족한지, 표현이 겹치는지 원문을 읽습니다.

## 임계값 조정

이진 분류의 기본 0.5가 업무상 최적이라는 보장은 없습니다. 누락 비용이 큰 긴급 문의는 recall 목표를 먼저 정하고 validation에서 임계값을 선택합니다. test에서 임계값을 고르면 성능을 낙관적으로 추정합니다.

## 오류 분석표

문장, 실제 레이블, 예측, 확률, 길이, 미등록어, 오류 유형을 저장합니다. 확신하며 틀린 사례부터 읽으면 레이블 오류나 반복되는 취약 패턴을 빨리 찾을 수 있습니다.

---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 퀴즈
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
