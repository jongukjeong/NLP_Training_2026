# 12.1 Transformer Architecture · 12.2 Positional Encoding

Transformer는 recurrence 없이 attention으로 token 관계를 계산합니다. Encoder는 bidirectional self-attention과 FFN을 쌓고, Decoder는 causal self-attention, encoder-decoder attention, FFN을 사용합니다.

Self Attention만으로는 token 순서를 구분하지 못하므로 positional encoding 또는 학습 가능한 position embedding을 더합니다.

```text
token embedding + position encoding → attention block
```

Sinusoidal encoding은 위치와 차원별 sin/cos 함수를 사용하며 학습 파라미터가 없습니다. 최대 sequence 길이와 embedding dimension의 shape를 확인해야 합니다.

## Transformer 한 블록을 따라가기

입력 토큰 ID `(B,T)`는 임베딩을 거쳐 `(B,T,d_model)`이 됩니다. 위치 정보를 더해도 shape는 변하지 않습니다. Multi-Head Attention, 잔차 연결, FFN을 지나도 마지막 shape는 계속 `(B,T,d_model)`로 유지됩니다.

```text
ID [B,T]
 → Embedding+Position [B,T,D]
 → Multi-Head Attention [B,T,D]
 → Add & Norm [B,T,D]
 → FFN [B,T,D]
 → Add & Norm [B,T,D]
```

## 위치 인코딩을 파동으로 이해하기

\[
PE(pos,2i)=\sin(pos/10000^{2i/d}),\quad
PE(pos,2i+1)=\cos(pos/10000^{2i/d})
\]

`pos`는 토큰 위치, `i`는 벡터 성분 번호, `d`는 모델 차원입니다. 빠르게 변하는 파동은 가까운 위치를 구분하고 느리게 변하는 파동은 먼 위치 정보를 제공합니다. 여러 주기의 시계바늘을 함께 읽어 위치를 표현한다고 생각할 수 있습니다.

## Multi-Head의 shape 계산

`B=32`, `T=100`, `d_model=512`, head 8이면 head당 차원은 64입니다. Q/K/V를 `(32,8,100,64)`로 나누고 점수는 `(32,8,100,100)`이 됩니다. head 출력을 다시 합치면 `(32,100,512)`입니다.

## 잔차 연결의 쉬운 의미

\[
y=x+F(x)
\]

층이 새로운 정보를 제대로 배우지 못해도 원래 입력 `x`가 통과할 길을 남깁니다. 덧셈이므로 `x`와 `F(x)`의 shape가 같아야 합니다. 잔차 연결은 “이전 내용을 지우고 새로 쓰기”보다 “이전 내용에 수정분 더하기”에 가깝습니다.

## 계산량

Attention 점수는 토큰 모든 쌍을 비교하므로 원소 수가 `T²`입니다. 길이 512면 한 head에 262,144개, 길이 1,024면 1,048,576개로 4배가 됩니다. 긴 문맥이 메모리를 빠르게 사용하는 이유입니다.

## 구현 검증

1. Attention 행렬 마지막 두 축이 `(T,T)`인지 확인합니다.
2. padding과 causal mask를 구분합니다.
3. 각 행의 Attention 가중치 합이 약 1인지 검사합니다.
4. 미래 위치 가중치가 0인지 작은 행렬로 출력합니다.
