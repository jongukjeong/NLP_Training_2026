# 20.3 모델 개발

기준선은 문자 n-gram TF-IDF와 cosine similarity입니다. 한국어 띄어쓰기와 일부 표현 변화에 견고하고 API 없이 재현할 수 있습니다.

```text
query → vectorize → top-k documents → threshold
→ evidence + source → optional LLM generation
```

향후 확장:

- embedding retriever
- lexical+vector hybrid와 RRF
- reranker
- metadata filter와 접근권한
- query rewriting

각 변경은 같은 평가셋에서 retrieval metric과 latency를 비교합니다. generation 개선으로 retrieval 실패를 숨기지 않습니다.
