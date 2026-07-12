# Chapter 12 Transformer 성능과 메모리 실험

## 길이 변화 실험

Batch와 모델을 고정하고 sequence 64, 128, 256에서 메모리와 시간을 측정합니다.

| 길이 | 점수 원소 비율 | Peak memory | ms/batch |
|---:|---:|---:|---:|
| 64 | 1 | 기록 | 기록 |
| 128 | 4 | 기록 | 기록 |
| 256 | 16 | 기록 | 기록 |

Attention의 `T²` 때문에 길이 4배는 점수 행렬 원소 16배가 됩니다.

## Head 수 비교

`d_model`이 같으면 head 수가 늘수록 head당 차원은 작아집니다. Head 4·8을 비교할 때 총 차원, 데이터, seed를 고정합니다. Head가 많다고 항상 더 다양한 관계를 배우는 것은 아닙니다.

## Ablation

위치 인코딩, 잔차 연결, mask 설정의 기여를 확인하되, 누수를 만드는 causal mask 제거 모델은 학습 실험용으로만 사용하고 올바른 생성 모델로 평가하지 않습니다.

## 메모리 부족 순서

Batch 축소 → 최대 길이 축소 → mixed precision → gradient accumulation → 작은 모델을 검토합니다. 여러 설정을 동시에 바꾸면 품질 변화 원인을 알기 어렵습니다.

## Mixed precision

일부 계산을 float16/bfloat16으로 처리해 메모리와 속도를 개선할 수 있습니다. Loss scaling과 지원 하드웨어를 확인하고 NaN 및 최종 지표를 비교합니다.

## 디버깅 기준

- mask 전후 미래 Attention 값
- Q/K/V와 head 결합 shape
- 잔차 덧셈 양쪽 dtype
- 학습/평가 Dropout 상태
- 첫 batch gradient norm
