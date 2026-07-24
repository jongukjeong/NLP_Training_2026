# 9.1 LSTM 구조 · 9.2~9.4 Gate

## 9.1 LSTM이 필요한 이유

기본 RNN은 문장을 왼쪽에서 오른쪽으로 읽으면서 이전 hidden state를 계속
갱신합니다. 문장이 길어지면 오래전 정보가 여러 번의 연산을 거쳐야 하므로
정보와 기울기가 작아지는 **기울기 소실(vanishing gradient)** 문제가 생길 수
있습니다.

LSTM(Long Short-Term Memory)은 기본 RNN에 다음 두 장치를 추가합니다.

1. 오래 전달할 정보를 담는 별도의 **cell state**를 둡니다.
2. 세 개의 **gate**가 정보를 지울지, 쓸지, 보여 줄지를 조절합니다.

예를 들어 “이 영화는 중간까지 지루했지만 **마지막은 정말 좋았다**”라는
문장을 읽는다고 생각해 봅시다. LSTM은 앞부분의 부정 정보와 뒷부분의 긍정
정보를 모두 상태에 반영하고, 학습된 gate를 통해 최종 판단에 필요한 정보를
선택합니다. Gate가 문법 규칙을 직접 아는 것은 아니며, 학습 과정에서 유용한
값을 내도록 파라미터가 조정됩니다.

## LSTM의 두 상태

| 상태 | 역할 | 직관 |
|---|---|---|
| cell state `c_t` | 비교적 긴 시간 전달되는 내부 기억 | 메모장 |
| hidden state `h_t` | 현재 시점의 출력이자 다음 시점의 입력 | 지금 보여 주는 요약 |

기본 RNN이 하나의 hidden state에 기억과 출력을 모두 담는다면, LSTM은
`c_t`와 `h_t`로 역할을 나눕니다. 여기서 “장기 기억”과 “단기 기억”은 이해를
돕는 표현입니다. 실제 상태는 사람이 읽을 수 있는 문장이 아니라 학습된
실수 벡터입니다.

한 시점 `t`에서 LSTM은 이전 상태 `h_{t-1}`, `c_{t-1}`와 현재 입력 `x_t`를
받아 새 상태 `h_t`, `c_t`를 만듭니다.

```text
(현재 입력 x_t, 이전 출력 h_{t-1}, 이전 기억 c_{t-1})
                         │
                         ▼
              forget → input → output gate
                         │
                         ▼
                   (새 출력 h_t, 새 기억 c_t)
```

## 세 Gate의 역할

- Forget Gate: 이전 cell state에서 무엇을 유지할지 결정
- Input Gate: 새 후보 정보를 얼마나 기록할지 결정
- Output Gate: cell state에서 현재 hidden state로 무엇을 노출할지 결정

Gate는 sigmoid 값 0~1로 정보 흐름을 조절하고 후보 state는 주로 tanh를 사용합니다. “기억한다”는 설명은 직관이며 실제로는 데이터에서 학습된 연속값 연산입니다.

## 세 게이트의 전체 식

$$
f_t=\sigma(W_f[x_t;h_{t-1}]+b_f)
$$
$$
i_t=\sigma(W_i[x_t;h_{t-1}]+b_i),\quad
\tilde c_t=\tanh(W_c[x_t;h_{t-1}]+b_c)
$$
$$
c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t
$$
$$
o_t=\sigma(W_o[x_t;h_{t-1}]+b_o),\quad
h_t=o_t\odot\tanh(c_t)
$$

세 Sigmoid 게이트는 각 기억 차원마다 0~1 값을 냅니다. 하나의 스위치가 아니라 64유닛이면 64개의 연속적인 조절 손잡이가 있는 셈입니다.

계산 순서를 말로 풀면 다음과 같습니다.

1. `f_t`로 이전 기억 `c_{t-1}` 중 남길 양을 정합니다.
2. `i_t`로 새 후보 기억 `c̃_t` 중 기록할 양을 정합니다.
3. 두 결과를 더해 새 cell state `c_t`를 만듭니다.
4. `o_t`로 새 기억 중 현재 hidden state `h_t`로 보여 줄 양을 정합니다.

## 9.2 Forget Gate: 이전 기억을 얼마나 남길까?

Forget Gate(망각 게이트)는 이전 cell state에 곱할 비율 `f_t`를 만듭니다.

$$
f_t=\sigma(W_f[x_t;h_{t-1}]+b_f)
$$

`f_t`는 이름과 달리 “잊을 양”이 아니라 **남길 양**입니다.

- `f_t ≈ 0`: 이전 기억을 거의 지웁니다.
- `f_t ≈ 1`: 이전 기억을 거의 그대로 유지합니다.
- `f_t ≈ 0.5`: 이전 기억의 절반 정도를 전달합니다.

예를 들어 이전 기억이 `[0.8, -0.4, 0.2]`이고 gate가
`[0.9, 0.1, 0.5]`라면 유지되는 기억은 `[0.72, -0.04, 0.10]`입니다.
Gate는 벡터의 모든 값을 한꺼번에 켜고 끄는 스위치가 아니라, 각 차원을
서로 다른 비율로 조절합니다.

[02_forget_gate.py](02_forget_gate.py)를 실행하면 같은 기억에 0.1, 0.5,
0.9를 각각 곱했을 때의 차이를 확인할 수 있습니다.

```bash
python 02_forget_gate.py
```

기억 상태에 대한 직접 미분에는 `f_t`가 나타납니다.

$$
\frac{\partial c_t}{\partial c_{t-1}}=f_t
$$

필요한 구간에서 `f_t`가 1에 가까우면 기억과 기울기가 비교적 잘
유지됩니다. 항상 1이면 불필요한 기억까지 쌓이므로 입력에 따라 적절한 값을
내도록 학습되어야 합니다.

## 9.3 Input Gate: 새 정보를 얼마나 기록할까?

Input Gate(입력 게이트)는 새 후보 기억 중 실제 cell state에 기록할 양을
정합니다.

$$
i_t=\sigma(W_i[x_t;h_{t-1}]+b_i)
$$

$$
\tilde c_t=\tanh(W_c[x_t;h_{t-1}]+b_c)
$$

여기에는 역할이 다른 두 값이 있습니다.

- 후보 기억 `c̃_t`: 새로 기록할 **내용**이며, 보통 -1~1의 값을 가집니다.
- input gate `i_t`: 그 내용을 기록할 **비율**이며, 0~1의 값을 가집니다.

따라서 `i_t` 자체가 새 기억은 아닙니다. 실제로 추가되는 정보는
`i_t ⊙ c̃_t`입니다. 예를 들어 후보 기억이 `-0.5`일 때 `i_t=0.3`이면
cell state에는 `-0.15`만 추가됩니다.

[03_input_gate.py](03_input_gate.py)는 같은 후보 기억에 input gate를
0.0, 0.3, 1.0으로 바꾸어 적용합니다.

```bash
python 03_input_gate.py
```

Forget Gate와 Input Gate의 결과를 합치면 새 cell state가 됩니다.

$$
c_t=\underbrace{f_t\odot c_{t-1}}_{\text{남긴 이전 기억}}
    +\underbrace{i_t\odot\tilde c_t}_{\text{기록할 새 기억}}
$$

## 9.4 Output Gate: 기억 중 무엇을 보여 줄까?

Output Gate(출력 게이트)는 갱신된 cell state 중 현재 hidden state로
노출할 양을 정합니다.

$$
o_t=\sigma(W_o[x_t;h_{t-1}]+b_o)
$$

$$
h_t=o_t\odot\tanh(c_t)
$$

cell state를 `tanh`로 -1~1 범위에 놓고 output gate를 곱합니다. 따라서
cell state에 정보가 남아 있어도 `o_t`가 0에 가까우면 현재 출력에는 거의
보이지 않습니다. 정보가 삭제된 것은 아니므로 다음 시점의 cell state로는
계속 전달될 수 있습니다.

[04_output_gate.py](04_output_gate.py)는 동일한 cell state에서 output
gate만 변경했을 때 hidden state가 어떻게 달라지는지 보여 줍니다.

```bash
python 04_output_gate.py
```

> **헷갈리기 쉬운 차이:** Forget Gate는 이전 `cell`을 바꾸고, Input
> Gate는 새 `cell`을 만드는 데 참여합니다. Output Gate는 완성된 `cell`을
> 삭제하지 않고 현재 `hidden`으로 보여 줄 양만 조절합니다.

## 세 Gate를 숫자로 함께 계산하기

한 차원만 보겠습니다.

- 이전 기억 `c_{t-1}=0.6`
- forget gate `f_t=0.8`
- input gate `i_t=0.3`
- 후보 기억 `c̃_t=-0.5`

$$
c_t=0.8\times0.6+0.3\times(-0.5)=0.33
$$

이전 기억 0.48을 남기고 새 부정 정보 -0.15를 반영했습니다. output gate가 0.7이면 `h_t=0.7×tanh(0.33)≈0.223`입니다.

## 예제 코드: 한 단계씩 상태 추적하기

[01_lstm_state.py](01_lstm_state.py)는 외부 라이브러리 없이 스칼라 하나로
forget/input/output gate와 두 상태의 변화를 출력합니다.

```bash
python 01_lstm_state.py
```

```python
forget = sigmoid(value + hidden + 1.0)
input_gate = sigmoid(value - hidden)
candidate = math.tanh(value + hidden)
output_gate = sigmoid(value + hidden)

cell = forget * cell + input_gate * candidate
hidden = output_gate * math.tanh(cell)
```

실제 LSTM은 위 값들이 스칼라가 아니라 벡터이고, 각 식에 서로 다른
가중치 행렬과 bias를 사용합니다. 예제는 학습 모델을 대신하는 코드가 아니라
`c_t = f_t c_{t-1} + i_t c̃_t`가 어떤 순서로 실행되는지 확인하기 위한
축소 모형입니다.

출력에서 다음을 확인합니다.

- `forget`이 1에 가까울수록 이전 `cell`이 많이 남습니다.
- `input`이 1에 가까울수록 `candidate`가 새 기억에 많이 반영됩니다.
- `output`은 `cell` 전체가 아니라 현재 `hidden`으로 노출할 양을 정합니다.

## Keras에서 LSTM 사용하기

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=10_000, output_dim=128, mask_zero=True),
    tf.keras.layers.LSTM(64, dropout=0.2),
    tf.keras.layers.Dense(1, activation="sigmoid"),
])
```

입력 shape이 `(batch, time)`이면 Embedding을 거쳐 `(batch, time, 128)`이
되고, `LSTM(64)`의 최종 출력은 `(batch, 64)`가 됩니다. 이 예에서는 마지막
Dense 층이 그 64차원 문장 표현으로 긍정 확률 하나를 예측합니다.

전체 문장을 이용하는 감성 분류에서는 다음과 같이 Bidirectional LSTM도
사용할 수 있습니다.

```python
tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, dropout=0.2))
```

양방향 모델은 앞뒤 문맥을 모두 보지만 latency와 파라미터 수가 증가합니다.

## 파라미터 수 계산

입력 차원 `D`, 은닉 크기 `H`인 LSTM은 네 종류의 계산을 하므로 대략 다음 파라미터를 가집니다.

$$
4H(D+H+1)
$$

`D=128`, `H=64`이면 `4×64×(128+64+1)=49,408`개입니다. 같은 크기의 SimpleRNN `H(D+H+1)=12,352`개보다 약 4배입니다. Bidirectional이면 방향별 층이 따로 있어 약 2배가 됩니다.

## LSTM 출력 설정

```python
lstm = tf.keras.layers.LSTM(
    64,
    return_sequences=True,
    return_state=True,
    dropout=0.2,
    recurrent_dropout=0.0,
)
sequence, h, c = lstm(vectors, mask=mask)
```

`sequence`는 `(B,T,64)`, `h`와 `c`는 `(B,64)`입니다. GPU 최적화 경로는 설정에 따라 달라질 수 있으므로 `recurrent_dropout`을 무조건 켜기보다 속도와 성능을 측정합니다.

## 양방향 모델의 정보 누수 판단

완성된 리뷰의 감성 분류는 미래 토큰을 봐도 되므로 양방향이 자연스럽습니다. 반면 타이핑 중 다음 단어 예측이나 실시간 스트림 판단은 미래 입력이 없으므로 양방향 결과를 그대로 사용할 수 없습니다. 학습 성능보다 운영 시점에 실제로 이용 가능한 정보인지 먼저 확인합니다.

## 감성 분석 오류 유형

| 유형 | 예문 | 점검 |
|---|---|---|
| 부정 | 재미있지 않다 | 부정어 범위 |
| 반전 | 느리지만 결과는 좋다 | 뒤 절의 영향 |
| 강도 | 정말 매우 좋다 | 정도 부사 |
| 풍자 | 참 잘도 만들었다 | 표면과 의도 차이 |
| 도메인 | 배터리가 가볍다 | 도메인별 의미 |

전체 정확도뿐 아니라 이 도전 세트의 정확도를 따로 기록합니다.

## 확인 문제

1. LSTM이 `h`와 `c`를 구분하는 이유를 설명하세요.
2. Forget Gate 값이 0과 1에 가까울 때 이전 기억은 각각 어떻게 됩니까?
3. 후보 기억 `c̃_t`와 Input Gate `i_t`의 역할 차이를 설명하세요.
4. Output Gate가 0에 가까우면 cell state의 정보도 삭제되는지 설명하세요.
5. `D=100`, `H=32`인 LSTM의 파라미터 수를 계산하세요.
6. 양방향 LSTM을 사용할 수 없는 운영 사례를 제시하세요.
