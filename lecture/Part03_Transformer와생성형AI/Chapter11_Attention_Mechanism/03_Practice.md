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
