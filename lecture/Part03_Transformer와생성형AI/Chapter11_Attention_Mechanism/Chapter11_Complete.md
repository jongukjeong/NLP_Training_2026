# Chapter 11 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 11. Attention Mechanism

Attention의 등장 배경, Bahdanau(Additive), Luong(Multiplicative), Self Attention을 학습하고 attention weight를 시각화합니다.

1. [핵심 강의](01_Attention.md)
2. [요약과 퀴즈](02_Summary_and_Quiz.md)
3. [실습: Attention Visualization](03_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 11 원리·수학·실습 가이드

## 1. Attention의 질문

출력 토큰을 만들 때 입력의 어느 위치를 얼마나 참고할까? Attention은 관련도 점수를 확률처럼 정규화하고, 입력 정보의 가중합을 만든다.

\[
e_{t,s}=score(q_t,k_s),\quad \alpha_{t,s}=\frac{\exp(e_{t,s})}{\sum_j\exp(e_{t,j})},\quad c_t=\sum_s\alpha_{t,s}v_s
\]

가중치 `[0.1,0.7,0.2]`와 값 `[1,3,5]`라면 문맥은 `0.1×1+0.7×3+0.2×5=3.2`다. 가중치 합은 1이며, 패딩 위치는 Softmax 전에 매우 작은 값으로 마스킹한다.

## 2. Bahdanau와 Luong

Bahdanau(Additive)는 작은 신경망으로 점수를 계산한다.

\[
e_{t,s}=v^T\tanh(W_qq_t+W_kk_s)
\]

Luong(Dot/Multiplicative)은 내적을 사용한다: `e=q^Tk` 또는 `q^TWk`. 내적은 빠르지만 벡터 차원이 커지면 값이 커진다.

## 3. Self-Attention

같은 문장에서 Q, K, V를 만든다.

\[
Attention(Q,K,V)=softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\]

`Q,K,V:[B,T,d]`, 점수와 가중치 `[B,T,T]`, 출력 `[B,T,d]`다. `√d_k`로 나누어 Softmax가 한 위치에 지나치게 포화되는 것을 줄인다.

```python
scores = tf.matmul(q, k, transpose_b=True) / tf.math.sqrt(tf.cast(dk, tf.float32))
weights = tf.nn.softmax(scores + mask, axis=-1)
context = tf.matmul(weights, v)
```

## 4. 시각화 해석 주의

Attention heatmap은 모델이 참고한 패턴을 보여주지만 완전한 인과 설명은 아니다. head별 패턴, 패딩 마스크, 토큰 분할을 함께 표시하고 서로 다른 문장에서도 반복되는지 확인한다.

1. 가중치 합이 1인 이유는?
2. `[B,T,d]@[B,d,T]` 점수 shape는?
3. `√d_k` 스케일링의 목적은?

---

<!-- SOURCE: 01_Attention.md -->

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

- [안내](examples/03_attention_visualization_solution/README.md)
- [코드](examples/03_attention_visualization_solution/attention_visualization.py)
- [입력](examples/03_attention_visualization_solution/tokens.csv)

Q/K의 scaled dot-product weight를 CSV와 PNG heatmap으로 저장합니다.

