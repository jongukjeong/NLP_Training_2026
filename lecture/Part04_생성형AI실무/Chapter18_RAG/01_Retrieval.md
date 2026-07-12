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
