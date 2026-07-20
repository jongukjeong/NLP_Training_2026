# 10.1 Seq2Seq · 10.2 Encoder · 10.3 Decoder

Seq2Seq는 입력 sequence를 출력 sequence로 변환합니다.

```text
입력 문장 → Encoder → context/state → Decoder → 출력 문장
```

Encoder RNN은 입력을 읽고 마지막 hidden/cell state를 Decoder 초기 상태로 전달합니다. Decoder는 시작 token에서 출발해 다음 token 분포를 반복 예측합니다.

학습 tensor:

- encoder input: `(batch, source_timesteps)`
- decoder input: `<START>`부터 마지막 직전 token
- decoder target: 첫 target token부터 `<END>`까지 한 칸 이동
- output logits/probabilities: `(batch, target_timesteps, target_vocab)`

고정 길이 context 하나에 모든 입력을 압축하는 기본 Seq2Seq는 긴 문장에서 병목이 생깁니다. Chapter 11의 Attention이 이를 완화합니다.

## 조건부 확률로 보는 번역

입력 문장 `x`가 주어졌을 때 번역문 전체 확률은 연쇄법칙으로 분해됩니다.

$$
P(y|x)=\prod_{t=1}^{T_y}P(y_t|y_1,\ldots,y_{t-1},x)
$$

각 단계에서 decoder는 어휘 크기 `V`개의 로짓을 만들고 Softmax로 다음 토큰 확률을 얻습니다. 문장 확률을 직접 곱하면 매우 작아지므로 평가와 탐색에서는 로그 확률 합을 사용합니다.

$$
\log P(y|x)=\sum_t\log P(y_t|y_{<t},x)
$$

## Encoder 상태의 흐름

```python
encoder_lstm = tf.keras.layers.LSTM(
    hidden_size, return_sequences=True, return_state=True
)
encoder_seq, state_h, state_c = encoder_lstm(source_vectors)
```

- `source_vectors`: `(B,T_source,D)`
- `encoder_seq`: `(B,T_source,H)`
- `state_h`, `state_c`: 각각 `(B,H)`

기본 Seq2Seq는 마지막 `state_h`, `state_c`를 decoder 초기 상태로 전달합니다. Attention 모델은 `encoder_seq` 전체도 보존합니다.

## Decoder의 학습 입력

목표가 `<BOS> I like NLP <EOS>`라면 다음처럼 한 칸 이동합니다.

| 위치 | Decoder 입력 | 예측 정답 |
|---:|---|---|
| 1 | `<BOS>` | `I` |
| 2 | `I` | `like` |
| 3 | `like` | `NLP` |
| 4 | `NLP` | `<EOS>` |

입력과 정답을 같은 위치로 주면 현재 정답을 그대로 보는 누수가 발생할 수 있습니다.

## Masked sequence loss

패딩을 포함한 모든 위치를 평균 내면 짧은 문장일수록 `<PAD>` 예측 비중이 커집니다.

$$
L=\frac{\sum_{b,t}m_{b,t}\,CE(y_{b,t},z_{b,t})}
{\sum_{b,t}m_{b,t}}
$$

```python
loss = loss_fn(target, logits)          # (B, T)
mask = tf.cast(target != PAD_ID, loss.dtype)
loss = tf.reduce_sum(loss * mask) / tf.reduce_sum(mask)
```

분모도 실제 토큰 수로 나누어야 배치의 패딩 비율에 따라 손실 크기가 흔들리지 않습니다.

## Teacher forcing과 노출 편향

학습 중에는 이전 정답을 입력하지만 추론 중에는 이전 예측을 입력합니다. 한 번 잘못 예측하면 이후 입력 분포가 학습 때와 달라져 오류가 누적될 수 있습니다. 이를 노출 편향이라고 합니다.

Teacher forcing 비율을 낮추는 방법이 항상 개선을 보장하지는 않습니다. 우선 정답 시프트, `<EOS>` 학습, attention, 데이터 품질을 확인하고 동일 평가셋에서 비교합니다.

## Greedy decoding 의사코드

```python
token = BOS_ID
state = encoder_state
result = []
for _ in range(max_length):
    logits, state = decoder_step(token, state)
    token = int(tf.argmax(logits[0]))
    if token == EOS_ID:
        break
    result.append(token)
```

종료 조건은 `<EOS>`와 최대 길이 모두 필요합니다. `<EOS>`를 생성하지 못하는 초기 모델이 무한 루프에 빠지는 것을 방지합니다.

## 번역 결과 진단

- 누락: 원문의 핵심 구가 사라짐
- 추가: 원문에 없는 내용 생성
- 반복: 같은 단어나 구가 되풀이됨
- 조기 종료: 번역이 중간에 끝남
- 미등록어: 고유명사·숫자가 깨짐
- 문법은 자연스럽지만 의미가 반대임

BLEU 같은 자동 점수와 함께 위 유형을 최소 30문장에서 사람이 분류합니다. 숫자와 고유명사는 별도 정확도도 유용합니다.

## 확인 문제

1. 문장 확률 대신 로그 확률 합을 사용하는 이유는 무엇입니까?
2. decoder 입력과 target이 한 칸 다른 이유를 설명하세요.
3. 패딩 마스크 없이 손실을 계산하면 어떤 편향이 생깁니까?
