# 18.4 Generation · 18.5 Hybrid Search

Generator prompt에는 질문, 검색 context, 답변 규칙과 citation 형식을 분리합니다. 근거가 부족하면 모른다고 답하도록 하고 검색되지 않은 사실을 추가하지 않도록 제한합니다.

Hybrid Search는 lexical(BM25/TF-IDF)과 vector 검색을 결합합니다. 고유명사·코드·정확한 용어에는 lexical, 동의어·의미 유사성에는 vector가 강할 수 있습니다.

결합 방법:

- score normalization 뒤 가중합
- Reciprocal Rank Fusion
- 후보 통합 후 reranker

점수 scale이 다른 검색기를 원시 점수로 바로 더하지 않습니다.

## 문서 로딩 단계가 중요한 이유

PDF, CSV, 웹 문서는 구조가 다릅니다. Loader는 텍스트만 가져오는 것이 아니라 페이지, 제목, 파일명 같은 metadata를 함께 보존해야 합니다. 답변 인용과 접근권한 필터링은 이 정보에 의존합니다.

```text
page_content: 실제 검색할 텍스트
metadata: source, page, title, updated_at, access_level
```

스캔 PDF는 OCR이 필요하고, 표가 많은 PDF는 읽기 순서가 깨질 수 있습니다. 로딩 후 임의 페이지를 사람이 확인하는 품질 검사가 필요합니다.

## Splitter 선택

Character splitter는 단순 길이 기준, recursive splitter는 문단·문장·공백 같은 경계를 순서대로 시도합니다. 토큰 기준 splitter는 실제 모델 문맥 예산과 맞추기 좋습니다.

청크 크기와 overlap은 하나의 정답이 아닙니다. 300/50, 600/100, 1,000/150처럼 후보를 정하고 Recall@k와 답변 근거성을 비교합니다.

## Vector Store의 역할

Vector Store는 임베딩과 metadata를 저장하고 가까운 벡터를 검색합니다. Chroma, FAISS, 관리형 서비스는 영속성, 분산 확장, 필터링, 운영 편의가 다릅니다. 작은 로컬 실습과 다중 사용자 운영의 선택 기준을 구분합니다.

## Metadata filtering

검색 전에 부서, 문서 버전, 공개 범위로 후보를 줄일 수 있습니다. 필터는 정확도를 높일 수 있지만 잘못된 metadata나 과도한 조건은 정답 문서를 제외합니다. 권한 필터는 프롬프트 지시가 아니라 검색 계층에서 강제합니다.

## MMR의 직관

유사도 상위 결과가 거의 같은 문단으로 반복될 때 MMR은 질문과의 관련성뿐 아니라 이미 선택한 문서와의 중복도 고려합니다.

\[
MMR(d)=\lambda sim(q,d)-(1-\lambda)\max_{s\in S}sim(d,s)
\]

`λ`가 1에 가까우면 관련성을, 0에 가까우면 다양성을 더 중시합니다. 정책의 여러 조건을 골고루 찾을 때 유용하지만 정확한 한 문단만 필요한 질문에는 이득이 작을 수 있습니다.

## Reranker

1차 retriever가 후보 20개를 빠르게 찾고, Cross-Encoder reranker가 질문과 문서를 함께 읽어 상위 5개를 다시 정렬합니다. 품질은 좋아질 수 있지만 문서마다 추가 추론이 필요해 지연과 비용이 증가합니다.

## Query enhancement

질문 재작성, 다중 검색어 생성, RAG-Fusion은 표현이 부족한 질문의 Recall을 높일 수 있습니다. 반대로 원래 의미가 바뀔 위험이 있으므로 원 질문과 생성 쿼리, 검색 결과를 로그에 남깁니다.
