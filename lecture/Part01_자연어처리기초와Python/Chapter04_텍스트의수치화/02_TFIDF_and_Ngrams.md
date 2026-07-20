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

## TF와 IDF 공식

$$
TF(t,d)=\frac{count(t,d)}{문서d의전체단어수}
$$

$$
IDF(t)=\log\frac{전체문서수}{단어t가등장한문서수}
$$

100개 문서 중 5개에만 등장한 단어의 IDF는 `log(20)≈2.996`입니다. 100개 모두에 등장하면 `log(1)=0`입니다. 라이브러리는 smoothing 때문에 손계산과 조금 다를 수 있습니다.

## sublinear_tf

`sublinear_tf=True`는 등장 횟수를 그대로 쓰지 않고 `1+log(count)`로 완화합니다. 한 문서에서 어떤 단어가 20번 나왔다고 1번 나온 단어보다 정확히 20배 중요하다고 보기 어려울 때 유용합니다.

## L2 정규화

`norm="l2"`는 각 문서 벡터의 길이를 1로 맞춥니다. 긴 문서가 단어 수 때문에 무조건 큰 값을 갖는 현상을 줄이고 cosine 계산을 편리하게 합니다.

## 단어와 문자 n-gram 비교

| 데이터 | 권장 후보 | 이유 |
|---|---|---|
| 정제된 뉴스 | word `(1,2)` | 단어 의미와 구 보존 |
| 오타 많은 문의 | char `(2,5)` | 철자·띄어쓰기 변화 대응 |
| 제품 코드 | word+char 비교 | 정확한 문자열 보존 |

특징 수, Hit@k, 메모리와 검색시간을 같은 평가셋에서 비교합니다.

## 지나친 n-gram

긴 n-gram은 학습 문장 전체를 외우는 특징이 될 수 있습니다. Train 성능은 높지만 새 표현에서 실패할 수 있으므로 validation 결과와 `matrix.shape[1]`을 함께 봅니다.
