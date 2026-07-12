# Chapter 8 RNN 비교 실험과 디버깅

## RNN을 써야 하는지 먼저 확인하기

순서가 중요하다고 가정하기 전에 TF-IDF나 평균 임베딩 기준선을 만듭니다. RNN이 더 느리면서 성능이 비슷하다면 업무에서는 단순 모델이 나을 수 있습니다.

## 공정한 모델 비교

```text
같은 데이터 분할
같은 tokenizer와 최대 길이
같은 임베딩 차원
비슷한 파라미터 예산
같은 평가 지표
```

| 모델 | Params | Macro F1 | 긴문장 F1 | P95 |
|---|---:|---:|---:|---:|
| 평균 풀링 | 기록 | 기록 | 기록 | 기록 |
| SimpleRNN | 기록 | 기록 | 기록 | 기록 |
| BiRNN | 기록 | 기록 | 기록 | 기록 |

## return_sequences 오류

두 번째 RNN을 쌓으려면 첫 RNN이 모든 시점 출력을 반환해야 합니다.

```python
tf.keras.layers.SimpleRNN(64, return_sequences=True),
tf.keras.layers.SimpleRNN(32),
```

첫 층이 마지막 벡터만 반환하면 다음 RNN이 시간축을 받을 수 없습니다.

## Mask 전달 테스트

같은 문장에 PAD 개수만 다르게 붙인 두 입력의 출력이 거의 같은지 비교합니다. 크게 다르면 mask가 전달되지 않았을 수 있습니다.

## Stateful RNN

긴 연속 신호를 batch 구간으로 나눌 때 상태를 유지할 수 있습니다. 독립 문장 분류에서 사용하면 앞 문장의 정보가 다음 문장으로 새어 나갑니다. Batch 순서와 `reset_states()`를 엄격히 관리합니다.

## Truncated BPTT

긴 시퀀스를 구간으로 잘라 역전파하면 메모리를 줄일 수 있지만 구간보다 먼 의존성을 직접 학습하기 어렵습니다. 구간 길이와 hidden state 전달 여부를 기록합니다.

## Gradient 폭주 관찰

Global norm을 epoch별로 기록합니다. 갑자기 매우 커지고 loss가 NaN이 되면 clipping과 학습률을 검토합니다.

```python
optimizer = tf.keras.optimizers.Adam(clipnorm=1.0)
```

## 길이 bucket

비슷한 길이 문장을 같은 batch에 묶으면 PAD 계산을 줄입니다. Bucket 경계가 너무 세밀하면 batch가 작아지고 데이터 섞임이 줄 수 있습니다.

## 오류 사례 분류

- 앞부분 핵심어를 잊음
- 문장 끝이 truncation됨
- 부정 범위를 잘못 이해
- 반복 표현에 흔들림
- OOV 제품명이 모두 같은 ID
- 양방향으로 미래 정보 누수

## Ablation

양방향 제거, mask 제거가 아니라 max length·pooling·hidden size 등 한 요소를 제거하거나 바꿔 실제 기여를 측정합니다. 안전상 필요한 mask를 의도적으로 제거한 결과를 최종 모델로 사용하지 않습니다.

## 결과 설명

“RNN이 문맥을 이해했다”보다 “평균 풀링 대비 전체 F1은 0.02, 31토큰 이상 문장 F1은 0.08 개선했지만 P95 지연은 12ms 증가했다”고 씁니다.

