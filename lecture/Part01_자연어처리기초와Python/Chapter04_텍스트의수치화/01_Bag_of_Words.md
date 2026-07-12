# 01. 수치화의 목적과 Bag of Words

## 문서를 벡터로 바꾸기

Bag of Words(BoW)는 문서에 어떤 단어가 몇 번 등장했는지를 벡터로 표현합니다.

```text
문서 A: 배송 빠름
문서 B: 배송 지연
어휘: [배송, 빠름, 지연]
A:     [1,   1,   0]
B:     [1,   0,   1]
```

단순하고 설명하기 쉬우며 분류·검색의 강력한 기준선입니다. 다만 단어 순서와 문맥을 대부분 잃습니다.

## CountVectorizer

```python
from sklearn.feature_extraction.text import CountVectorizer

documents = ["배송 빠름", "배송 지연", "환불 요청"]
vectorizer = CountVectorizer(token_pattern=r"(?u)\b\w+\b")
matrix = vectorizer.fit_transform(documents)

print(vectorizer.get_feature_names_out())
print(matrix.toarray())
```

한국어 전처리 결과가 공백 토큰으로 준비됐다면 `token_pattern`을 명시해 한 글자 토큰 처리 정책을 통제합니다.

## 희소 행렬

실제 어휘가 50,000개여도 한 문서에 등장하는 단어는 일부입니다. scikit-learn은 0을 모두 저장하지 않는 희소 행렬을 사용합니다. 큰 데이터에서 `toarray()`로 전체를 밀집 행렬로 바꾸면 메모리가 급증하므로 작은 확인용으로만 사용합니다.

## 어휘 제어

```python
CountVectorizer(
    min_df=2,
    max_df=0.95,
    max_features=20_000,
)
```

- `min_df`: 너무 드문 항목 제거
- `max_df`: 거의 모든 문서에 나오는 항목 제거
- `max_features`: 최대 특징 수 제한

이 값은 데이터 크기와 평가 결과를 기준으로 정하며 평가 데이터에 맞춰 조정하지 않습니다.

> 다음: [TF-IDF와 n-gram](02_TFIDF_and_Ngrams.md)
