# 7.3 Activation · 7.4 Loss · 7.5 Optimizer

| 작업 | 출력 | activation | loss |
|---|---:|---|---|
| 이진 분류 | 1 | sigmoid | BinaryCrossentropy |
| 단일 레이블 다중 분류 | 클래스 수 | softmax | SparseCategoricalCrossentropy |
| 회귀 | 1 | linear | MSE/MAE |

ReLU는 hidden layer의 일반적인 시작점입니다. sigmoid는 큰 절댓값 구간에서 gradient가 작아질 수 있어 깊은 hidden layer의 기본 선택으로는 잘 쓰지 않습니다.

Optimizer는 gradient로 가중치를 갱신합니다. Adam은 좋은 기준선이지만 learning rate가 너무 크면 발산하고 너무 작으면 학습이 느립니다.

분류에서는 label 형식과 loss가 맞아야 합니다. 정수 클래스 ID는 SparseCategoricalCrossentropy, one-hot label은 CategoricalCrossentropy를 사용합니다.
