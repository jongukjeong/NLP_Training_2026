# RAG 평가와 운영

단계를 나눠 평가합니다.

- ingestion: 누락·깨진 text·metadata
- retrieval: Hit@k, MRR, nDCG
- generation: 근거 충실성, 정답성, citation 정확성
- system: latency, 비용, 실패율, 최신성

검색 실패를 generation prompt로 숨기지 않습니다. 평가셋은 질문, 관련 chunk/document ID, 기대 핵심 답과 난이도를 포함합니다.

Prompt injection이 문서에 포함될 수 있으므로 검색 문서는 data이지 system instruction이 아님을 명시합니다. access control은 검색 전 단계에 적용하고 사용자가 볼 수 없는 chunk가 context에 들어가지 않게 합니다.

## 검색과 생성을 분리 평가하기

답변이 틀렸을 때 정답 문서를 검색했는지 먼저 확인합니다. 검색 실패라면 생성 Prompt만 고쳐도 해결되지 않습니다.

## Retrieval 지표

정답 문서가 top-k에 있는지 Hit@k, 첫 정답 순위를 MRR로 계산합니다. 여러 관련 문서가 있으면 Recall@k도 사용합니다.

## Generation 지표

- Answer correctness: 질문에 맞는 답인가?
- Groundedness: 문맥에서 확인되는가?
- Citation correctness: 표시한 출처가 실제 근거인가?
- Abstention: 근거 없을 때 답변을 보류하는가?

## 평가 레코드

```text
question_id,expected_doc,retrieved_docs,first_rank,answer,citations,retrieval_pass,generation_pass,error_type
```

## RAG 오류 분류

검색 실패, 청크 경계, rerank 실패, 생성 오류, 인용 오류, 권한 오류를 구분합니다.

## 정답 없는 질문

정답 문서가 없는 질문도 포함합니다. 이때 아무 문서나 인용해 답하면 실패이며 “근거를 찾지 못했다”가 올바른 결과일 수 있습니다.

## 변경 비교

Chunk, embedding, top-k, hybrid, reranker를 한 번에 하나씩 바꾸고 Hit@k·MRR·근거성·P95·비용을 기록합니다.
