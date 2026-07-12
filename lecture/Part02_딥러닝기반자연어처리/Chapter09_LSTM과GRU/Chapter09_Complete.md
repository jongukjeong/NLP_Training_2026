# Chapter 9. LSTM과 GRU — 통합 원고

> 이 문서는 Chapter 9. LSTM과 GRU 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 9. LSTM과 GRU — `README.md`
- 9.1 LSTM 구조 · 9.2~9.4 Gate — `01_LSTM_Gates.md`
- 9.5 GRU와 모델 선택 — `02_GRU_and_Selection.md`
- 감성 분석 설계 — `03_Sentiment_Analysis.md`
- 요약과 퀴즈 — `04_Summary_and_Quiz.md`
- 실습: 감성 분석 — `05_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 9. LSTM과 GRU

# Chapter 9. LSTM과 GRU

1. [LSTM 구조와 세 Gate](01_LSTM_Gates.md)
2. [GRU와 모델 선택](02_GRU_and_Selection.md)
3. [감성 분석 설계](03_Sentiment_Analysis.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: 감성 분석](05_Practice.md)


---

<!-- SOURCE: 01_LSTM_Gates.md -->

# 9.1 LSTM 구조 · 9.2~9.4 Gate

# 9.1 LSTM 구조 · 9.2~9.4 Gate

LSTM은 hidden state와 별도의 cell state를 유지해 긴 의존성 학습을 돕습니다.

- Forget Gate: 이전 cell state에서 무엇을 유지할지 결정
- Input Gate: 새 후보 정보를 얼마나 기록할지 결정
- Output Gate: cell state에서 현재 hidden state로 무엇을 노출할지 결정

Gate는 sigmoid 값 0~1로 정보 흐름을 조절하고 후보 state는 주로 tanh를 사용합니다. “기억한다”는 설명은 직관이며 실제로는 데이터에서 학습된 연속값 연산입니다.

```python
layers.Bidirectional(layers.LSTM(64, dropout=0.2))
```

전체 문장을 이용하는 감성 분류에서는 Bidirectional이 유용할 수 있지만 latency와 파라미터 수가 증가합니다.


---

<!-- SOURCE: 02_GRU_and_Selection.md -->

# 9.5 GRU와 모델 선택

# 9.5 GRU와 모델 선택

GRU는 cell state와 hidden state를 통합하고 update/reset gate를 사용합니다. LSTM보다 구조가 단순해 파라미터가 적고 빠를 수 있지만 항상 성능이 우수하거나 열등한 것은 아닙니다.

비교 기준:

- validation 성능과 반복 간 분산
- 학습·추론 시간
- 모델 크기와 메모리
- sequence 길이
- 운영 latency

동일한 split, vocabulary, embedding dimension, seed와 평가 지표를 사용해 비교합니다.

```python
rnn = layers.GRU(64)       # 또는 layers.LSTM(64)
```

모델 이름보다 데이터와 평가 설계가 중요합니다.


---

<!-- SOURCE: 03_Sentiment_Analysis.md -->

# 감성 분석 설계

# 감성 분석 설계

감성 label은 주관적일 수 있으므로 annotation 기준과 불일치 사례를 기록합니다. 부정어, 반어, 복합 감정과 도메인 표현을 오류 분석에서 별도로 확인합니다.

```text
TextVectorization → Embedding(mask_zero=True)
→ Bidirectional LSTM/GRU → Dropout → sigmoid
```

평가 시 accuracy와 함께 precision, recall, F1, confusion matrix를 봅니다. 같은 상품·사용자의 거의 동일한 리뷰가 train/test에 나뉘지 않도록 중복 그룹을 고려합니다.

작은 데이터의 높은 점수는 일반화를 의미하지 않습니다. 실제 배포 전 시간·도메인 기준 holdout이 필요합니다.


---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 요약과 퀴즈

# 요약과 퀴즈

1. LSTM이 hidden state 외에 유지하는 state는? **cell state**
2. Forget Gate의 역할은? **이전 cell 정보 유지량 결정**
3. Input Gate의 역할은? **새 정보 기록량 결정**
4. Output Gate의 역할은? **현재 hidden state 노출량 결정**
5. GRU의 대표 장점은? **구조와 파라미터가 상대적으로 단순함**
6. LSTM과 GRU 비교 시 고정할 조건은? **split, 전처리, 차원, seed, 지표 등**
7. 반어가 감성 분석에서 어려운 이유는? **표면 단어와 실제 감정 방향이 다를 수 있음**


---

<!-- SOURCE: 05_Practice.md -->

# 실습: 감성 분석

# 실습: 감성 분석

같은 데이터와 설정에서 LSTM과 GRU를 학습하고 테스트 지표를 비교합니다.

- [안내](examples/05_sentiment_solution/README.md)
- [완성 코드](examples/05_sentiment_solution/sentiment_compare.py)
- [데이터셋](examples/05_sentiment_solution/reviews.csv)

