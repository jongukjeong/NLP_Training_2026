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
