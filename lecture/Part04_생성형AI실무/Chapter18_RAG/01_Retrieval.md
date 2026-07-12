# 18.1 Embedding · 18.2 Vector Database · 18.3 Retrieval

RAG는 질문과 관련된 근거를 검색해 생성 모델 입력에 제공하는 구조입니다.

```text
문서 수집 → parsing → chunking → embedding/index
질문 → query 표현 → top-k retrieval → context 구성
```

Vector DB는 vector와 문서 ID·metadata를 저장하고 유사도 검색과 filter를 제공합니다. 제품 선택 전 데이터 규모, update, filter, backup, tenancy, latency와 운영 복잡도를 평가합니다.

Chunk 크기와 overlap은 retrieval recall과 context 비용에 영향을 줍니다. page, section, source URI와 문서 version을 metadata로 보존해야 출처를 표시하고 삭제·갱신할 수 있습니다.
