# Chapter 8 통합 강의 원고

---

<!-- SOURCE: README.md -->

# Chapter 8. 순환신경망(RNN)

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **순환신경망(Recurrent Neural Network, RNN): 이전 정보를 다음 시점으로 전달하는 신경망**
- **은닉 상태(Hidden State): 현재까지 읽은 정보를 요약해 다음 시점으로 전달하는 값**
- **시간 역전파(Backpropagation Through Time, BPTT): RNN을 시간축으로 펼쳐 기울기를 계산하는 방법**
- **기울기 소실(Vanishing Gradient): 역전파 과정에서 기울기가 지나치게 작아지는 문제**

1. [Sequence Data와 Vanilla RNN](01_Sequence_and_RNN.md)
2. [BPTT와 Vanishing Gradient](02_BPTT_and_Gradient.md)
3. [문장 분류 설계](03_Sentence_Classification.md)
4. [퀴즈](04_Summary_and_Quiz.md)
5. [실습: 문장 분류](05_Practice.md)

목표는 timestep, hidden state, padding/masking과 RNN의 gradient 한계를 이해하고 문장 분류 모델을 완성하는 것입니다.

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: LEARNING_PATH.md -->

# Chapter 8 비전공자 학습 경로

## 기본 도달 목표

짧은 문장이 RNN을 통과하는 shape 흐름 확인

완성형 코드를 처음부터 모두 이해하거나 다시 작성하는 것은 기본 목표가 아닙니다.

## 1. Step by Step — 강사와 함께

1. 토큰 시퀀스를 확인한다
2. 배치·길이·차원 축을 구분한다
3. RNN 출력 shape를 확인한다
4. 문장 분류 결과를 비교한다

각 단계가 끝날 때 입력, 출력 또는 중간 결과를 화면에서 확인합니다. 설명할 수 없는 줄은 다음 단계로 넘어가기 전에 질문합니다.

## 2. Basic Practice — 짧은 흐름 연결

Step by Step의 네 단계를 한 흐름으로 연결합니다. 처음에는 함수 분리, 타입 힌트, 복잡한 예외 처리와 자동 보고서를 요구하지 않습니다.

완료 확인:

- 입력이 무엇인지 설명한다.
- 핵심 처리 한 단계를 찾아 수정한다.
- 출력이 예상과 다른 이유를 한 가지 찾는다.
- 실행 결과를 짧게 기록한다.

## 실행 코드 위치

- [Step by Step](examples/01_step_by_step/README.md)
- [Basic Practice](examples/02_basic_practice/README.md)
- [Practice Starter](examples/03_practice_starter/README.md)

세 자료는 외부 모델이나 API 없이 핵심 흐름을 먼저 이해하도록 구성했습니다. 실제 라이브러리와 완성형 구조는 기존 solution에서 비교합니다.

## 3. Practice·Assignment — 먼저 시도

[05_Practice.md](05_Practice.md)의 기본 요구사항을 먼저 수행합니다. 막히면 전체 solution 대신 필요한 단계의 힌트만 확인합니다.

## 4. Solution — 피드백 후 공개

[examples/05_sentence_classification_solution/README.md](examples/05_sentence_classification_solution/README.md)은 다수의 수강생이 기본 요구사항을 시도하고 공통 오류를 함께 확인한 뒤 공개합니다. 자신의 코드와 다음 항목을 비교합니다.

1. 반복되는 처리를 어떻게 묶었는가
2. 잘못된 입력을 어디에서 검사하는가
3. 결과를 어떻게 검증하고 기록하는가

## 선택 확장

- BPTT
- padding·mask
- 모델 비교
- 디버깅

선택 확장은 기본 완료 기준에 포함하지 않습니다.

---

<!-- SOURCE: 00_RNN_문장흐름_따라가기.md -->

# Chapter 8 RNN 문장 흐름 따라가기

## RNN을 메모하며 읽는 사람으로 이해하기

사람이 문장을 왼쪽부터 읽으며 머릿속 메모를 갱신한다고 생각해 봅시다. RNN의 hidden state는 지금까지 읽은 내용을 압축한 메모입니다.

```text
입력: 배송 / 이 / 너무 / 늦다
메모: 배송 → 배송 주제 → 정도 강조 → 부정적 배송 평가
```

실제 hidden state는 사람이 읽을 수 있는 문장이 아니라 숫자 벡터입니다.

## 한 시점의 계산

$$
h_t=\tanh(W_xx_t+W_hh_{t-1}+b)
$$

- `x_t`: 현재 단어 벡터
- `h_{t-1}`: 이전까지의 메모
- `W_x, W_h`: 어떤 정보를 중요하게 볼지 학습한 가중치
- `h_t`: 현재 단어까지 읽은 새 메모

스칼라 예에서 현재 입력 영향 0.6, 이전 메모 영향 0.3, 편향 0.1이면 합은 1.0이고 `tanh(1)≈0.762`가 새 상태입니다.

## 모든 시점 출력과 마지막 출력

문장 분류는 마지막 메모 `(B,H)`만 사용할 수 있습니다. 각 단어의 품사를 예측하려면 모든 위치의 상태 `(B,T,H)`가 필요합니다.

```python
last = tf.keras.layers.SimpleRNN(64)(x)
all_steps = tf.keras.layers.SimpleRNN(64, return_sequences=True)(x)
```

## 왜 앞부분을 잊는가

문장이 길어지면 초기 단어의 영향은 여러 단계의 곱을 거칩니다. 매 단계 0.8만 남는다고 단순화하면 20단계 뒤에는 `0.8²⁰≈0.0115`만 남습니다. “안” 같은 부정어가 문장 앞에 있고 판단 단어가 끝에 있으면 어려울 수 있습니다.

## Padding이 메모리에 미치는 영향

짧은 문장 뒤에 붙인 0은 실제 단어가 아닙니다. mask가 없다면 RNN은 padding도 여러 시점 읽으며 마지막 상태를 바꿀 수 있습니다.

```python
embedding = tf.keras.layers.Embedding(vocab_size, 64, mask_zero=True)
```

0번 ID는 padding 전용으로 두어야 합니다.

## 양방향 RNN

정방향은 왼쪽에서 오른쪽, 역방향은 오른쪽에서 왼쪽으로 읽습니다. 두 메모를 합치면 전체 문맥을 사용할 수 있습니다. 완성된 리뷰 분류에는 적합하지만 미래 단어가 아직 없는 실시간 다음 단어 예측에는 사용할 수 없습니다.

## 길이별 성능 분석

전체 정확도만 보면 긴 문장의 약점을 놓칠 수 있습니다.

| 토큰 길이 | 샘플 수 | F1 |
|---:|---:|---:|
| 1~10 | 기록 | 기록 |
| 11~30 | 기록 | 기록 |
| 31 이상 | 기록 | 기록 |

긴 문장에서만 급락하면 truncation, 기울기 소실, 부족한 긴 문장 학습 사례를 확인합니다.

## Gradient clipping 쉽게 이해하기

기울기 폭주는 수정량이 너무 커 학습이 튀는 현상입니다. clipping은 방향은 유지하면서 최대 이동 크기를 제한하는 안전벨트입니다. 손실된 장기 기억을 복구하는 기능은 아닙니다.

## RNN 오류 사례

- 문장축과 임베딩축을 반대로 입력
- mask가 중간 사용자 정의 층에서 사라짐
- `return_sequences` 설정이 다음 층과 맞지 않음
- 독립 문장인데 stateful 상태가 다음 batch로 전달
- 최대 길이가 너무 짧아 핵심 뒷부분이 잘림

## 확인 문제

1. hidden state를 일상 언어로 설명하세요.
2. 토큰 분류에 모든 시점 출력이 필요한 이유는?
3. 양방향 RNN이 실시간 생성에 부적절한 이유는?
4. clipping이 해결하는 문제는 무엇입니까?

---

<!-- SOURCE: 00_RNN_비교실험과_디버깅.md -->

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

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 8 원리·수학·실습 가이드

## 1. 순서가 중요한 데이터

“개가 사람을 물었다”와 “사람이 개를 물었다”는 단어 집합이 같아도 의미가 다르다. RNN은 현재 입력과 직전까지의 요약인 은닉 상태를 함께 사용한다.

$$
h_t=\tanh(W_{xh}x_t+W_{hh}h_{t-1}+b_h),\qquad y_t=W_{hy}h_t+b_y
$$

입력은 `[B,T,D]`, 은닉 상태는 매 시점 `[B,H]`다. 문장 분류에서는 마지막 유효 상태나 전체 상태를 풀링해 `[B,C]` 로짓을 만든다.

## 2. 시간축으로 펼쳐 보기

같은 RNN 셀이 `t=1…T`에서 반복되며 모든 시점이 같은 가중치를 공유한다. 따라서 문장 길이가 늘어도 파라미터 수는 늘지 않지만 계산 경로는 길어진다.

```python
rnn = tf.keras.layers.SimpleRNN(64, return_sequences=True)
x = tf.random.normal((32, 20, 128))
print(rnn(x).shape)  # (32, 20, 64)
```

`return_sequences=False`이면 마지막 출력 `[32,64]`, `True`이면 모든 시점 `[32,20,64]`을 반환한다.

## 3. BPTT와 기울기 문제

BPTT는 마지막 손실에서 시간축을 거슬러 미분한다. 먼 시점의 영향에는 반복적인 미분 곱이 들어간다.

$$
\frac{\partial L}{\partial h_t}=\frac{\partial L}{\partial h_T}
\prod_{k=t+1}^{T}\frac{\partial h_k}{\partial h_{k-1}}
$$

각 곱이 0.5라면 10단계 뒤 영향은 `0.5^10≈0.001`로 작아진다. 1.5라면 `1.5^10≈57.7`로 폭증한다. 전자는 장기 기억을 잃는 기울기 소실, 후자는 학습이 불안정한 기울기 폭주다.

대응책은 LSTM/GRU, 짧은 구간 학습, 적절한 초기화, gradient clipping이다.

```python
optimizer = tf.keras.optimizers.Adam(clipnorm=1.0)
```

## 4. 패딩과 마스크

배치 안 문장 길이를 맞추려고 0을 붙이지만 0은 실제 단어가 아니다. `Embedding(mask_zero=True)`로 패딩 위치가 RNN 상태에 영향을 주지 않게 한다. 전처리에서 패딩 ID와 실제 어휘 ID가 겹치지 않아야 한다.

## 5. 문장 분류 설계

```python
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(vocab_size, 128, mask_zero=True),
    tf.keras.layers.SimpleRNN(64),
    tf.keras.layers.Dense(num_classes),
])
```

검증 시 길이 구간별 성능을 따로 본다. 짧은 문장만 잘 맞고 긴 문장에서 급락한다면 장기 의존성이나 truncation을 의심한다.

## 흔한 오류와 확인 문제

- 문장축 `T`와 특성축 `D`를 바꾸어 입력함
- 패딩을 실제 토큰처럼 학습함
- 긴 문장을 모두 같은 최대 길이로 만들어 메모리를 낭비함
- 양방향 RNN을 실시간 다음 토큰 예측에 사용해 미래 정보가 누수됨

1. `[16,30,100]`을 `SimpleRNN(64)`에 넣으면 기본 출력 shape는?
2. `0.5^20`이 장기 기억에 의미하는 것은?
3. `mask_zero=True`가 필요한 이유는?

---

<!-- SOURCE: 01_Sequence_and_RNN.md -->

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

## RNN 셀 내부를 단계별로 계산하기

$$
h_t=\tanh(W_xx_t+W_hh_{t-1}+b)
$$

입력과 이전 기억을 각각 선형 변환해 더한 뒤 Tanh로 `-1~1` 범위의 새 상태를 만듭니다. 단순한 스칼라 예에서 `x_t=1`, `h_{t-1}=0.5`, `W_x=0.8`, `W_h=0.4`, `b=0`이면 Tanh 입력은 `1.0`, 새 상태는 약 `0.762`입니다.

다음 시점은 이 `0.762`를 다시 사용합니다. 같은 가중치가 모든 시점에 공유되므로 길이가 늘어도 파라미터 수는 그대로지만 계산 횟수와 기억 경로는 늘어납니다.

## 입력과 출력 shape 변형

| 설정 | 출력 shape | 사용 예 |
|---|---|---|
| `return_sequences=False` | `(B,H)` | 문장 전체 분류 |
| `return_sequences=True` | `(B,T,H)` | 토큰 분류, 다음 RNN, Attention |
| `return_state=True` | 출력과 마지막 상태 | Encoder-Decoder 상태 전달 |
| Bidirectional | 마지막 차원 보통 `2H` | 전체 문맥 분류 |

```python
layer = tf.keras.layers.SimpleRNN(
    64, return_sequences=True, return_state=True
)
sequence, final_state = layer(x)
print(sequence.shape)     # (B, T, 64)
print(final_state.shape)  # (B, 64)
```

## BPTT를 직관적으로 이해하기

마지막 분류 손실은 마지막 상태에 영향을 주고, 마지막 상태는 그 이전 상태에 의존합니다. 따라서 미분은 시간축을 거꾸로 통과합니다.

$$
\frac{\partial L}{\partial h_t}
=\frac{\partial L}{\partial h_T}
\prod_{k=t+1}^{T}\frac{\partial h_k}{\partial h_{k-1}}
$$

각 단계의 미분 크기가 평균 0.8이면 20단계 전 영향은 `0.8²⁰≈0.0115`입니다. 1.2이면 `1.2²⁰≈38.3`입니다. 앞은 기울기 소실, 뒤는 기울기 폭주입니다.

## 긴 문장의 실제 문제

문장 앞의 부정어가 뒤의 평가를 뒤집거나, 대명사가 오래전 명사를 가리키는 경우 긴 의존성이 필요합니다. SimpleRNN이 긴 문장에서 실패한다면 다음을 비교합니다.

1. 문장 길이 구간별 F1
2. truncation으로 잘린 비율
3. LSTM/GRU 교체 효과
4. gradient norm 분포
5. 양방향 사용 가능 여부

## Mask 전달 확인

`mask_zero=True`가 있어도 중간 사용자 정의 층이 mask를 버리면 RNN이 패딩을 읽을 수 있습니다.

```python
embedding = tf.keras.layers.Embedding(vocab_size, 64, mask_zero=True)
vectors = embedding(token_ids)
mask = embedding.compute_mask(token_ids)
print(mask[0])  # 실제 토큰 True, padding False
```

문장 끝 패딩과 앞쪽 패딩은 상태에 다른 영향을 줄 수 있습니다. 기본적인 RNN 실습에서는 뒤쪽 패딩과 명시적 mask를 권장합니다.

## Gradient clipping

Global norm이 임계값을 넘을 때 전체 기울기의 방향은 유지하면서 크기를 줄입니다.

$$
g' = g\times\frac{c}{\|g\|}\quad (\|g\|>c)
$$

norm 10인 기울기를 임계값 1로 자르면 크기가 1이 됩니다. clipping은 폭주를 완화하지만 소실된 기울기를 되살리지는 않습니다.

## 오류 분석 실습

- 길이 1~10, 11~30, 31 이상으로 평가를 나눕니다.
- 부정, 반전 접속사, 반복 표현, 미등록어 사례를 태깅합니다.
- 오분류가 전처리 문제인지 순서 모델 문제인지 구분합니다.
- 같은 파라미터 예산에서 평균 풀링 기준선과 비교합니다.

## 확인 문제

1. 모든 시점 출력이 필요한 두 가지 작업을 제시하세요.
2. `0.9³⁰`을 계산하고 기울기 흐름을 해석하세요.
3. clipping이 해결하는 문제와 해결하지 못하는 문제는 무엇입니까?

---

<!-- SOURCE: 02_BPTT_and_Gradient.md -->

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

## 연쇄법칙의 시간 전개

RNN 가중치는 모든 시점에 공유되므로 한 가중치의 gradient에는 각 시점의 기여가 더해집니다.

$$
\frac{\partial L}{\partial W_h}=\sum_t\frac{\partial L}{\partial h_t}\frac{\partial h_t}{\partial W_h}
$$

긴 문장은 계산 그래프가 깊어져 메모리와 시간이 증가합니다. Truncated BPTT는 일정 구간마다 상태를 분리해 계산 부담을 줄이지만 구간보다 먼 의존성은 직접 학습하기 어렵습니다.

## gradient norm 기록

```python
with tf.GradientTape() as tape:
    pred = model(x, training=True)
    loss = loss_fn(y, pred)
grads = tape.gradient(loss, model.trainable_variables)
print(float(tf.linalg.global_norm(grads)))
```

매우 큰 norm이 반복되면 clipping과 학습률을 검토합니다. 거의 0이면 activation 포화, 지나치게 긴 경로, gradient 단절 가능성을 봅니다.

## 상태 초기화

일반적인 독립 문장 배치는 각 문장을 0 상태에서 시작합니다. `stateful=True`는 배치 사이 상태를 유지하므로 샘플 순서와 batch 크기를 엄격히 관리해야 합니다. 서로 무관한 문장의 상태가 섞이면 누수가 됩니다.

## 해결책 비교

LSTM/GRU는 덧셈 기억 경로, gradient clipping은 폭주 제한, normalization은 분포 안정화, residual 연결은 짧은 gradient 경로를 제공합니다. 각 방법이 해결하는 문제가 다릅니다.

---

<!-- SOURCE: 03_Sentence_Classification.md -->

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

## 대표 벡터 선택

마지막 상태는 짧은 문장에는 간단하지만 앞쪽 정보가 희석될 수 있습니다. 전체 상태의 mean/max pooling은 모든 위치를 직접 요약하고, Attention은 입력에 따라 중요한 위치의 가중치를 학습합니다.

패딩을 포함한 max/mean pooling은 결과를 왜곡하므로 mask-aware 구현을 사용합니다.

## 양방향 RNN

정방향과 역방향 상태를 연결하면 각 토큰이 양쪽 문맥을 반영합니다. 문장 분류에는 유용하지만 파라미터·지연이 늘고 미래가 없는 스트리밍에는 사용할 수 없습니다.

## 길이별 배치

비슷한 길이의 문장을 같은 배치로 묶으면 패딩 계산을 줄입니다. 최대 길이는 무조건 데이터 최댓값보다 길이 분포의 상위 백분위와 잘린 샘플의 중요도를 보고 정합니다.

## 평가 실험

평균 풀링, SimpleRNN, Bidirectional RNN을 동일 임베딩 크기와 데이터 분할에서 비교합니다. 전체 F1뿐 아니라 길이 구간별 F1, 추론시간, 파라미터 수를 기록합니다.

## 오분류 읽기

부정어가 먼 문장, 핵심어가 처음에만 있는 문장, 중의적 표현, 과도하게 잘린 문장을 별도 태그로 분류합니다. 모델 변경 전에 반복되는 오류 유형이 전처리로 해결 가능한지 봅니다.

## 문장 표현을 만드는 세 가지 방법

RNN이 모든 시점에서 `(B,T,H)`를 출력했다면 분류에 사용할 `(B,H)` 문장 벡터를 만들어야 합니다.

1. 마지막 상태: 구현이 단순하지만 앞부분 정보가 약해질 수 있음
2. Masked mean/max pooling: 모든 시점을 요약하지만 순서별 중요도를 고정 방식으로 결합
3. Attention pooling: 입력에 따라 중요한 시점의 가중치를 학습

```python
embedding = layers.Embedding(vocab_size, 128, mask_zero=True)
x = embedding(inputs)
x = layers.Bidirectional(
    layers.SimpleRNN(64, return_sequences=True)
)(x)
x = layers.GlobalMaxPooling1D()(x)
outputs = layers.Dense(num_classes)(x)
```

`GlobalMaxPooling1D`이 padding을 올바르게 처리하는지는 구현과 입력값에 따라 확인해야 합니다. 안전하게 mask-aware pooling을 구현하거나 마지막 유효 상태를 사용합니다.

## 클래스 수에 따른 출력

3개 중 하나를 고르면 출력은 `(B,3)` logits입니다. 정수 레이블은 `SparseCategoricalCrossentropy(from_logits=True)`를 사용합니다.

```python
model.compile(
    optimizer="adam",
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"],
)
```

## 길이별 평가 코드

```python
lengths = (token_ids != 0).sum(axis=1)
groups = {
    "short": lengths <= 10,
    "medium": (lengths > 10) & (lengths <= 30),
    "long": lengths > 30,
}
for name, mask in groups.items():
    print(name, classification_report(y[mask], pred[mask]))
```

전체 F1과 함께 긴 문장 F1을 기록합니다. 긴 문장만 낮으면 truncation과 장기 의존성 문제를 구분합니다.

## 기준선과 비교

TF-IDF+선형 모델, 평균 임베딩, SimpleRNN을 같은 test에서 비교합니다. RNN이 순서를 사용한다는 설명만으로 채택하지 않고 실제 개선량과 지연을 측정합니다.

## 대표 오류

- “안 나쁘다”처럼 이중 부정
- 앞부분의 핵심 주제를 마지막 상태가 잊음
- 긴 문장의 결론이 최대 길이 밖에서 잘림
- padding mask 누락
- 양방향 모델로 미래 정보가 누수되는 실시간 과제

## 실험 보고

모델, 파라미터 수, 전체·길이별 F1, P95, 최대 길이, 잘린 문장 비율과 실제 오분류를 한 표에 정리합니다.

---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 퀴즈
1. RNN의 state는 무엇을 요약하나요? **이전 timestep까지의 정보**
2. Embedding 입력 shape는? **batch, timesteps**
3. `mask_zero=True`의 목적은? **0 padding 무시 지원**
4. BPTT는 어느 방향으로 gradient를 계산하나요? **시간축을 거슬러 역전파**
5. clipnorm이 주로 완화하는 문제는? **exploding gradient**
6. `return_sequences=True`가 필요한 경우는? **후속 layer가 전체 timestep 출력을 사용할 때**

---

<!-- SOURCE: 05_Practice.md -->

# 실습: 문장 분류

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

- [안내](examples/05_sentence_classification_solution/README.md)
- [완성 코드](examples/05_sentence_classification_solution/rnn_sentence_classifier.py)
- [데이터셋](examples/05_sentence_classification_solution/sentences.csv)
