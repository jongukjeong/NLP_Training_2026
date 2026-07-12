# Chapter 18. Retrieval-Augmented Generation(RAG) — 통합 원고

> 이 문서는 Chapter 18. Retrieval-Augmented Generation(RAG) 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 18. Retrieval-Augmented Generation(RAG) — `README.md`
- 18.1 Embedding · 18.2 Vector Database · 18.3 Retrieval — `01_Retrieval.md`
- 18.4 Generation · 18.5 Hybrid Search — `02_Generation_and_Hybrid.md`
- RAG 평가와 운영 — `03_Evaluation.md`
- 요약과 퀴즈 — `04_Summary_and_Quiz.md`
- 실습: PDF QA 시스템 구축 — `05_Practice.md`

---

<!-- SOURCE: README.md -->

# Chapter 18. Retrieval-Augmented Generation(RAG)

# Chapter 18. Retrieval-Augmented Generation(RAG)

1. [Embedding·Vector DB·Retrieval](01_Retrieval.md)
2. [Generation과 Hybrid Search](02_Generation_and_Hybrid.md)
3. [평가와 운영](03_Evaluation.md)
4. [요약과 퀴즈](04_Summary_and_Quiz.md)
5. [실습: PDF QA 시스템](05_Practice.md)


---

<!-- SOURCE: 01_Retrieval.md -->

# 18.1 Embedding · 18.2 Vector Database · 18.3 Retrieval

# 18.1 Embedding · 18.2 Vector Database · 18.3 Retrieval

RAG는 질문과 관련된 근거를 검색해 생성 모델 입력에 제공하는 구조입니다.

```text
문서 수집 → parsing → chunking → embedding/index
질문 → query 표현 → top-k retrieval → context 구성
```

Vector DB는 vector와 문서 ID·metadata를 저장하고 유사도 검색과 filter를 제공합니다. 제품 선택 전 데이터 규모, update, filter, backup, tenancy, latency와 운영 복잡도를 평가합니다.

Chunk 크기와 overlap은 retrieval recall과 context 비용에 영향을 줍니다. page, section, source URI와 문서 version을 metadata로 보존해야 출처를 표시하고 삭제·갱신할 수 있습니다.


---

<!-- SOURCE: 02_Generation_and_Hybrid.md -->

# 18.4 Generation · 18.5 Hybrid Search

# 18.4 Generation · 18.5 Hybrid Search

Generator prompt에는 질문, 검색 context, 답변 규칙과 citation 형식을 분리합니다. 근거가 부족하면 모른다고 답하도록 하고 검색되지 않은 사실을 추가하지 않도록 제한합니다.

Hybrid Search는 lexical(BM25/TF-IDF)과 vector 검색을 결합합니다. 고유명사·코드·정확한 용어에는 lexical, 동의어·의미 유사성에는 vector가 강할 수 있습니다.

결합 방법:

- score normalization 뒤 가중합
- Reciprocal Rank Fusion
- 후보 통합 후 reranker

점수 scale이 다른 검색기를 원시 점수로 바로 더하지 않습니다.


---

<!-- SOURCE: 03_Evaluation.md -->

# RAG 평가와 운영

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

# 실습: PDF QA 시스템 구축

정책 원문으로 교육용 PDF를 생성하고, PDF text를 page별로 추출한 뒤 TF-IDF 검색과 출처 표시 QA를 수행합니다. API 키 없이 retrieval QA가 동작합니다.

- [안내](examples/05_pdf_qa_solution/README.md)
- [PDF 생성](examples/05_pdf_qa_solution/build_sample_pdf.py)
- [QA 코드](examples/05_pdf_qa_solution/pdf_qa.py)
- [정책 원문](examples/05_pdf_qa_solution/policy_source.txt)
- [평가셋](examples/05_pdf_qa_solution/evaluation.csv)

