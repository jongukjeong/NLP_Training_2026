# Chapter 11. Attention Mechanism — 통합 원고

> 이 문서는 Chapter 11. Attention Mechanism 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 11. Attention Mechanism — `README.md`
- 11.1~11.4 Attention — `01_Attention.md`
- 요약과 퀴즈 — `02_Summary_and_Quiz.md`
- 실습: Attention Visualization — `03_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 11. Attention Mechanism

# Chapter 11. Attention Mechanism

Attention의 등장 배경, Bahdanau(Additive), Luong(Multiplicative), Self Attention을 학습하고 attention weight를 시각화합니다.

1. [핵심 강의](01_Attention.md)
2. [요약과 퀴즈](02_Summary_and_Quiz.md)
3. [실습: Attention Visualization](03_Practice.md)


---

<!-- SOURCE: 01_Attention.md -->

# 11.1~11.4 Attention

# 11.1~11.4 Attention

고정 길이 context 하나에 입력 전체를 압축하는 Seq2Seq의 병목을 줄이기 위해 decoder가 매 timestep마다 encoder state를 선택적으로 참조합니다.

```text
score(query, key) → softmax → attention weights
weights × values의 가중합 → context
```

| 방식 | score 특징 |
|---|---|
| Bahdanau | query와 key를 작은 신경망에 넣는 additive attention |
| Luong | dot 또는 학습된 행렬을 사용하는 multiplicative attention |
| Self Attention | 같은 sequence에서 query, key, value를 생성 |

scaled dot-product attention은 `QKᵀ / sqrt(d_k)` 뒤 softmax를 적용합니다. 차원이 커질 때 dot product가 커져 softmax가 포화되는 것을 완화하기 위해 scale합니다.

Mask 종류:

- padding mask: padding token 참조 방지
- causal mask: 미래 token 참조 방지

Attention weight는 모델 내부 계산의 단서이지만 인간의 설명이나 인과적 근거와 동일하지 않습니다.


---

<!-- SOURCE: 02_Summary_and_Quiz.md -->

# 요약과 퀴즈

# 요약과 퀴즈

1. Attention이 완화한 Seq2Seq 병목은? **고정 context 압축**
2. Bahdanau 방식은 additive인가요? **예**
3. Luong의 대표 score는? **dot product 계열**
4. Self Attention의 Q/K/V는 어디서 오나요? **같은 sequence 표현**
5. `sqrt(d_k)`로 나누는 이유는? **큰 dot product와 softmax 포화 완화**
6. causal mask의 목적은? **미래 token 참조 차단**
7. attention weight를 인간 설명과 동일시해도 되나요? **아니요**


---

<!-- SOURCE: 03_Practice.md -->

# 실습: Attention Visualization

# 실습: Attention Visualization

- [안내](examples/03_attention_visualization_solution/README.md)
- [코드](examples/03_attention_visualization_solution/attention_visualization.py)
- [입력](examples/03_attention_visualization_solution/tokens.csv)

Q/K의 scaled dot-product weight를 CSV와 PNG heatmap으로 저장합니다.

