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

## 대표 벡터 선택

마지막 상태는 짧은 문장에는 간단하지만 앞쪽 정보가 희석될 수 있습니다. 전체 상태의 mean/max pooling은 모든 위치를 직접 요약하고, Attention은 입력에 따라 중요한 위치의 가중치를 학습합니다.

패딩을 포함한 max/mean pooling은 결과를 왜곡하므로 mask-aware 구현을 사용합니다.

## 양방향 RNN

정방향과 역방향 상태를 연결하면 각 토큰이 양쪽 문맥을 반영합니다. 문장 분류에는 유용하지만 파라미터·지연이 늘고 미래가 없는 스트리밍에는 사용할 수 없습니다.

## 길이별 배치

비슷한 길이의 문장을 같은 배치로 묶으면 패딩 계산을 줄입니다. 최대 길이는 무조건 데이터 최댓값보다 길이 분포의 상위 백분위와 잘린 샘플의 중요도를 보고 정합니다.

## 평가 실험

평균 풀링, SimpleRNN, Bidirectional RNN을 동일 임베딩 크기와 데이터 분할에서 비교합니다. 전체 F1뿐 아니라 길이 구간별 F1, 추론시간, 파라미터 수를 기록합니다.

## 오분류 읽기

부정어가 먼 문장, 핵심어가 처음에만 있는 문장, 중의적 표현, 과도하게 잘린 문장을 별도 태그로 분류합니다. 모델 변경 전에 반복되는 오류 유형이 전처리로 해결 가능한지 봅니다.

## 문장 표현을 만드는 세 가지 방법

RNN이 모든 시점에서 `(B,T,H)`를 출력했다면 분류에 사용할 `(B,H)` 문장 벡터를 만들어야 합니다.

1. 마지막 상태: 구현이 단순하지만 앞부분 정보가 약해질 수 있음
2. Masked mean/max pooling: 모든 시점을 요약하지만 순서별 중요도를 고정 방식으로 결합
3. Attention pooling: 입력에 따라 중요한 시점의 가중치를 학습

```python
embedding = layers.Embedding(vocab_size, 128, mask_zero=True)
x = embedding(inputs)
x = layers.Bidirectional(
    layers.SimpleRNN(64, return_sequences=True)
)(x)
x = layers.GlobalMaxPooling1D()(x)
outputs = layers.Dense(num_classes)(x)
```

`GlobalMaxPooling1D`이 padding을 올바르게 처리하는지는 구현과 입력값에 따라 확인해야 합니다. 안전하게 mask-aware pooling을 구현하거나 마지막 유효 상태를 사용합니다.

## 클래스 수에 따른 출력

3개 중 하나를 고르면 출력은 `(B,3)` logits입니다. 정수 레이블은 `SparseCategoricalCrossentropy(from_logits=True)`를 사용합니다.

```python
model.compile(
    optimizer="adam",
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=["accuracy"],
)
```

## 길이별 평가 코드

```python
lengths = (token_ids != 0).sum(axis=1)
groups = {
    "short": lengths <= 10,
    "medium": (lengths > 10) & (lengths <= 30),
    "long": lengths > 30,
}
for name, mask in groups.items():
    print(name, classification_report(y[mask], pred[mask]))
```

전체 F1과 함께 긴 문장 F1을 기록합니다. 긴 문장만 낮으면 truncation과 장기 의존성 문제를 구분합니다.

## 기준선과 비교

TF-IDF+선형 모델, 평균 임베딩, SimpleRNN을 같은 test에서 비교합니다. RNN이 순서를 사용한다는 설명만으로 채택하지 않고 실제 개선량과 지연을 측정합니다.

## 대표 오류

- “안 나쁘다”처럼 이중 부정
- 앞부분의 핵심 주제를 마지막 상태가 잊음
- 긴 문장의 결론이 최대 길이 밖에서 잘림
- padding mask 누락
- 양방향 모델로 미래 정보가 누수되는 실시간 과제

## 실험 보고

모델, 파라미터 수, 전체·길이별 F1, P95, 최대 길이, 잘린 문장 비율과 실제 오분류를 한 표에 정리합니다.
