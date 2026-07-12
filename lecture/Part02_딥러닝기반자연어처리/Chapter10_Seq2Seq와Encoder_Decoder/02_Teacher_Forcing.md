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

## 시프트 데이터 직접 만들기

```python
target = [BOS, I, am, student, EOS]
decoder_input = target[:-1]
decoder_label = target[1:]
```

입력과 레이블 길이는 같고 한 칸 어긋납니다. 첫 레이블은 `I`, 마지막 레이블은 `EOS`입니다.

## Batch shape

`decoder_input`과 `decoder_label`은 `(B,T_target)`입니다. Embedding 후 입력은 `(B,T_target,D)`, decoder logits는 `(B,T_target,V)`입니다. `V`는 target 어휘 크기입니다.

## Teacher forcing 비율

비율 1.0은 항상 정답 이전 토큰, 0.0은 항상 모델 이전 예측을 사용합니다. 비율을 낮추면 추론 상황과 가까워지지만 초기 오답이 연쇄되어 학습이 불안정할 수 있습니다.

## Scheduled sampling 실험

```text
epoch 1~5: ratio 1.0
epoch 6~10: ratio 0.8
epoch 11~: ratio 0.5
```

고정 1.0 기준선과 생성 BLEU·반복률·학습 안정성을 비교합니다. 무조건 낮추는 것이 정답은 아닙니다.

## Exposure bias 오류 보기

첫 토큰 하나를 잘못 선택했을 때 이후 번역이 얼마나 무너지는지 greedy 출력의 단계별 토큰과 확률을 저장합니다.

## PAD 마스크 확인

PAD 위치 token loss가 0으로 제외되는지 작은 batch에서 직접 출력합니다. 평균 분모도 실제 토큰 수인지 검사합니다.

## 대표 구현 오류

- BOS를 정답에도 포함
- EOS가 학습 정답에서 빠짐
- decoder 입력과 label이 같은 배열
- PAD 손실 포함
- 추론에서 정답 토큰을 실수로 사용
