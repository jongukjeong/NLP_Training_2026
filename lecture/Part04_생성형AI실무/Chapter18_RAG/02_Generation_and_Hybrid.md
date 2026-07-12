# 18.4 Generation · 18.5 Hybrid Search

Generator prompt에는 질문, 검색 context, 답변 규칙과 citation 형식을 분리합니다. 근거가 부족하면 모른다고 답하도록 하고 검색되지 않은 사실을 추가하지 않도록 제한합니다.

Hybrid Search는 lexical(BM25/TF-IDF)과 vector 검색을 결합합니다. 고유명사·코드·정확한 용어에는 lexical, 동의어·의미 유사성에는 vector가 강할 수 있습니다.

결합 방법:

- score normalization 뒤 가중합
- Reciprocal Rank Fusion
- 후보 통합 후 reranker

점수 scale이 다른 검색기를 원시 점수로 바로 더하지 않습니다.
