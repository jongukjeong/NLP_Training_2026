# 감성 분석 설계

감성 label은 주관적일 수 있으므로 annotation 기준과 불일치 사례를 기록합니다. 부정어, 반어, 복합 감정과 도메인 표현을 오류 분석에서 별도로 확인합니다.

```text
TextVectorization → Embedding(mask_zero=True)
→ Bidirectional LSTM/GRU → Dropout → sigmoid
```

평가 시 accuracy와 함께 precision, recall, F1, confusion matrix를 봅니다. 같은 상품·사용자의 거의 동일한 리뷰가 train/test에 나뉘지 않도록 중복 그룹을 고려합니다.

작은 데이터의 높은 점수는 일반화를 의미하지 않습니다. 실제 배포 전 시간·도메인 기준 holdout이 필요합니다.
