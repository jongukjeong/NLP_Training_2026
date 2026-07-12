# 10.4 Teacher Forcing

Teacher Forcing은 학습 중 Decoder의 다음 입력으로 모델의 이전 예측 대신 정답 token을 제공합니다.

```text
decoder input : <START> 나 는 학생
decoder target: 나       는 학생 <END>
```

학습을 안정화하지만 inference에서는 정답이 없으므로 이전 예측을 다시 입력합니다. 이 차이를 exposure bias라고 합니다.

대응 방법으로 scheduled sampling 등을 검토할 수 있지만 교육 실습에서는 학습과 inference 경로의 차이를 명시하고 오류 누적을 관찰합니다.

padding token의 loss를 제외하려면 sample weight 또는 mask를 적용합니다. 그렇지 않으면 긴 padding을 맞히는 능력이 loss를 지배할 수 있습니다.
