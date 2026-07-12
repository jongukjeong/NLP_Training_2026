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
