# 02. TF-IDF와 n-gram

## TF-IDF

TF-IDF는 한 문서에서 자주 등장하지만 전체 문서에서는 드문 단어에 높은 가중치를 줍니다.

```text
TF-IDF = 문서 내 빈도(TF) × 역문서 빈도(IDF)
```

모든 문서에 등장하는 단어보다 특정 문서를 구분하는 단어를 강조합니다.

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    min_df=1,
    sublinear_tf=True,
    norm="l2",
)
matrix = vectorizer.fit_transform(documents)
```

## n-gram

- unigram: 단어 하나 (`환불`)
- bigram: 연속 단어 둘 (`환불 요청`)
- trigram: 연속 단어 셋

bigram은 `배송 지연`, `환불 불가`처럼 일부 순서를 보존하지만 특징 수가 증가하고 드문 조합이 많아집니다.

## 문자 n-gram

띄어쓰기 변이가 큰 데이터에서는 문자 n-gram이 유용할 수 있습니다.

```python
TfidfVectorizer(analyzer="char", ngram_range=(2, 5), min_df=2)
```

오탈자와 띄어쓰기 변화에 강하지만 특징 의미를 해석하기 어렵고 행렬이 커질 수 있습니다.

## fit과 transform 분리

```python
train_matrix = vectorizer.fit_transform(train_texts)
test_matrix = vectorizer.transform(test_texts)
```

평가 데이터까지 `fit_transform()`하면 평가 데이터의 어휘와 문서 빈도가 학습에 반영되어 데이터 누수가 발생합니다.

> 다음: [코사인 유사도와 검색](03_Similarity_and_Search.md)
