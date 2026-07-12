# 03. 코사인 유사도와 검색

코사인 유사도는 두 벡터의 방향이 얼마나 비슷한지 측정합니다. 값이 1에 가까울수록 방향이 유사합니다.

```python
from sklearn.metrics.pairwise import cosine_similarity

query_vector = vectorizer.transform(["배송이 늦어요"])
scores = cosine_similarity(query_vector, document_matrix).ravel()
best_indices = scores.argsort()[::-1][:3]
```

## 검색 결과에 포함할 정보

- 문서 ID
- 원문 또는 제목
- 유사도 점수
- 순위
- 사용한 벡터라이저 설정과 버전

## 0점과 동점

질의의 단어가 어휘에 하나도 없으면 질의 벡터가 0이 되고 모든 점수가 0일 수 있습니다. 이때 첫 문서를 정답처럼 반환하지 말고 “검색 가능한 단어가 없습니다”라는 상태를 처리합니다.

동점은 문서 ID 등 안정적인 보조 기준으로 정렬해 재현성을 확보합니다.

## TF-IDF 검색의 한계

`반품`과 `환불`처럼 의미는 비슷하지만 표면 단어가 다르면 유사도가 낮을 수 있습니다. 이는 Chapter 5의 임베딩이 필요한 이유입니다. 그럼에도 TF-IDF는 빠르고 설명 가능하며 도메인 단어가 명확한 검색에서 좋은 기준선입니다.

> 다음: [평가와 실무 주의사항](04_Evaluation.md)

## 코사인 공식과 손계산

\[
cos(A,B)=\frac{A\cdot B}{\|A\|\|B\|}
\]

`A=[1,2]`, `B=[2,1]`이면 내적은 4, 두 벡터 길이는 각각 `√5`이므로 cosine은 `4/5=0.8`입니다.

## Top-k 검색 함수

```python
import numpy as np

def search(query, vectorizer, document_matrix, documents, k=3):
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, document_matrix).ravel()
    if query_vector.nnz == 0:
        return []
    indices = np.argsort(scores)[::-1][:k]
    return [(documents[i], float(scores[i])) for i in indices]
```

0 벡터를 별도로 처리하지 않으면 관련 없는 첫 문서를 결과처럼 보여줄 수 있습니다.

## 임계값

Top-1을 무조건 반환하기보다 validation 질문에서 최소 점수를 정할 수 있습니다. 점수가 낮으면 “관련 문서를 찾지 못했습니다”를 반환합니다. 점수는 정답 확률이 아니므로 업무 데이터로 임계값을 정합니다.

## 중복 결과

거의 같은 문서가 top-k를 채우면 사용자에게 다양한 정보를 주지 못합니다. 문서 중복 제거, 문서 그룹별 하나만 선택, MMR 같은 다양성 검색을 검토합니다.

## 검색 로그

질문, 문서 ID, rank, score, vectorizer 버전과 사용자 선택 여부를 기록합니다. 개인정보가 포함된 질문은 마스킹과 보존 기간을 적용합니다.
