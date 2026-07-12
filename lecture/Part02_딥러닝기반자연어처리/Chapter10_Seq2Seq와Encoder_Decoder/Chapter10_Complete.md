# Chapter 10 통합 강의 원고

입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 10. Seq2Seq와 Encoder-Decoder

1. [Seq2Seq·Encoder·Decoder](01_Seq2Seq_Architecture.md)
2. [Teacher Forcing](02_Teacher_Forcing.md)
3. [Beam Search](03_Beam_Search.md)
4. [번역 모델 설계와 평가](04_Translation_Evaluation.md)
5. [요약과 퀴즈](05_Summary_and_Quiz.md)
6. [실습: 번역 모델 구현](06_Practice.md)

이 장은 교육용 문자 단위 번역 모델로 입력/출력 tensor와 inference loop를 이해합니다. 실제 번역 품질을 위한 규모의 모델이 아닙니다.

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_번역모델_입출력_따라가기.md -->

# Chapter 10 번역 모델 입출력 따라가기

## 번역을 두 사람의 협업으로 이해하기

Encoder는 원문을 읽고 핵심 정보를 정리하는 사람, Decoder는 그 정보를 받아 번역문을 한 단어씩 작성하는 사람입니다. 기본 Seq2Seq에서는 Encoder의 마지막 메모가 두 사람 사이의 메모지 역할을 합니다.

## 학습 데이터 만들기

원문 `나는 학생이다`, 번역문 `I am a student`에 특수 토큰을 붙입니다.

```text
source: 나는 학생이다 <EOS>
target 전체: <BOS> I am a student <EOS>
decoder 입력: <BOS> I am a student
학습 정답:     I am a student <EOS>
```

Decoder 입력과 정답은 한 칸 차이입니다. 현재 단어를 보고 같은 현재 단어를 맞히게 만들면 학습 목표가 잘못됩니다.

## 확률의 곱

\[
P(y|x)=P(I|x)P(am|I,x)P(a|I,am,x)\cdots
\]

각 단어 확률이 `[0.8,0.7,0.9]`라면 세 토큰 문장의 확률은 `0.8×0.7×0.9=0.504`입니다. 문장이 길수록 곱은 매우 작아지므로 로그를 더합니다.

\[
\log P(y|x)=\sum_t\log P(y_t|y_{<t},x)
\]

## Teacher Forcing

학습 중 이전 정답 단어를 다음 입력으로 주는 방식입니다. 초보 번역가에게 매 단계 올바른 앞 단어를 보여주며 연습시키는 것과 비슷합니다. 실제 번역에서는 자신의 이전 예측을 사용하므로 한 번의 오류가 뒤로 이어질 수 있습니다.

## 패딩 손실 제외

문장 길이를 맞추기 위해 붙인 `<PAD>`는 번역할 내용이 아닙니다. PAD까지 정답으로 많이 학습하면 짧은 문장에서 PAD 예측이 손실 대부분을 차지할 수 있습니다.

```python
mask = tf.cast(target != PAD_ID, token_loss.dtype)
loss = tf.reduce_sum(token_loss * mask) / tf.reduce_sum(mask)
```

분모도 실제 토큰 수여야 합니다.

## Greedy decoding

매 단계 가장 확률 높은 단어 하나를 선택합니다. 빠르지만 초기에 두 번째 후보를 버려 문장 전체로는 더 좋은 번역을 놓칠 수 있습니다.

## Beam Search 숫자 예

첫 단계 후보:

```text
I: -0.2, You: -0.5
```

다음 단계 누적 로그 점수:

```text
I am: -0.3
I like: -1.0
You are: -0.7
You like: -0.9
```

beam 2라면 `I am`, `You are`를 남깁니다. 점수는 확률 곱 대신 로그 확률 합을 사용합니다.

## 길이 편향

토큰을 추가할수록 로그 확률 합은 보통 더 작아져 짧은 문장이 유리할 수 있습니다. 길이 정규화로 완화하지만 계수는 validation에서 선택합니다.

## 종료 조건

`<EOS>`가 나오면 완료 후보로 옮기고 더 확장하지 않습니다. `<EOS>`가 나오지 않을 가능성에 대비해 최대 길이도 둡니다.

## 번역 오류 유형

| 유형 | 의미 |
|---|---|
| 누락 | 원문 내용이 빠짐 |
| 추가 | 원문에 없는 내용 생성 |
| 반복 | 같은 구절 반복 |
| 조기 종료 | 번역이 중간에 끝남 |
| 의미 반전 | 자연스럽지만 뜻이 반대 |
| 고유명사 오류 | 이름·숫자·코드가 변형 |

BLEU 점수만 보지 말고 각 유형별 실제 문장을 읽습니다.

## 확인 문제

1. Decoder 입력과 정답이 한 칸 다른 이유는?
2. 확률 대신 로그 확률을 더하는 이유는?
3. Teacher Forcing과 실제 추론의 차이는?
4. `<EOS>`와 최대 길이가 모두 필요한 이유는?

---

<!-- SOURCE: 00_번역평가와_오류개선.md -->

# Chapter 10 번역 평가와 오류 개선

## 번역은 정답이 하나가 아니다

“How are you?”는 “어떻게 지내?”, “잘 지내세요?” 등 여러 번역이 가능합니다. 자동 지표 하나로 품질 전체를 판단하지 않습니다.

## Token accuracy의 한계

각 위치 토큰이 정답과 같은 비율은 간단하지만 표현이 다른 좋은 번역을 오답 처리합니다. Teacher Forcing 조건의 정확도와 실제 자유 생성 품질도 다릅니다.

## BLEU의 직관

후보 번역의 n-gram이 참고 번역과 얼마나 겹치는지 계산하고 지나치게 짧은 번역에 벌점을 줍니다.

\[
BLEU=BP\times\exp\left(\sum_nw_n\log p_n\right)
\]

`p_n`은 n-gram precision, `w_n`은 비중, BP는 brevity penalty입니다. 짧은 문장 한두 개의 BLEU는 불안정할 수 있습니다.

## 길이 비율

\[
LengthRatio=\frac{생성토큰수}{참고토큰수}
\]

평균이 0.6이면 번역이 지나치게 짧아 누락이 많을 수 있습니다. 1.5면 반복·추가를 의심합니다.

## 오류 taxonomy

| 오류 | 확인 질문 |
|---|---|
| 누락 | 원문 핵심 조건이 빠졌나? |
| 추가 | 근거 없는 내용이 생겼나? |
| 의미 반전 | 부정·수량이 바뀌었나? |
| 고유명사 | 이름·숫자·코드가 유지됐나? |
| 반복 | 같은 구가 되풀이됐나? |
| 문법 | 목표 언어로 자연스러운가? |

## Greedy와 Beam 비교

같은 100문장에서 BLEU, 길이 비율, 평균 지연, 반복률을 비교합니다. Beam이 느려졌지만 품질이 거의 같다면 greedy가 운영에 더 적합할 수 있습니다.

## Teacher Forcing ratio 실험

비율 1.0, 0.8 등 후보를 비교하되 학습 안정성과 실제 생성 오류를 함께 봅니다. Scheduled sampling이 항상 개선을 보장하지 않습니다.

## EOS 문제

- 너무 일찍 EOS: 번역 누락
- EOS를 생성하지 않음: 최대 길이까지 반복

EOS target이 학습 데이터에 포함됐는지, padding mask와 ID가 올바른지 확인합니다.

## 복사 문제

숫자·URL·제품명은 번역보다 복사가 필요할 수 있습니다. Subword와 OOV 처리, Attention 정렬을 확인합니다.

## 사람 평가

정확성, 유창성, 누락, 용어 일관성을 1~5점으로 평가하고 평가자 기준 예시를 제공합니다. 가능하면 두 명 이상이 일부 표본을 중복 평가합니다.

## 결과 보고

자동 지표, 사람 평가, 길이·지연, 오류 유형별 건수를 함께 제시합니다. 좋은 예만 고르지 않고 무작위 표본과 실패 사례를 포함합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 10 원리·수학·실습 가이드

## 1. 번역을 조건부 생성으로 보기

Seq2Seq는 입력 문장 `x`가 주어졌을 때 출력 토큰열 `y`의 확률을 모델링한다.

\[
P(y|x)=\prod_{t=1}^{T_y}P(y_t\mid y_{<t},x)
\]

“나는 학생이다”가 주어지면 `<BOS> → I → am → a → student → <EOS>`처럼 앞서 생성한 토큰과 입력 정보를 이용해 다음 토큰을 예측한다.

## 2. Encoder와 Decoder

Encoder는 입력 `[B,T_x,D]`를 읽어 상태로 요약한다. Decoder는 그 상태와 이전 토큰으로 다음 로짓 `[B,V]`를 만든다. 고전 Seq2Seq는 마지막 상태 하나에 모든 정보를 압축하므로 긴 문장에서 병목이 생긴다. 다음 장의 Attention은 모든 encoder 상태를 다시 참고해 이 문제를 줄인다.

## 3. Teacher Forcing과 시프트

학습할 때 decoder 입력은 정답을 한 칸 오른쪽으로 민 값, 레이블은 정답 원문이다.

```text
decoder input: <BOS> I am a student
target:         I am a student <EOS>
```

Teacher forcing 비율 `r`은 이전 입력으로 정답 토큰을 사용할 확률이다. 학습은 빠르지만 추론 때는 자신의 예측을 입력하므로 노출 편향이 생긴다. scheduled sampling은 비율을 서서히 낮추지만 편향과 구현 복잡도를 함께 검토한다.

패딩 위치의 손실은 제외한다.

\[
L=-\frac{\sum_t m_t\log P(y_t|y_{<t},x)}{\sum_t m_t}
\]

`m_t`는 실제 토큰이면 1, 패딩이면 0이다.

## 4. Greedy와 Beam Search

Greedy는 매 단계 가장 높은 토큰 하나만 고른다. Beam search는 상위 `k`개 문장을 유지하며 누적 로그 확률을 비교한다.

\[
score(y)=\sum_t\log P(y_t|y_{<t},x)
\]

곱셈 대신 로그 합을 쓰면 매우 작은 확률의 수치 언더플로를 피한다. 누적합은 짧은 문장을 선호하므로 길이 정규화 `score/length^α`를 사용할 수 있다. beam을 키우면 항상 좋아지는 것이 아니라 느려지고 평범한 문장을 선호할 수도 있다.

## 5. 최소 구현 점검

```python
encoder_out, state_h, state_c = encoder(source_embeddings)
decoder_out, _, _ = decoder(target_embeddings, initial_state=[state_h, state_c])
logits = projection(decoder_out)  # [B, T_y, V]
```

- source/target tokenizer를 분리했는가?
- `<BOS>`, `<EOS>`, `<PAD>`, `<UNK>` ID를 고정했는가?
- target 입력과 레이블이 정확히 한 칸 시프트되었는가?
- 추론 루프가 `<EOS>` 또는 최대 길이에서 종료되는가?
- BLEU뿐 아니라 실제 번역 오류를 읽었는가?

1. `P(y|x)`가 토큰별 확률의 곱으로 표현되는 이유는?
2. Teacher forcing과 실제 추론의 차이는?
3. Beam search에서 로그 확률을 쓰는 이유는?

---

<!-- SOURCE: 01_Seq2Seq_Architecture.md -->

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

\[
P(y|x)=\prod_{t=1}^{T_y}P(y_t|y_1,\ldots,y_{t-1},x)
\]

각 단계에서 decoder는 어휘 크기 `V`개의 로짓을 만들고 Softmax로 다음 토큰 확률을 얻습니다. 문장 확률을 직접 곱하면 매우 작아지므로 평가와 탐색에서는 로그 확률 합을 사용합니다.

\[
\log P(y|x)=\sum_t\log P(y_t|y_{<t},x)
\]

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

\[
L=\frac{\sum_{b,t}m_{b,t}\,CE(y_{b,t},z_{b,t})}
{\sum_{b,t}m_{b,t}}
\]

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

---

<!-- SOURCE: 02_Teacher_Forcing.md -->

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

---

<!-- SOURCE: 03_Beam_Search.md -->

# 10.5 Beam Search

Greedy decoding은 각 단계에서 확률이 가장 높은 token 하나를 선택합니다. 빠르지만 초기에 내린 선택을 되돌릴 수 없습니다.

Beam Search는 상위 `beam_width`개의 부분 sequence를 유지합니다.

```text
각 후보 확장 → 누적 log probability 계산 → 상위 beam 유지 → 종료 조건 확인
```

확률을 곱하면 underflow가 발생하므로 log probability를 더합니다. 긴 문장이 불리해지는 문제를 줄이기 위해 length normalization을 사용하기도 합니다.

beam을 넓히면 계산량과 메모리가 증가하며 품질이 항상 향상되는 것은 아닙니다. 반복, 종료 실패와 문장 길이를 함께 평가합니다.

## 후보 확장 예

beam 2에서 첫 단계 후보가 `I:-0.2`, `You:-0.5`이고 다음 단계가 각각 `am:-0.1`, `like:-0.8`, `are:-0.2`, `like:-0.4`라면 누적 점수는 `I am:-0.3`, `I like:-1.0`, `You are:-0.7`, `You like:-0.9`입니다. 상위 두 후보 `I am`, `You are`를 유지합니다.

## 길이 정규화

로그 확률은 토큰을 추가할 때 대체로 더 작아져 짧은 문장을 선호합니다.

\[
score_{norm}(y)=\frac{\sum_t\log P(y_t|y_{<t},x)}{length(y)^\alpha}
\]

`α`가 클수록 길이 벌점을 완화합니다. validation 번역 품질과 길이 비율로 선택합니다.

## 완료 후보 관리

`<EOS>`가 나온 후보는 더 확장하지 않고 완료 목록에 둡니다. 활성 후보가 모두 완료되거나 최대 길이에 도달하면 종료합니다. 완료 후보와 미완료 후보의 점수 비교 규칙을 명확히 합니다.

## Beam 크기의 trade-off

beam을 늘리면 탐색 후보는 많아지지만 속도와 메모리 비용이 늘고, 모델 자체의 확률 편향 때문에 품질이 오히려 떨어질 수 있습니다. greedy, beam 2/4/8을 동일 데이터에서 비교합니다.

## 생성 결과 기록

원문, 정답, greedy, beam 결과, 로그 점수, 길이, 종료 원인을 저장합니다. 자동 점수만으로는 누락·추가·반복을 구분하기 어렵습니다.

---

<!-- SOURCE: 04_Translation_Evaluation.md -->

# 번역 모델 설계와 평가

데이터 split 전에 동일·유사 번역쌍을 그룹화해 누수를 방지합니다. source와 target 언어의 vocabulary, 시작·종료·padding token ID를 저장해야 inference를 재현할 수 있습니다.

평가:

- validation loss
- exact match(교육용 짧은 문장)
- BLEU/chrF 같은 자동 지표
- 의미 보존, 유창성, 누락·추가에 대한 사람 평가

자동 지표 하나만으로 번역 품질을 결론 내리지 않습니다. 이름·숫자·부정 표현과 도메인 용어를 별도 검사합니다.

실무 번역은 Transformer와 사전학습 모델이 일반적이지만 Encoder-Decoder와 decoding 개념은 이후 구조의 기반입니다.

## 자동 평가와 사람 평가를 함께 쓰기

BLEU는 참고 번역과 n-gram 겹침을 측정하지만 의미가 같은 다른 표현을 낮게 평가할 수 있습니다. 자동 지표는 모델 비교에 사용하고 실제 번역 오류를 사람이 함께 확인합니다.

## 평가표

| 원문 | 참고 | 생성 | 누락 | 추가 | 의미반전 | 고유명사 |
|---|---|---|---:|---:|---:|---:|
| 기록 | 기록 | 기록 | 0/1 | 0/1 | 0/1 | 0/1 |

최소 50~100문장의 무작위 표본을 평가합니다.

## 숫자·고유명사 정확도

계약·상품 번역에서는 자연스러움보다 숫자와 이름 보존이 중요할 수 있습니다.

\[
보존정확도=정확히보존된항목수/전체항목수
\]

제품 코드 40개 중 37개가 유지되면 92.5%입니다.

## 길이와 반복

생성/참고 길이 비율, 반복 n-gram 비율, EOS 도달률을 측정합니다. BLEU가 비슷해도 한 모델이 반복과 조기 종료가 많을 수 있습니다.

## Greedy와 Beam

Beam 1·2·4·8의 BLEU, 사람 점수, P95와 길이 비율을 비교합니다. Beam을 키웠는데 지연만 늘고 품질이 같다면 작은 beam을 선택합니다.

## 평가 분할

Train 문장과 거의 같은 문장이 test에 있지 않은지 중복을 검사합니다. 문장 길이, 도메인, 고유명사 포함 여부별로 성능을 나눕니다.

## 보고 방식

좋은 번역만 제시하지 않고 무작위 예, 최악 점수 예, 의미 반전 예를 함께 보여 줍니다. 모델이 사용할 수 없는 상황을 명확히 적습니다.

---

<!-- SOURCE: 05_Summary_and_Quiz.md -->

# 요약과 퀴즈

1. Encoder의 출력 state는 어디에 사용되나요? **Decoder 초기 상태**
2. Decoder input과 target은 어떻게 다른가요? **한 timestep 이동**
3. Teacher Forcing은 학습 중 무엇을 다음 입력으로 사용하나요? **정답 token**
4. exposure bias란? **학습과 inference의 decoder 입력 차이로 인한 오류 누적 문제**
5. Greedy와 Beam Search의 차이는? **하나의 후보 대 여러 상위 후보 유지**
6. Beam Search에서 log probability를 쓰는 이유는? **곱셈 underflow 방지**
7. 기본 Seq2Seq의 고정 context 병목을 완화하는 다음 기술은? **Attention**

---

<!-- SOURCE: 06_Practice.md -->

# 실습: 번역 모델 구현

짧은 영어-한국어 문자 단위 번역쌍으로 Encoder-Decoder를 학습하고 greedy inference 예제를 실행합니다.

- [안내](examples/06_translation_solution/README.md)
- [완성 코드](examples/06_translation_solution/seq2seq_translation.py)
- [데이터셋](examples/06_translation_solution/translations.csv)

실습 완료 후 tensor shape, teacher forcing용 shift, 시작·종료 token과 inference loop를 설명할 수 있어야 합니다.
