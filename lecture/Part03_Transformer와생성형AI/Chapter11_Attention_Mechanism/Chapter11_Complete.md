# Chapter 11 통합 강의 원고

---

<!-- SOURCE: README.md -->

# Chapter 11. Attention Mechanism

Attention의 등장 배경, Bahdanau(Additive), Luong(Multiplicative), Self Attention을 학습하고 attention weight를 시각화합니다.

1. [핵심 강의](01_Attention.md)
2. [퀴즈](02_Summary_and_Quiz.md)
3. [실습: Attention Visualization](03_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_Attention_비교실험과_오류진단.md -->

# Chapter 11 Attention 비교 실험과 오류 진단

## 실험 질문

Attention이 실제로 어떤 도움을 주는지 확인하려면 RNN 마지막 상태만 사용하는 모델과 Attention을 추가한 모델을 같은 조건에서 비교합니다.

| 모델 | 전체 F1 | 긴 문장 F1 | Params | P95 |
|---|---:|---:|---:|---:|
| RNN | 기록 | 기록 | 기록 | 기록 |
| RNN+Attention | 기록 | 기록 | 기록 | 기록 |

긴 문장 성능이 개선되면 입력 전체를 다시 참고하는 구조가 도움을 줬다고 해석할 수 있습니다. 전체 성능이 같다면 추가 계산 비용을 고려합니다.

## Alignment 품질

번역에서 사람이 기대하는 원문-번역 단어 대응을 소규모로 표시하고 Attention 최대 위치와 비교합니다. 자연스러운 번역이 반드시 단어별 일대일 정렬을 갖는 것은 아니므로 보조 지표로 사용합니다.

## Entropy

Attention 분포가 한 위치에 집중하는지 넓게 퍼지는지 측정할 수 있습니다.

\[
H(\alpha)=-\sum_i\alpha_i\log\alpha_i
\]

`[1,0,0]`은 entropy가 낮고 `[1/3,1/3,1/3]`은 높습니다. 낮다고 항상 좋은 것은 아니며 여러 단어를 함께 봐야 하는 질문은 분산이 자연스럽습니다.

## 오류 진단

- 모든 행이 거의 같은 분포: Q가 구분되지 않거나 학습 부족
- PAD에 큰 가중치: mask 축·값 오류
- 한 토큰에만 항상 집중: Softmax 포화, 데이터 편향
- NaN: 큰 점수, 잘못된 mask, dtype 문제
- 시각화 토큰 불일치: tokenizer 결과와 라벨 순서 확인

## 강의 질문

“어디를 보았는가”와 “왜 최종 답을 냈는가”는 같은 질문인가? 여러 층·head와 FFN이 함께 작동하므로 다르다는 점을 토론합니다.

---

<!-- SOURCE: 00_Attention_행렬과_시각화_읽기.md -->

# Chapter 11 Attention 행렬과 시각화 읽기

## Attention 표의 행과 열

Attention heatmap을 보기 전에 행과 열이 무엇인지 확인해야 합니다. 일반적으로 행은 질문하는 Query 위치, 열은 참고 대상인 Key 위치입니다.

```text
          나는  학교에  간다
나는      0.6   0.2    0.2
학교에    0.2   0.5    0.3
간다      0.1   0.3    0.6
```

첫 행은 `나는`이 세 토큰을 각각 60%, 20%, 20% 참고했다는 뜻입니다. 각 행의 합은 1에 가깝습니다.

## 점수에서 가중치까지

Query와 Key의 내적으로 원점수를 계산합니다.

\[
S=\frac{QK^T}{\sqrt{d_k}}
\]

점수 `[2,1,0]`에 Softmax를 적용하면 약 `[0.665,0.245,0.090]`입니다. 가장 큰 점수가 가장 높은 비율을 받지만 나머지가 완전히 0은 아닙니다.

## 행렬 shape 따라가기

`B=2`, `T=4`, `d_k=8`이라고 합시다.

```text
Q:       (2,4,8)
K^T:     (2,8,4)
QK^T:    (2,4,4)
weights: (2,4,4)
V:       (2,4,8)
output:  (2,4,8)
```

점수 행렬의 마지막 두 축은 “각 Query 위치 × 각 Key 위치”입니다.

## Padding mask

문장 길이를 맞추기 위해 붙인 PAD는 참고 대상이 아닙니다. PAD 점수에 매우 작은 음수를 더하면 Softmax 후 0에 가까워집니다.

```python
scores += (1.0 - mask) * -1e9
weights = tf.nn.softmax(scores, axis=-1)
```

mask shape가 점수 행렬에 맞게 broadcast되는지 출력합니다. 잘못된 축에 적용하면 실제 단어가 가려질 수 있습니다.

## Causal mask와 차이

Padding mask는 빈칸을 가리고, causal mask는 아직 생성하지 않은 미래 단어를 가립니다. 번역 Decoder와 GPT에서는 둘을 함께 사용할 수 있습니다.

## Multi-Head 시각화

Head마다 서로 다른 가중치 표가 있습니다. 평균만 보면 특정 head의 뚜렷한 패턴이 사라질 수 있습니다. head별 그림과 평균 그림을 모두 비교합니다.

## Subword 주의

Tokenizer가 `자연어처리`를 `자연`, `##어`, `##처리`처럼 나누면 heatmap에도 세 위치가 나타납니다. 사용자에게 보여줄 때는 원 단어로 합치거나 subword임을 표시합니다.

## 시각화가 설명할 수 없는 것

색이 진하다는 것은 해당 층·head의 계산에서 가중치가 컸다는 뜻입니다. 최종 예측에는 여러 층의 잔차 연결과 FFN도 영향을 줍니다. Attention 하나만 보고 모델의 전체 판단 이유라고 결론 내리지 않습니다.

## 실습 점검

1. 각 행 가중치 합이 약 1인가?
2. PAD와 미래 위치의 가중치가 0에 가까운가?
3. 행·열 토큰 순서가 실제 tokenizer 출력과 같은가?
4. head와 layer 번호를 기록했는가?
5. 다른 문장에서도 같은 패턴이 반복되는가?

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

## Attention을 검색으로 비유하기

Attention은 현재 필요한 정보를 문장 안에서 검색하는 과정과 비슷합니다. Query는 지금 찾는 내용, Key는 각 토큰의 색인, Value는 실제로 가져올 정보입니다. Query와 Key가 잘 맞을수록 해당 Value를 많이 가져옵니다.

\[
e_i=q^Tk_i,\qquad \alpha_i=\frac{e^{e_i}}{\sum_j e^{e_j}},\qquad c=\sum_i\alpha_iv_i
\]

기호를 풀면 `e_i`는 관련도 점수, `α_i`는 0~1 사이의 주목 비율, `c`는 최종 문맥 벡터입니다. Softmax 때문에 모든 `α`의 합은 1입니다.

### 작은 숫자로 계산하기

세 토큰 점수가 `[1, 3, 2]`라면 Softmax 가중치는 약 `[0.09, 0.67, 0.24]`입니다. 값이 스칼라 `[10, 20, 30]`일 때 문맥은 `0.09×10+0.67×20+0.24×30=21.5`입니다. 두 번째 토큰이 가장 중요하지만 다른 토큰 정보도 일부 섞입니다.

## Additive와 Dot-product의 차이

Bahdanau Attention은 Query와 Key를 작은 신경망에 넣어 점수를 학습합니다.

\[
e_i=v^T\tanh(W_qq+W_kk_i)
\]

Luong Attention은 내적 `q^Tk_i` 또는 변환이 포함된 `q^TWk_i`를 사용합니다. 내적은 행렬 곱으로 빠르게 계산하기 좋고, additive 방식은 서로 다른 표현 공간을 유연하게 맞출 수 있습니다.

## 왜 루트 차원으로 나누는가

Key 차원 `d_k`가 커지면 내적의 절댓값도 커져 Softmax가 거의 0 또는 1로 포화될 수 있습니다.

\[
Attention(Q,K,V)=softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\]

예를 들어 `d_k=64`이면 점수를 8로 나눕니다. 분포를 무조건 균등하게 만드는 것이 아니라 학습 초기에 gradient가 너무 작아지는 것을 완화합니다.

## Mask를 숫자로 이해하기

패딩 점수에 `-10^9` 같은 매우 작은 값을 더하면 Softmax 결과가 거의 0이 됩니다. mask는 Value를 지운 뒤 평균 내는 것이 아니라 Softmax 전에 점수에 적용해야 합니다.

## 시각화 실습 해석

heatmap의 행은 Query, 열은 Key로 두었는지 먼저 확인합니다. 토큰화로 한 단어가 여러 subword로 나뉘면 가중치도 나뉩니다. Attention이 높은 위치는 참고 관계의 단서지만 “이 위치 때문에 최종 예측했다”는 완전한 인과 설명으로 단정하지 않습니다.

## 확인 문제

1. Query, Key, Value를 도서 검색에 비유해 설명하세요.
2. 점수 `[0,0]`의 Softmax 결과는 무엇입니까?
3. padding mask를 Softmax 전에 적용하는 이유는 무엇입니까?

---

<!-- SOURCE: 02_Summary_and_Quiz.md -->

# 퀴즈
1. Attention이 완화한 Seq2Seq 병목은? **고정 context 압축**
2. Bahdanau 방식은 additive인가요? **예**
3. Luong의 대표 score는? **dot product 계열**
4. Self Attention의 Q/K/V는 어디서 오나요? **같은 sequence 표현**
5. `sqrt(d_k)`로 나누는 이유는? **큰 dot product와 softmax 포화 완화**
6. causal mask의 목적은? **미래 token 참조 차단**
7. attention weight를 인간 설명과 동일시해도 되나요? **아니요**

## 짧은 확인 문제

1. Query를 인터넷 검색에 비유하면 무엇입니까?
2. 가중치 `[0.3, 0.7]`, 값 `[10, 20]`의 가중합은 얼마입니까?
3. Attention heatmap이 완전한 원인 설명이 아닌 이유는 무엇입니까?
4. Self-Attention과 Cross-Attention의 차이를 한 문장으로 말해 보세요.
5. padding 토큰의 가중치는 왜 0이어야 합니까?

---

<!-- SOURCE: 03_Practice.md -->

# 실습: Attention Visualization

- [안내](examples/03_attention_visualization_solution/README.md)
- [코드](examples/03_attention_visualization_solution/attention_visualization.py)
- [입력](examples/03_attention_visualization_solution/tokens.csv)

Q/K의 scaled dot-product weight를 CSV와 PNG heatmap으로 저장합니다.

## 실습 입력

짧은 문장 여러 개를 사용해 먼저 Attention 행렬을 검증합니다.

```python
sentences = [
    "나는 자연어 처리를 공부한다",
    "배송은 느리지만 제품은 만족스럽다",
]
```

Tokenizer 결과와 원문 토큰을 함께 출력합니다. Subword 모델을 사용하면 화면 라벨도 subword 순서와 일치해야 합니다.

## Attention 가중치 계산

```python
scores = tf.matmul(q, k, transpose_b=True)
scores = scores / tf.math.sqrt(tf.cast(tf.shape(k)[-1], tf.float32))
scores += mask
weights = tf.nn.softmax(scores, axis=-1)
context = tf.matmul(weights, v)
```

`q,k,v`가 `(B,T,D)`라면 `weights`는 `(B,T,T)`, `context`는 `(B,T,D)`입니다.

## 검증 코드

```python
row_sums = tf.reduce_sum(weights, axis=-1)
tf.debugging.assert_near(row_sums, tf.ones_like(row_sums))
tf.debugging.assert_all_finite(weights, "Attention에 NaN/Inf")
```

Padding 위치의 최대 가중치도 확인합니다. 단순히 heatmap이 그려졌다는 이유로 계산이 맞다고 판단하지 않습니다.

## 시각화

```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.heatmap(weights[0].numpy(), xticklabels=tokens, yticklabels=tokens,
            cmap="Blues", vmin=0, vmax=1)
plt.xlabel("Key")
plt.ylabel("Query")
plt.tight_layout()
```

행·열 라벨, head, layer 번호와 mask 여부를 제목에 표시합니다.

## 비교 과제

Bahdanau, Luong dot, scaled dot-product 결과를 같은 입력으로 계산합니다. 가중치 entropy, 실행시간, 최댓값 위치를 비교합니다.

## 결과 보고

1. 입력과 token 목록
2. Q/K/V 및 가중치 shape
3. 행합 검증 결과
4. PAD 가중치
5. 세 방식 heatmap
6. Attention이 높은 위치에 대한 해석과 한계

## 자주 발생하는 오류

- Softmax axis를 Query 축에 적용
- mask에서 0과 1 의미가 반대
- 토큰 라벨 길이와 행렬 크기 불일치
- batch·head 축을 선택하지 않고 4차원 배열을 시각화
- 가중치를 최종 인과 설명으로 단정
