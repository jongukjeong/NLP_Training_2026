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

$$
MSE=\frac1N\sum_i(y_i-\hat y_i)^2,\qquad MAE=\frac1N\sum_i|y_i-\hat y_i|
$$

분류의 교차 엔트로피는 정답 클래스 확률이 낮을수록 급격히 커집니다. 정확도는 미분할 수 없는 최종 평가 지표이고, 손실은 학습에 사용할 수 있는 연속적인 신호입니다.

## SGD, Momentum, Adam

SGD는 현재 gradient만 사용합니다. Momentum은 이전 이동 방향을 누적해 좁고 흔들리는 골짜기를 통과하도록 돕습니다. Adam은 gradient의 1차·2차 모멘트를 추정해 파라미터별 크기를 조절합니다. Adam이 언제나 최고의 일반화 성능을 보장하지는 않습니다.

## 학습률 관찰

너무 큰 학습률은 손실을 발산시키고 너무 작은 값은 제한된 epoch 안에 충분히 이동하지 못합니다. learning-rate warmup과 decay는 초반 불안정성을 줄이고 후반에 세밀하게 조정합니다.

## 불균형 데이터

클래스 가중치는 희소 클래스의 손실 기여를 높입니다. 그러나 너무 큰 가중치는 오탐을 늘릴 수 있으므로 precision-recall 곡선과 업무 비용을 함께 봅니다. 데이터 증강이나 재표집은 test 분포를 바꾸지 않도록 train에만 적용합니다.

## 진단 순서

레이블 샘플 확인 → 단순 기준선 → 작은 데이터 과적합 → gradient norm → 학습 곡선 → 하이퍼파라미터 순으로 점검합니다. optimizer 변경은 데이터와 연결 오류를 해결하지 못합니다.
