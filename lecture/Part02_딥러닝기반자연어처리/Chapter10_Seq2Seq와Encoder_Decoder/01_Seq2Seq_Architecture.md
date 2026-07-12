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
