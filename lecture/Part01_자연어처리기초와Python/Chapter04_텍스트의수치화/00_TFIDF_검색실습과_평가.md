# Chapter 4 TF-IDF 검색 실습과 평가

## 작은 검색기를 만드는 전체 과정

```text
문서 읽기 → 전처리 → TF-IDF 학습 → 문서 행렬
질문 전처리 → 같은 TF-IDF 변환 → cosine → 순위
```

질문에 별도 vocabulary를 만들지 않는 것이 핵심입니다.

## 최소 코드

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = [
    "배송은 영업일 기준 3일 걸립니다",
    "환불은 결제 취소 후 처리됩니다",
    "비밀번호는 계정 설정에서 변경합니다",
]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
doc_matrix = vectorizer.fit_transform(docs)

query = "배송 기간은 며칠인가요"
query_vector = vectorizer.transform([query])
scores = cosine_similarity(query_vector, doc_matrix)[0]
print(scores)
```

결과는 문서 3개에 대한 유사도 배열입니다. 가장 큰 값의 인덱스가 첫 검색 결과입니다.

## 행렬 shape

문서가 3개이고 학습된 특징이 25개면 `doc_matrix.shape==(3,25)`, 질문은 `(1,25)`입니다. 같은 열 25개를 사용하므로 cosine을 계산할 수 있습니다.

## Vocabulary 확인

```python
feature_names = vectorizer.get_feature_names_out()
print(feature_names[:20])
```

예상한 제품명과 bigram이 있는지 확인합니다. 전처리 때문에 중요한 코드가 사라졌다면 검색 전에 수정합니다.

## Top-k 반환

```python
import numpy as np

top_k = 2
indices = np.argsort(scores)[::-1][:top_k]
for rank, index in enumerate(indices, 1):
    print(rank, float(scores[index]), docs[index])
```

점수는 모델과 데이터에 따라 달라 절대적인 정답 확률로 해석하지 않습니다.

## 평가 데이터

| 질문 | 정답 문서 ID |
|---|---|
| 배송에 며칠 걸려요? | d001 |
| 암호를 바꾸고 싶어요 | d003 |
| 결제 취소 절차는? | d002 |

표현이 문서와 완전히 같은 질문만 사용하면 실제 검색 난이도를 과소평가합니다.

## Hit@k

10개 질문 중 1위에 정답이 7개면 Hit@1=0.7입니다. top-3에 9개면 Hit@3=0.9입니다. 서비스가 사용자에게 결과 세 개를 보여준다면 Hit@3이 중요할 수 있습니다.

## MRR

첫 정답 순위가 1, 2, 2, 4라면:

\[
MRR=(1+0.5+0.5+0.25)/4=0.5625
\]

정답이 앞에 나올수록 높은 점수를 받습니다.

## N-gram 비교

| 설정 | 장점 | 비용 |
|---|---|---|
| `(1,1)` | 단순, 작은 행렬 | 구 표현 손실 |
| `(1,2)` | `결제 취소` 보존 | 특징 수 증가 |
| `(1,3)` | 긴 구 보존 | 희소성과 메모리 증가 |

동일 평가셋에서 Hit와 행렬 크기, 검색시간을 기록합니다.

## min_df와 max_df

`min_df`는 너무 드문 특징, `max_df`는 지나치게 흔한 특징을 제한합니다. 제품 코드는 드물지만 중요하므로 높은 `min_df`가 검색을 망칠 수 있습니다.

## 오류 분석

- 동의어: “암호”와 “비밀번호”가 다른 단어
- 고유명사: 제품 코드가 정제됨
- 짧은 질문: 단서가 한 단어뿐
- 긴 문서: 관련 부분이 다른 내용에 묻힘
- 중복 문서: 거의 같은 결과가 상위를 차지

TF-IDF의 동의어 한계는 임베딩 검색 또는 동의어 사전과 비교할 수 있습니다.

## 모델 저장

```python
import joblib
joblib.dump(vectorizer, "tfidf.joblib")
```

서비스에서 다시 fit하지 않고 저장한 vectorizer를 불러옵니다. 학습 문서 버전과 vectorizer 버전을 함께 관리합니다.

## 완료 기준

1. 문서 ID와 원문 보존
2. 같은 전처리와 vectorizer 재사용
3. Hit@1·Hit@3·MRR 계산
4. 오류 질문 원문 분석
5. 행렬 shape와 메모리 확인
6. 저장 후 재로딩 검색 결과 확인
