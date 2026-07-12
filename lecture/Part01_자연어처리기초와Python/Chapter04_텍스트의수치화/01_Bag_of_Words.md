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

## Binary와 Count 표현

Binary 방식은 단어가 한 번이라도 나오면 1, Count 방식은 실제 등장 횟수를 기록합니다. 스팸 문구처럼 반복 횟수가 중요하면 Count가 유용하고, 긴 문서가 단순히 더 큰 값을 갖는 문제를 줄이려면 Binary를 비교할 수 있습니다.

```python
binary_vectorizer = CountVectorizer(binary=True)
count_vectorizer = CountVectorizer(binary=False)
```

문장 `배송 배송 지연`은 어휘 `[배송, 지연]`에서 Binary `[1,1]`, Count `[2,1]`입니다.

## 행렬 shape 해석

문서 1,000개와 어휘 5,000개가 있으면 행렬 shape는 `(1000,5000)`입니다. 행은 문서, 열은 단어입니다. 새 문서를 `transform()`하면 `(새 문서 수,5000)`으로 같은 열을 사용합니다.

## 메모리 확인

```python
print(matrix.shape)
print("0이 아닌 원소:", matrix.nnz)
sparsity = 1 - matrix.nnz / (matrix.shape[0] * matrix.shape[1])
print("희소도:", sparsity)
```

희소도가 0.99라면 원소의 99%가 0입니다. 이 때문에 희소 행렬을 사용합니다.

## 어휘 누수와 미등록 단어

평가 문서까지 포함해 `fit()`하면 미래 어휘를 미리 알게 됩니다. Train에서 fit하고 validation/test에는 transform만 적용합니다. 학습 어휘에 없는 새 단어는 해당 열이 없으므로 벡터에 반영되지 않습니다.

## BoW가 적합한 경우

- 카테고리별 핵심 단어가 뚜렷한 문서 분류
- 제품 코드와 정확한 용어 중심 검색
- 빠르고 설명 가능한 기준선

번역·문장 생성처럼 순서가 핵심인 과제에는 적합하지 않습니다.
