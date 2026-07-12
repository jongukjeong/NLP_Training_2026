# 감성 분석 설계

감성 label은 주관적일 수 있으므로 annotation 기준과 불일치 사례를 기록합니다. 부정어, 반어, 복합 감정과 도메인 표현을 오류 분석에서 별도로 확인합니다.

```text
TextVectorization → Embedding(mask_zero=True)
→ Bidirectional LSTM/GRU → Dropout → sigmoid
```

평가 시 accuracy와 함께 precision, recall, F1, confusion matrix를 봅니다. 같은 상품·사용자의 거의 동일한 리뷰가 train/test에 나뉘지 않도록 중복 그룹을 고려합니다.

작은 데이터의 높은 점수는 일반화를 의미하지 않습니다. 실제 배포 전 시간·도메인 기준 holdout이 필요합니다.

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
