# Chapter 8. 순환신경망(RNN) — 통합 원고

> 이 문서는 Chapter 8. 순환신경망(RNN) 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 8. 순환신경망(RNN) — `README.md`
- 8.1 Sequence Data · 8.2 Vanilla RNN — `01_Sequence_and_RNN.md`
- 8.3 BPTT · 8.4 Vanishing Gradient — `02_BPTT_and_Gradient.md`
- 문장 분류 설계 — `03_Sentence_Classification.md`
- 요약과 퀴즈 — `04_Summary_and_Quiz.md`
- 실습: 문장 분류 — `05_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 8. 순환신경망(RNN)

# Chapter 8. 순환신경망(RNN)

1. [Sequence Data와 Vanilla RNN](01_Sequence_and_RNN.md)
2. [BPTT와 Vanishing Gradient](02_BPTT_and_Gradient.md)
3. [문장 분류 설계](03_Sentence_Classification.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: 문장 분류](05_Practice.md)

목표는 timestep, hidden state, padding/masking과 RNN의 gradient 한계를 이해하고 문장 분류 모델을 완성하는 것입니다.


---

<!-- SOURCE: 01_Sequence_and_RNN.md -->

# 8.1 Sequence Data · 8.2 Vanilla RNN

# 8.1 Sequence Data · 8.2 Vanilla RNN

Sequence data는 순서가 의미를 가집니다. 문장은 길이가 다르므로 정수 토큰을 padding해 `(batch, timesteps)` 형태로 만들고 Embedding을 거쳐 `(batch, timesteps, features)`로 변환합니다.

RNN은 현재 입력과 이전 hidden state로 새 hidden state를 계산합니다.

```text
h_t = tanh(W_x x_t + W_h h_(t-1) + b)
```

```python
layers.Embedding(vocab_size, 32, mask_zero=True)
layers.SimpleRNN(32)
```

`mask_zero=True`는 0 padding timestep을 후속 mask 지원 layer가 무시하도록 돕습니다. 0은 실제 단어 ID로 사용하지 않습니다.

`return_sequences=False`는 마지막 출력만, `True`는 모든 timestep 출력을 반환합니다. 다음 recurrent layer나 attention에 전체 sequence가 필요하면 `True`를 사용합니다.


---

<!-- SOURCE: 02_BPTT_and_Gradient.md -->

# 8.3 BPTT · 8.4 Vanishing Gradient

# 8.3 BPTT · 8.4 Vanishing Gradient

BPTT(Backpropagation Through Time)는 펼쳐진 timestep을 따라 gradient를 역전파합니다. 긴 sequence에서는 같은 변환이 반복되며 gradient가 매우 작아지거나 커질 수 있습니다.

- vanishing gradient: 먼 과거 정보 학습 어려움
- exploding gradient: 학습 불안정·NaN

대응:

- LSTM/GRU 사용
- gradient clipping
- 적절한 sequence 길이
- normalization과 초기화
- validation curve와 gradient 이상 감시

```python
optimizer = keras.optimizers.Adam(clipnorm=1.0)
```

clip은 exploding gradient를 완화하지만 vanishing gradient의 근본 해결책은 아닙니다.


---

<!-- SOURCE: 03_Sentence_Classification.md -->

# 문장 분류 설계

# 문장 분류 설계

```text
문장 → TextVectorization(output_sequence_length=N)
→ Embedding(mask_zero=True) → SimpleRNN → Dense
```

최대 길이가 너무 짧으면 정보가 잘리고 너무 길면 계산량과 padding이 증가합니다. training data의 길이 분위수를 기준으로 정하고 잘린 비율을 기록합니다.

비교 실험:

- multi-hot MLP 기준선
- SimpleRNN
- sequence 길이 변화
- 단방향과 양방향 RNN

양방향 모델은 전체 문장을 본 뒤 분류하는 작업에는 적합하지만 미래 token을 볼 수 없는 실시간 생성에는 사용할 수 없습니다.


---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 요약과 퀴즈

# 요약과 퀴즈

1. RNN의 state는 무엇을 요약하나요? **이전 timestep까지의 정보**
2. Embedding 입력 shape는? **batch, timesteps**
3. `mask_zero=True`의 목적은? **0 padding 무시 지원**
4. BPTT는 어느 방향으로 gradient를 계산하나요? **시간축을 거슬러 역전파**
5. clipnorm이 주로 완화하는 문제는? **exploding gradient**
6. `return_sequences=True`가 필요한 경우는? **후속 layer가 전체 timestep 출력을 사용할 때**


---

<!-- SOURCE: 05_Practice.md -->

# 실습: 문장 분류

# 실습: 문장 분류

- [안내](examples/05_sentence_classification_solution/README.md)
- [완성 코드](examples/05_sentence_classification_solution/rnn_sentence_classifier.py)
- [데이터셋](examples/05_sentence_classification_solution/sentences.csv)

