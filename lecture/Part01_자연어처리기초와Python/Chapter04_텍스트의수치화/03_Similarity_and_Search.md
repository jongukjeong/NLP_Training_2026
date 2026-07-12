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
