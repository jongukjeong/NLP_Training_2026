# 10.5 Beam Search

Greedy decoding은 각 단계에서 확률이 가장 높은 token 하나를 선택합니다. 빠르지만 초기에 내린 선택을 되돌릴 수 없습니다.

Beam Search는 상위 `beam_width`개의 부분 sequence를 유지합니다.

```text
각 후보 확장 → 누적 log probability 계산 → 상위 beam 유지 → 종료 조건 확인
```

확률을 곱하면 underflow가 발생하므로 log probability를 더합니다. 긴 문장이 불리해지는 문제를 줄이기 위해 length normalization을 사용하기도 합니다.

beam을 넓히면 계산량과 메모리가 증가하며 품질이 항상 향상되는 것은 아닙니다. 반복, 종료 실패와 문장 길이를 함께 평가합니다.
