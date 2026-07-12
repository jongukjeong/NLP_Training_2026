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
