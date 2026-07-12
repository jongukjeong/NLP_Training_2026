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
