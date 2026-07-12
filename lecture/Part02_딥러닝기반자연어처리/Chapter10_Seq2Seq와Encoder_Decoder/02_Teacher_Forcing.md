# 10.4 Teacher Forcing

Teacher Forcing은 학습 중 Decoder의 다음 입력으로 모델의 이전 예측 대신 정답 token을 제공합니다.

```text
decoder input : <START> 나 는 학생
decoder target: 나       는 학생 <END>
```

학습을 안정화하지만 inference에서는 정답이 없으므로 이전 예측을 다시 입력합니다. 이 차이를 exposure bias라고 합니다.

대응 방법으로 scheduled sampling 등을 검토할 수 있지만 교육 실습에서는 학습과 inference 경로의 차이를 명시하고 오류 누적을 관찰합니다.

padding token의 loss를 제외하려면 sample weight 또는 mask를 적용합니다. 그렇지 않으면 긴 padding을 맞히는 능력이 loss를 지배할 수 있습니다.

## 학습과 추론의 입력 차이

학습에서는 정답 이전 토큰을 사용하므로 병렬로 모든 target 위치의 손실을 계산할 수 있습니다. 추론에서는 직전 예측이 다음 입력이어서 한 단계씩 생성합니다. 이 차이가 exposure bias의 원인입니다.

## 비율 스케줄

Teacher forcing 비율 `r`은 정답 토큰을 사용할 확률입니다. 초기 1.0에서 점차 낮추는 scheduled sampling을 사용할 수 있지만, 잘못된 예측이 학습 입력에 들어가 불안정해질 수 있습니다.

```python
use_truth = tf.random.uniform(()) < ratio
next_input = tf.where(use_truth, target[:, t], predicted)
```

배치 전체에 같은 선택을 적용할지 샘플별로 선택할지도 실험 정의에 기록합니다.

## Padding과 손실

Teacher forcing 입력의 PAD 위치와 target PAD 위치가 한 칸 이동해도 정확히 대응하는지 작은 예를 출력합니다. 마스크 분모는 PAD를 제외한 토큰 수여야 합니다.

## 디버깅

한 샘플에서 decoder input, target, argmax prediction을 표로 출력합니다. `<BOS>`를 예측 대상으로 넣거나 `<EOS>`가 target에서 빠지는 오류가 자주 발생합니다.
