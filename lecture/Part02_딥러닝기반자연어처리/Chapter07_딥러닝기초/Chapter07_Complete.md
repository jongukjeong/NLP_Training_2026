# Chapter 7. 딥러닝 기초 — 통합 원고

> 이 문서는 Chapter 7. 딥러닝 기초 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 7. 딥러닝 기초 — `README.md`
- 7.1 Perceptron · 7.2 Multi Layer Perceptron — `01_Perceptron_and_MLP.md`
- 7.3 Activation · 7.4 Loss · 7.5 Optimizer — `02_Training_Components.md`
- 실무 텍스트 분류 설계 — `03_Text_Classification.md`
- 요약과 퀴즈 — `04_Summary_and_Quiz.md`
- 실습: 텍스트 분류 — `05_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 7. 딥러닝 기초

# Chapter 7. 딥러닝 기초

Perceptron에서 Multi Layer Perceptron으로 확장하며 activation, loss, optimizer가 텍스트 분류 학습에서 맡는 역할을 이해합니다.

1. [Perceptron과 MLP](01_Perceptron_and_MLP.md)
2. [Activation·Loss·Optimizer](02_Training_Components.md)
3. [텍스트 분류 설계](03_Text_Classification.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: 텍스트 분류](05_Practice.md)


---

<!-- SOURCE: 01_Perceptron_and_MLP.md -->

# 7.1 Perceptron · 7.2 Multi Layer Perceptron

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

# 실습: 텍스트 분류

고객 문의를 배송·환불·계정 세 클래스로 분류합니다.

- [안내](examples/05_text_classification_solution/README.md)
- [완성 코드](examples/05_text_classification_solution/text_classifier.py)
- [데이터셋](examples/05_text_classification_solution/inquiries.csv)

