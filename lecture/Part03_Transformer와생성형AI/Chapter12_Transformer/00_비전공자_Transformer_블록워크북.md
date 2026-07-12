# Chapter 12 비전공자용 Transformer 블록 워크북

## Transformer는 문장을 여러 번 다듬는 구조다

Transformer 블록은 각 토큰이 다른 토큰을 참고하게 한 뒤, 토큰별 작은 신경망으로 표현을 다시 가공합니다. 이 블록을 여러 층 쌓으면 단어 표면보다 문맥에 맞는 표현을 만들 수 있습니다.

```text
토큰 임베딩 + 위치 정보
→ Multi-Head Attention
→ 잔차 연결과 LayerNorm
→ Feed Forward Network
→ 잔차 연결과 LayerNorm
```

## 위치 정보가 필요한 이유

Self-Attention만 사용하면 입력 순서를 자동으로 알지 못합니다. “고양이가 강아지를 쫓았다”와 “강아지가 고양이를 쫓았다”는 단어가 같아도 의미가 다릅니다. Positional Encoding은 각 위치에 서로 다른 신호를 더해 순서 정보를 제공합니다.

\[
PE(pos,2i)=\sin\left(\frac{pos}{10000^{2i/d}}\right)
\]

\[
PE(pos,2i+1)=\cos\left(\frac{pos}{10000^{2i/d}}\right)
\]

수식 전체를 외울 필요는 없습니다. 위치마다 다른 주기의 파동 값을 만들고, 모델이 상대적인 위치 차이를 활용할 수 있게 한다는 의미가 중요합니다.

## Multi-Head는 여러 관점으로 관계를 본다

임베딩 차원 (d_{model}=12), Head 수 (h=3)이라면 Head 하나의 차원은 보통 (d_k=4)입니다. 세 Head가 각각 다른 관계를 계산한 뒤 결과를 이어 붙입니다.

\[
\operatorname{MultiHead}(Q,K,V)=\operatorname{Concat}(head_1,head_2,head_3)W^O
\]

Head 수를 늘린다고 정보량이 무조건 늘지는 않습니다. 전체 차원이 고정되면 Head 하나의 차원은 작아집니다.

## FFN은 토큰마다 같은 변환을 적용한다

\[
\operatorname{FFN}(x)=\sigma(xW_1+b_1)W_2+b_2
\]

Attention이 토큰 사이의 정보를 섞는다면 FFN은 각 토큰 표현 내부를 가공합니다. 모든 위치에 같은 가중치를 사용하지만 입력 표현이 다르므로 출력은 달라집니다.

## 잔차 연결은 원래 정보를 우회시킨다

\[
y=x+F(x)
\]

새 변환 (F(x))만 다음 층으로 보내지 않고 원래 입력 (x)를 더합니다. 깊은 네트워크에서도 정보와 Gradient가 흐르기 쉬워집니다. 더하려는 두 Tensor의 shape가 같아야 합니다.

## LayerNorm은 토큰별 값의 규모를 정돈한다

\[
\hat{x}=\frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}
\]

평균을 빼고 표준편차로 나눈 뒤 학습 가능한 크기와 위치를 적용합니다. `epsilon`은 분모가 0에 가까워지는 것을 막습니다.

## 길이가 두 배면 Attention 표는 네 배가 된다

토큰 수가 (n)일 때 Attention 점수 행렬은 (n\times n)입니다. 128 토큰은 16,384칸, 256 토큰은 65,536칸입니다. 긴 문맥에서 메모리 사용량이 빠르게 증가하는 이유입니다.

## 구현 오류를 찾는 순서

1. 입력과 출력 shape를 출력합니다.
2. Head 분할 전후 전체 원소 수가 같은지 확인합니다.
3. Softmax 축이 Key 위치축인지 확인합니다.
4. Mask 적용 후 금지 위치 값이 0에 가까운지 확인합니다.
5. 작은 데이터 한 Batch를 과적합할 수 있는지 확인합니다.

