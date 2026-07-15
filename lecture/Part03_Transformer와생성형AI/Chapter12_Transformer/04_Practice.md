# 실습: Transformer 구현

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

작은 Transformer encoder로 token sequence의 이진 패턴을 분류합니다.

- [안내](examples/04_transformer_solution/README.md)
- [코드](examples/04_transformer_solution/transformer_encoder.py)
- [데이터](examples/04_transformer_solution/sequences.csv)

## 구현 순서

전체 Transformer를 한 번에 작성하지 않습니다.

```text
1. Positional Encoding
2. Padding/Causal mask
3. Scaled Dot-Product Attention
4. Multi-Head Attention
5. FFN
6. Encoder Block
7. 작은 분류 모델
```

## Encoder Block

```python
class EncoderBlock(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attn = tf.keras.layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=d_model // num_heads
        )
        self.ffn = tf.keras.Sequential([
            tf.keras.layers.Dense(d_ff, activation="relu"),
            tf.keras.layers.Dense(d_model),
        ])
        self.norm1 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.norm2 = tf.keras.layers.LayerNormalization(epsilon=1e-6)
        self.drop1 = tf.keras.layers.Dropout(dropout)
        self.drop2 = tf.keras.layers.Dropout(dropout)

    def call(self, x, mask=None, training=False):
        a = self.attn(x, x, attention_mask=mask, training=training)
        x = self.norm1(x + self.drop1(a, training=training))
        f = self.ffn(x)
        return self.norm2(x + self.drop2(f, training=training))
```

## Shape 단위 테스트

```python
x = tf.random.normal((2, 10, 64))
block = EncoderBlock(64, 4, 128)
y = block(x, training=False)
assert y.shape == x.shape
```

`d_model=64`, head 4이므로 head 차원은 16입니다.

## Mask 테스트

PAD를 추가한 입력과 추가하지 않은 입력의 실제 토큰 출력이 허용 오차 안에서 비슷한지 확인합니다. 라이브러리의 `attention_mask` shape와 True/False 의미를 공식 문서 기준으로 맞춥니다.

## 작은 데이터 과적합

20개 sequence에서 분류 loss가 충분히 내려가는지 확인합니다. 실패하면 큰 데이터 학습 전에 mask, label, loss, gradient를 점검합니다.

## 비교 실험

| 실험 | Head | d_ff | Layer | Val F1 | Memory |
|---|---:|---:|---:|---:|---:|
| base | 4 | 128 | 1 | 기록 | 기록 |
| e01 | 8 | 128 | 1 | 기록 | 기록 |
| e02 | 4 | 256 | 1 | 기록 | 기록 |

한 번에 한 값만 바꿉니다.

## 완료 기준

Positional Encoding 차이, 미래/PAD mask, Attention 행합, 블록 shape, 작은 데이터 과적합, 저장 후 재로딩을 검증합니다.
