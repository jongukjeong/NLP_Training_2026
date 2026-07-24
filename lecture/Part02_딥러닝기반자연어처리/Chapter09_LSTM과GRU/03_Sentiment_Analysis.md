# 9.6 감성 분석 파이프라인

감성 label은 주관적일 수 있으므로 annotation 기준과 불일치 사례를 기록합니다. 부정어, 반어, 복합 감정과 도메인 표현을 오류 분석에서 별도로 확인합니다.

```text
TextVectorization → Embedding(mask_zero=True)
→ Bidirectional LSTM/GRU → Dropout → sigmoid
```

평가 시 accuracy와 함께 precision, recall, F1, confusion matrix를 봅니다. 같은 상품·사용자의 거의 동일한 리뷰가 train/test에 나뉘지 않도록 중복 그룹을 고려합니다.

작은 데이터의 높은 점수는 일반화를 의미하지 않습니다. 실제 배포 전 시간·도메인 기준 holdout이 필요합니다.

[06_sentiment_pipeline.py](06_sentiment_pipeline.py)는 9.1~9.5에서 살펴본
순차 상태 갱신을 두 개의 짧은 감성 문장에 적용합니다.

```bash
python 06_sentiment_pipeline.py
```

“배송이 느리지만 제품은 좋아요”와 “제품은 좋지만 배송이 느려요”처럼
비슷한 단어가 들어 있어도 순서와 마지막 정보에 따라 상태와 예측이 달라지는
것을 확인합니다. 이 코드는 Gate의 직관을 위한 규칙 기반 축소 모형이며,
학습된 LSTM·GRU 감성 분류기는 아닙니다. 실제 모델 구조는 아래 Keras
예제를 사용합니다.

## 데이터 설계

평점으로 감성 레이블을 자동 생성할 때 중간 평점 처리와 반어적 리뷰를 점검합니다. 동일 사용자의 반복 리뷰나 거의 같은 문장이 분할을 넘어가면 누수됩니다.

## 전처리의 균형

느낌표, 이모지, 반복 문자, 부정 표현은 감성 신호일 수 있으므로 일괄 제거하지 않습니다. 미등록어 비율과 truncation 비율을 train/validation/test별로 기록합니다.

## 확률과 calibration

Sigmoid 0.9가 실제로 약 90% 정확한지를 calibration curve로 확인할 수 있습니다. 확률이 과신되어 있다면 임계값과 사용자 표시 정책에 영향을 줍니다.

## 도전 평가셋

부정, 반전, 풍자, 도메인 용어, 매우 긴 문장으로 작은 challenge set을 만듭니다. 일반 test F1과 함께 보고 모델이 어떤 언어 현상을 아직 못 다루는지 설명합니다.

## 운영 관점

오분류 비용이 대칭인지 확인합니다. 부정 리뷰 누락과 긍정 리뷰 오탐의 업무 비용이 다르면 PR 곡선에서 임계값을 정하고 모호한 구간은 사람 검토로 보냅니다.

## 데이터 준비 흐름

```text
리뷰 원문 → 중복 제거 → 레이블 규칙 → 그룹 분할
→ tokenizer fit(train만) → padding → 모델 학습 → 오류 분석
```

별점에서 레이블을 만들면 별점 3의 처리와 내용·별점 불일치를 표본 검사합니다.

## 모델 코드

```python
model = tf.keras.Sequential([
    layers.Embedding(vocab_size, 128, mask_zero=True),
    layers.Bidirectional(layers.GRU(64)),
    layers.Dropout(0.3),
    layers.Dense(1, activation="sigmoid"),
])
model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"],
)
```

양방향 GRU의 출력은 보통 정방향·역방향을 연결해 128차원입니다.

## 임계값 선택

```python
from sklearn.metrics import precision_recall_curve

precision, recall, thresholds = precision_recall_curve(y_valid, prob_valid)
```

부정 리뷰를 놓치지 않는 것이 중요하면 목표 Recall을 만족하는 threshold를 validation에서 찾습니다. Test에서 고르면 성능이 과대평가됩니다.

## Challenge set 평가

부정, 반전, 풍자, 대상 혼합, 긴 문장을 각 20개 이상 준비합니다. 전체 test가 좋아도 “느리지만 결과는 좋다” 같은 반전 문장에서 실패할 수 있습니다.

## 확신하며 틀린 사례

예측 확률이 0.9 이상인데 오답인 리뷰를 먼저 읽습니다. 잘못된 레이블, 데이터 누수, 특정 키워드 편향을 찾기 쉽습니다.

## 운영 출력

확률이 모호한 구간은 `uncertain`으로 보내 사람 검토를 받을 수 있습니다. 긍정/부정만 강제로 반환하는 것보다 업무 위험을 줄일 수 있습니다.
