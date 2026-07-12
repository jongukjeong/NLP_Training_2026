# RAG 평가와 운영

단계를 나눠 평가합니다.

- ingestion: 누락·깨진 text·metadata
- retrieval: Hit@k, MRR, nDCG
- generation: 근거 충실성, 정답성, citation 정확성
- system: latency, 비용, 실패율, 최신성

검색 실패를 generation prompt로 숨기지 않습니다. 평가셋은 질문, 관련 chunk/document ID, 기대 핵심 답과 난이도를 포함합니다.

Prompt injection이 문서에 포함될 수 있으므로 검색 문서는 data이지 system instruction이 아님을 명시합니다. access control은 검색 전 단계에 적용하고 사용자가 볼 수 없는 chunk가 context에 들어가지 않게 합니다.
