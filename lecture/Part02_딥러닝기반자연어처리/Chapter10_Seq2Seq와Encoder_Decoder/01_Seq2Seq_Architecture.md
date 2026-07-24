# 10.1 Seq2Seq · 10.2 Encoder · 10.3 Decoder

## 10.1 Seq2Seq: 시퀀스를 다른 시퀀스로 바꾸기

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

[01_seq2seq.py](01_seq2seq.py)는 한국어 토큰 3개가 영어 토큰 4개로
바뀌는 예를 보여 줍니다. Seq2Seq의 입력과 출력 길이가 같을 필요가 없다는
점을 먼저 확인합니다.

```bash
python 01_seq2seq.py
```

### 조건부 확률로 보는 번역

입력 문장 `x`가 주어졌을 때 번역문 전체 확률은 연쇄법칙으로 분해됩니다.

$$
P(y|x)=\prod_{t=1}^{T_y}P(y_t|y_1,\ldots,y_{t-1},x)
$$

각 단계에서 decoder는 어휘 크기 `V`개의 로짓을 만들고 Softmax로 다음 토큰 확률을 얻습니다. 문장 확률을 직접 곱하면 매우 작아지므로 평가와 탐색에서는 로그 확률 합을 사용합니다.

$$
\log P(y|x)=\sum_t\log P(y_t|y_{<t},x)
$$

## 10.2 Encoder: 입력 문장을 상태로 바꾸기

Encoder는 입력 토큰을 순서대로 읽으며 hidden state를 갱신합니다. 기본
Seq2Seq에서는 마지막 상태가 입력 문장의 요약인 context가 되고 Decoder의
초기 상태로 전달됩니다.

[02_encoder.py](02_encoder.py)는 토큰마다 스칼라 상태가 변하는 과정을
출력합니다.

```bash
python 02_encoder.py
```

예제의 스칼라 계산은 흐름을 보여 주기 위한 축소 모형입니다. 실제 Encoder는
Embedding 벡터를 RNN·LSTM·GRU에 입력하고 벡터 상태를 학습합니다.

### Encoder 상태의 흐름

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

## 10.3 Decoder: 상태에서 출력 문장 만들기

Decoder는 Encoder가 전달한 상태와 이전 출력 토큰을 이용하여 다음 토큰의
확률 분포를 만듭니다. 첫 입력은 문장의 시작을 뜻하는 `<BOS>`이고,
`<EOS>`를 예측하면 생성을 끝냅니다.

[03_decoder.py](03_decoder.py)는 `<BOS>`에서 시작해 `<EOS>`까지 한 토큰씩
생성하는 반복 구조를 보여 줍니다.

```bash
python 03_decoder.py
```

이 예제는 생성 순서에만 집중하기 위해 학습된 확률 분포 대신 작은
전이 사전을 사용합니다. 실제 Decoder는 매 단계 Softmax 확률에서 다음
토큰을 선택하고 상태도 함께 갱신합니다.

### Decoder의 학습 입력

목표가 `<BOS> I like NLP <EOS>`라면 다음처럼 한 칸 이동합니다.

| 위치 | Decoder 입력 | 예측 정답 |
|---:|---|---|
| 1 | `<BOS>` | `I` |
| 2 | `I` | `like` |
| 3 | `like` | `NLP` |
| 4 | `NLP` | `<EOS>` |

입력과 정답을 같은 위치로 주면 현재 정답을 그대로 보는 누수가 발생할 수 있습니다.

### Masked sequence loss

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

### Teacher forcing과 노출 편향

학습 중에는 이전 정답을 입력하지만 추론 중에는 이전 예측을 입력합니다. 한 번 잘못 예측하면 이후 입력 분포가 학습 때와 달라져 오류가 누적될 수 있습니다. 이를 노출 편향이라고 합니다.

Teacher forcing 비율을 낮추는 방법이 항상 개선을 보장하지는 않습니다. 우선 정답 시프트, `<EOS>` 학습, attention, 데이터 품질을 확인하고 동일 평가셋에서 비교합니다.

### Greedy decoding 의사코드

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

### 번역 결과 진단

- 누락: 원문의 핵심 구가 사라짐
- 추가: 원문에 없는 내용 생성
- 반복: 같은 단어나 구가 되풀이됨
- 조기 종료: 번역이 중간에 끝남
- 미등록어: 고유명사·숫자가 깨짐
- 문법은 자연스럽지만 의미가 반대임

BLEU 같은 자동 점수와 함께 위 유형을 최소 30문장에서 사람이 분류합니다. 숫자와 고유명사는 별도 정확도도 유용합니다.

## 10.1~10.3 확인 문제

1. 문장 확률 대신 로그 확률 합을 사용하는 이유는 무엇입니까?
2. Encoder의 마지막 상태는 Decoder에서 어떻게 사용됩니까?
3. Decoder가 `<BOS>`와 `<EOS>`를 필요로 하는 이유를 설명하세요.
4. decoder 입력과 target이 한 칸 다른 이유를 설명하세요.
5. 패딩 마스크 없이 손실을 계산하면 어떤 편향이 생깁니까?
