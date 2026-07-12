# Chapter 18 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 18. Retrieval-Augmented Generation(RAG)

1. [Embedding·Vector DB·Retrieval](01_Retrieval.md)
2. [Generation과 Hybrid Search](02_Generation_and_Hybrid.md)
3. [평가와 운영](03_Evaluation.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: PDF QA 시스템](05_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 18 원리·수학·실습 가이드

## 1. RAG의 데이터 흐름

`문서 → 청크 → 임베딩/색인 → 질문 검색 → 상위 문맥 → 근거 기반 생성 → 인용`

LLM 가중치를 다시 학습하지 않고 최신·사내 문서를 조회한다. 검색이 실패하면 생성 모델은 올바른 답을 만들 근거가 없으므로 retrieval과 generation을 분리 평가한다.

## 2. Dense와 Sparse 검색

코사인 유사도는 벡터 방향의 유사성을 측정한다.

\[
cos(q,d)=\frac{q\cdot d}{\|q\|\|d\|}
\]

`q=[1,0]`, `d=[0.8,0.6]`이면 norm이 각각 1이므로 유사도 0.8이다. Dense 검색은 의미가 비슷한 표현에 강하고, BM25 같은 Sparse 검색은 제품 코드·고유명사·정확한 키워드에 강하다.

Hybrid Search는 두 순위를 결합한다. Reciprocal Rank Fusion의 한 형태는 다음과 같다.

\[
RRF(d)=\sum_r\frac1{k+rank_r(d)}
\]

## 3. Chunk와 생성

청크가 너무 작으면 문맥이 끊기고 너무 크면 관련 없는 내용과 비용이 늘어난다. 제목·페이지·문서 ID를 metadata로 보존하고, 질문에 충분한 최소 청크 크기와 overlap을 평가셋으로 정한다.

생성 프롬프트에는 “제공된 문맥만 사용, 근거 없으면 모른다고 답함, 문서/페이지 인용” 규칙을 둔다. 인용 문자열만 존재하는지 아니라 실제 주장과 근거가 일치하는지 확인한다.

## 4. 검색 평가

\[
Recall@k=\frac{k개\ 안에\ 찾은\ 관련문서}{전체\ 관련문서}
\]

\[
MRR=\frac1N\sum_i\frac1{rank_i}
\]

관련 문서가 1위면 reciprocal rank 1, 2위면 0.5다. 검색 실패, 근거는 찾았지만 답 생성 실패, 인용 오류를 별도 분류한다.

1. 코사인 유사도 1은 무엇을 뜻하는가?
2. 제품 번호 검색에서 sparse가 유리할 수 있는 이유는?
3. 답변 품질 전에 Recall@k를 확인해야 하는 이유는?

---

<!-- SOURCE: 01_Retrieval.md -->

# 18.1 Embedding · 18.2 Vector Database · 18.3 Retrieval

RAG는 질문과 관련된 근거를 검색해 생성 모델 입력에 제공하는 구조입니다.

```text
문서 수집 → parsing → chunking → embedding/index
질문 → query 표현 → top-k retrieval → context 구성
```

Vector DB는 vector와 문서 ID·metadata를 저장하고 유사도 검색과 filter를 제공합니다. 제품 선택 전 데이터 규모, update, filter, backup, tenancy, latency와 운영 복잡도를 평가합니다.

Chunk 크기와 overlap은 retrieval recall과 context 비용에 영향을 줍니다. page, section, source URI와 문서 version을 metadata로 보존해야 출처를 표시하고 삭제·갱신할 수 있습니다.

## RAG를 도서관으로 이해하기

LLM은 답변 작성자, Retriever는 사서, Vector Database는 책 위치를 찾는 색인입니다. 사서가 관련 문서를 못 찾으면 작성자가 근거 있는 답을 만들기 어렵습니다. 따라서 검색과 생성을 나누어 평가합니다.

## Embedding과 코사인 유사도

문장 의미를 벡터 방향으로 표현하고 두 방향이 얼마나 비슷한지 계산합니다.

\[
cos(q,d)=\frac{q\cdot d}{\|q\|\|d\|}
\]

`q=[1,0]`, `d=[0.8,0.6]`이면 내적 0.8, 두 벡터 norm이 모두 1이므로 유사도는 0.8입니다. 값이 클수록 보통 의미가 가깝지만 모델별 점수 범위와 임계값은 평가 데이터로 정합니다.

## Chunk 크기의 trade-off

100자처럼 너무 작으면 정의와 조건이 갈라지고, 문서 전체처럼 너무 크면 관련 없는 정보와 토큰 비용이 늘어납니다. 제목과 문단 경계를 우선하고 overlap으로 경계 문맥을 일부 보존합니다.

## Sparse와 Dense

BM25 같은 sparse 검색은 정확한 단어·제품 코드에 강하고 dense 검색은 다른 표현의 의미 유사성에 강합니다. “A-104 오류”와 “로그인이 계속 실패”가 한 시스템에 함께 들어오면 hybrid search가 유리할 수 있습니다.

## Recall@k

\[
Recall@k=\frac{상위k개에서찾은관련문서수}{전체관련문서수}
\]

관련 문서 2개 중 top-3에서 1개를 찾으면 Recall@3은 0.5입니다. 정답 문서가 검색되지 않은 질문은 생성 프롬프트만 바꿔도 해결되지 않습니다.

## 검색 디버깅

질문, 기대 문서 ID, 검색 문서와 점수, rank, chunk 원문을 저장합니다. 고유명사 실패, 너무 작은 청크, metadata filter 오류, embedding 언어 부적합을 구분합니다.

---

<!-- SOURCE: 02_Generation_and_Hybrid.md -->

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

---

<!-- SOURCE: 03_Evaluation.md -->

# RAG 평가와 운영

단계를 나눠 평가합니다.

- ingestion: 누락·깨진 text·metadata
- retrieval: Hit@k, MRR, nDCG
- generation: 근거 충실성, 정답성, citation 정확성
- system: latency, 비용, 실패율, 최신성

검색 실패를 generation prompt로 숨기지 않습니다. 평가셋은 질문, 관련 chunk/document ID, 기대 핵심 답과 난이도를 포함합니다.

Prompt injection이 문서에 포함될 수 있으므로 검색 문서는 data이지 system instruction이 아님을 명시합니다. access control은 검색 전 단계에 적용하고 사용자가 볼 수 없는 chunk가 context에 들어가지 않게 합니다.

---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 요약과 퀴즈

1. RAG의 두 핵심 단계는? **Retrieval과 Generation**
2. chunk metadata가 필요한 이유는? **출처·갱신·삭제·권한 관리**
3. 고유한 제품 코드 검색에 강한 방식은? **lexical search**
4. 의미적 동의어 검색에 강한 방식은? **vector search**
5. 검색기 원시 점수를 바로 더해도 되나요? **아니요**
6. retrieval과 generation 평가는 분리해야 하나요? **예**
7. 문서 속 지시를 system instruction으로 따라야 하나요? **아니요**

---

<!-- SOURCE: 05_Practice.md -->

# 실습: PDF QA 시스템 구축

정책 원문으로 교육용 PDF를 생성하고, PDF text를 page별로 추출한 뒤 TF-IDF 검색과 출처 표시 QA를 수행합니다. API 키 없이 retrieval QA가 동작합니다.

- [안내](examples/05_pdf_qa_solution/README.md)
- [PDF 생성](examples/05_pdf_qa_solution/build_sample_pdf.py)
- [QA 코드](examples/05_pdf_qa_solution/pdf_qa.py)
- [정책 원문](examples/05_pdf_qa_solution/policy_source.txt)
- [평가셋](examples/05_pdf_qa_solution/evaluation.csv)

