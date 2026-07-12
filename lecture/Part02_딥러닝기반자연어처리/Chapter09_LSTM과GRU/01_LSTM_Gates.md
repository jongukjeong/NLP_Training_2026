# 9.1 LSTM 구조 · 9.2~9.4 Gate

LSTM은 hidden state와 별도의 cell state를 유지해 긴 의존성 학습을 돕습니다.

- Forget Gate: 이전 cell state에서 무엇을 유지할지 결정
- Input Gate: 새 후보 정보를 얼마나 기록할지 결정
- Output Gate: cell state에서 현재 hidden state로 무엇을 노출할지 결정

Gate는 sigmoid 값 0~1로 정보 흐름을 조절하고 후보 state는 주로 tanh를 사용합니다. “기억한다”는 설명은 직관이며 실제로는 데이터에서 학습된 연속값 연산입니다.

```python
layers.Bidirectional(layers.LSTM(64, dropout=0.2))
```

전체 문장을 이용하는 감성 분류에서는 Bidirectional이 유용할 수 있지만 latency와 파라미터 수가 증가합니다.

## LSTM의 두 상태

LSTM은 외부로 보이는 단기 표현 `h_t`와 비교적 곧게 흐르는 기억 통로 `c_t`를 구분합니다. `c_t`는 오래 보존할 내용, `h_t`는 현재 단계에서 사용할 내용을 담는다고 이해할 수 있습니다.

## 세 게이트의 전체 식

\[
f_t=\sigma(W_f[x_t;h_{t-1}]+b_f)
\]
\[
i_t=\sigma(W_i[x_t;h_{t-1}]+b_i),\quad
\tilde c_t=\tanh(W_c[x_t;h_{t-1}]+b_c)
\]
\[
c_t=f_t\odot c_{t-1}+i_t\odot\tilde c_t
\]
\[
o_t=\sigma(W_o[x_t;h_{t-1}]+b_o),\quad
h_t=o_t\odot\tanh(c_t)
\]

세 Sigmoid 게이트는 각 기억 차원마다 0~1 값을 냅니다. 하나의 스위치가 아니라 64유닛이면 64개의 연속적인 조절 손잡이가 있는 셈입니다.

## 숫자로 게이트 계산하기

한 차원만 보겠습니다.

- 이전 기억 `c_{t-1}=0.6`
- forget gate `f_t=0.8`
- input gate `i_t=0.3`
- 후보 기억 `c̃_t=-0.5`

\[
c_t=0.8\times0.6+0.3\times(-0.5)=0.33
\]

이전 기억 0.48을 남기고 새 부정 정보 -0.15를 반영했습니다. output gate가 0.7이면 `h_t=0.7×tanh(0.33)≈0.223`입니다.

## 파라미터 수 계산

입력 차원 `D`, 은닉 크기 `H`인 LSTM은 네 종류의 계산을 하므로 대략 다음 파라미터를 가집니다.

\[
4H(D+H+1)
\]

`D=128`, `H=64`이면 `4×64×(128+64+1)=49,408`개입니다. 같은 크기의 SimpleRNN `H(D+H+1)=12,352`개보다 약 4배입니다. Bidirectional이면 방향별 층이 따로 있어 약 2배가 됩니다.

## Forget gate와 기울기

기억 상태에 대한 직접 미분에는 `f_t`가 나타납니다.

\[
\frac{\partial c_t}{\partial c_{t-1}}=f_t
\]

필요한 구간에서 forget 값이 1에 가까우면 기억과 기울기가 비교적 잘 유지됩니다. 항상 1이면 불필요한 기억까지 쌓이므로 입력에 따라 학습되어야 합니다.

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
2. `D=100`, `H=32`인 LSTM의 파라미터 수를 계산하세요.
3. 양방향 LSTM을 사용할 수 없는 운영 사례를 제시하세요.
