# Chapter 18 통합 강의 원고

---

<!-- SOURCE: README.md -->

# Chapter 18. Retrieval-Augmented Generation(RAG)

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **검색 증강 생성(Retrieval-Augmented Generation, RAG): 관련 문서를 검색한 뒤 근거로 답을 생성하는 구조**
- **청크(Chunk): 검색을 위해 나눈 문서 조각**
- **임베딩(Embedding): 의미 유사도를 비교할 수 있는 벡터 표현**
- **재순위화 모델(Reranker): 검색 후보의 순서를 다시 평가하는 모델**
- **평균 역순위(Mean Reciprocal Rank, MRR): 첫 정답 순위의 역수를 평균한 검색 지표**

1. [Embedding·Vector DB·Retrieval](01_Retrieval.md)
2. [Generation과 Hybrid Search](02_Generation_and_Hybrid.md)
3. [평가와 운영](03_Evaluation.md)
4. [퀴즈](04_Summary_and_Quiz.md)
5. [실습: PDF QA 시스템](05_Practice.md)

## 먼저 읽을 상세 가이드

- [비전공자용 RAG 검색 평가 워크북](00_비전공자_RAG_검색평가워크북.md): Chunk, 코사인 유사도, Recall@k, MRR과 오류 분류를 계산합니다.

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: LEARNING_PATH.md -->

# Chapter 18 비전공자 학습 경로

## 기본 도달 목표

작은 문서에서 검색 결과와 근거 문장 확인

완성형 코드를 처음부터 모두 이해하거나 다시 작성하는 것은 기본 목표가 아닙니다.

## 1. Step by Step — 강사와 함께

1. 문서 세 개를 준비한다
2. 질문과 가까운 문서를 찾는다
3. 검색된 근거를 출력한다
4. 답변이 근거에 포함되는지 확인한다

각 단계가 끝날 때 입력, 출력 또는 중간 결과를 화면에서 확인합니다. 설명할 수 없는 줄은 다음 단계로 넘어가기 전에 질문합니다.

## 2. Basic Practice — 짧은 흐름 연결

Step by Step의 네 단계를 한 흐름으로 연결합니다. 처음에는 함수 분리, 타입 힌트, 복잡한 예외 처리와 자동 보고서를 요구하지 않습니다.

완료 확인:

- 입력이 무엇인지 설명한다.
- 핵심 처리 한 단계를 찾아 수정한다.
- 출력이 예상과 다른 이유를 한 가지 찾는다.
- 실행 결과를 짧게 기록한다.

## 실행 코드 위치

- [Step by Step](examples/01_step_by_step/README.md)
- [Basic Practice](examples/02_basic_practice/README.md)
- [Practice Starter](examples/03_practice_starter/README.md)

세 자료는 외부 모델이나 API 없이 핵심 흐름을 먼저 이해하도록 구성했습니다. 실제 라이브러리와 완성형 구조는 기존 solution에서 비교합니다.

## 3. Practice·Assignment — 먼저 시도

[05_Practice.md](05_Practice.md)의 기본 요구사항을 먼저 수행합니다. 막히면 전체 solution 대신 필요한 단계의 힌트만 확인합니다.

## 4. Solution — 피드백 후 공개

[examples/05_pdf_qa_solution/README.md](examples/05_pdf_qa_solution/README.md)은 다수의 수강생이 기본 요구사항을 시도하고 공통 오류를 함께 확인한 뒤 공개합니다. 자신의 코드와 다음 항목을 비교합니다.

1. 반복되는 처리를 어떻게 묶었는가
2. 잘못된 입력을 어디에서 검사하는가
3. 결과를 어떻게 검증하고 기록하는가

## 선택 확장

- PDF loader
- chunk 실험
- hybrid 검색
- RAG 평가

선택 확장은 기본 완료 기준에 포함하지 않습니다.

---

<!-- SOURCE: 00_RAG_운영과_품질모니터링.md -->

# Chapter 18 RAG 운영과 품질 모니터링

## 문서 생명주기

추가·수정·삭제 문서가 색인에 언제 반영되는지 정의합니다. 삭제 문서가 vector store에 남으면 오래된 답이나 권한 문제가 생깁니다.

## 버전 일관성

Embedding 모델을 바꾸면 기존 문서 벡터와 새 질문 벡터의 공간이 다를 수 있습니다. 전체 재색인 또는 버전별 index를 사용합니다.

## 모니터링 지표

- 검색 결과 없음 비율
- top score 분포
- 문서별 검색 빈도
- 답변 보류율
- 인용 유효율
- 검색·생성 P95
- 문서 최신성

점수 분포 변화는 문서나 질문 분포 변화의 신호일 수 있지만 정답률을 직접 의미하지는 않습니다.

## 권한

사용자 권한을 metadata filter로 검색 전에 적용합니다. 생성 Prompt에 “기밀을 말하지 마”라고만 적는 것은 접근통제가 아닙니다.

## 캐시

같은 질문 결과를 캐시하면 비용을 줄일 수 있지만 정책 문서가 바뀌었을 때 오래된 답을 반환할 수 있습니다. 문서 버전과 TTL을 캐시 키·정책에 포함합니다.

## 품질 회귀시험

재색인, embedding, chunk, reranker 변경 때 고정 평가셋의 Hit@k·MRR·근거성을 비교합니다.

---

<!-- SOURCE: 00_RAG_처음부터_평가까지.md -->

# Chapter 18 RAG 처음부터 평가까지

## RAG를 시험 답안 작성으로 이해하기

Retriever는 참고서를 찾아 주고, LLM은 찾아온 페이지로 답안을 작성합니다. 참고서를 잘못 찾으면 글을 잘 쓰는 모델도 정답을 만들기 어렵습니다.

## 두 개의 파이프라인

```text
색인: 문서 → 로딩 → 정제 → 청크 → 임베딩 → 저장
질의: 질문 → 검색 → rerank → 문맥 구성 → 생성 → 인용
```

색인은 문서가 바뀔 때 실행하고 질의는 사용자 요청마다 실행합니다.

## Loader 검사

PDF에서 페이지 순서, 표, 머리말이 제대로 추출되는지 확인합니다. 빈 페이지와 깨진 문자 비율을 기록합니다. metadata에 source와 page를 보존해야 인용할 수 있습니다.

## Chunk 실험

같은 평가 질문으로 청크 크기 300/600/1,000토큰을 비교합니다. 작은 청크는 정확한 부분을 찾기 쉽지만 문맥이 끊길 수 있고, 큰 청크는 조건이 함께 남지만 잡음과 비용이 늘어납니다.

## 검색 결과를 눈으로 확인하기

```text
질문: 휴가 신청은 며칠 전까지?
1위: 휴가 정책 3쪽, score 0.82
2위: 근태 정책 7쪽, score 0.70
3위: 복지 안내 2쪽, score 0.61
```

정답 문서가 몇 위인지, 청크 안에 실제 답이 있는지 확인합니다. score만 보고 정답이라 하지 않습니다.

## Recall@k와 MRR

정답 문서가 top-3 안에 있으면 단일 정답 질문의 Hit@3은 성공입니다. MRR은 첫 정답 순위를 평가합니다.

\[
MRR=\frac1N\sum_i\frac1{rank_i}
\]

세 질문의 첫 정답 순위가 1, 2, 4라면 MRR은 `(1+0.5+0.25)/3≈0.583`입니다.

## Hybrid Search

Dense 검색은 의미가 비슷한 표현, sparse 검색은 정확한 단어와 제품 번호에 강합니다. 두 결과를 RRF 같은 방식으로 결합할 수 있습니다.

## 답변 Prompt

```text
제공된 문맥만 사용한다.
근거가 없으면 모른다고 답한다.
각 주장에 문서와 페이지를 표시한다.
서로 충돌하면 충돌 사실을 설명한다.
```

이 규칙이 있어도 모델이 항상 지키지는 않으므로 자동·수동 평가가 필요합니다.

## 실패 분류

1. Retrieval 실패: 정답 청크가 검색되지 않음
2. Context 실패: 정답은 있으나 잘리거나 순서가 나쁨
3. Generation 실패: 문맥에 답이 있지만 잘못 생성
4. Citation 실패: 답은 맞지만 출처가 틀림
5. Access 실패: 권한 없는 문서가 검색됨

원인을 나누지 않으면 Prompt 변경으로 검색 문제를 해결하려는 실수를 합니다.

## 운영 점검

문서 업데이트 주기, 삭제 반영, embedding 버전, 권한 metadata, 질문·검색 로그의 개인정보, 비용과 P95 지연을 관리합니다.

---

<!-- SOURCE: 00_비전공자_RAG_검색평가워크북.md -->

# Chapter 18 비전공자용 RAG 검색 평가 워크북

## RAG는 두 개의 시스템을 이어 붙인다

RAG는 관련 문서를 찾는 Retrieval과, 찾은 근거로 답을 만드는 Generation으로 나뉩니다. 답이 틀렸을 때 두 단계를 분리하지 않으면 검색을 고쳐야 하는지 프롬프트를 고쳐야 하는지 알 수 없습니다.

```text
문서 수집 → 분할 → 임베딩·색인
질문 → 검색 → 근거 선택 → 답변 생성 → 출처 표시
```

## Chunk는 검색 가능한 문서 조각이다

Chunk가 너무 크면 관련 없는 내용까지 함께 들어오고, 너무 작으면 답에 필요한 문맥이 여러 조각으로 흩어집니다. 한 가지 크기를 정답처럼 사용하지 말고 고정 질문으로 크기와 겹침을 비교합니다.

| 설정 | 장점 | 위험 |
|---|---|---|
| 작은 Chunk | 세밀한 위치 검색 | 문맥 단절 |
| 큰 Chunk | 주변 문맥 보존 | 불필요한 내용 증가 |
| Overlap | 경계 정보 보존 | 중복과 저장량 증가 |

## Embedding 유사도를 손으로 읽기

코사인 유사도는 두 벡터의 방향이 얼마나 비슷한지 측정합니다.

\[
\cos(\theta)=\frac{q\cdot d}{\lVert q\rVert\lVert d\rVert}
\]

1에 가까우면 방향이 비슷하고, 0에 가까우면 관련성이 낮습니다. 그러나 높은 점수가 사실의 정확성이나 답변 가능성을 보장하지는 않습니다.

## Sparse와 Dense 검색을 구분한다

- Sparse 검색: 실제 단어와 빈도에 강해 제품 코드·고유명사 검색에 유리
- Dense 검색: 표현이 달라도 의미가 비슷한 문서를 찾는 데 유리
- Hybrid 검색: 두 후보를 결합하고 필요하면 Reranker로 순서를 조정

검색기마다 점수 범위가 다르므로 원시 점수를 그대로 더하지 않습니다. 순위 결합이나 정규화 방법을 명시합니다.

## Recall@k 계산하기

정답 문서가 상위 (k)개 안에 포함된 질문의 비율입니다. 평가 질문 10개 중 8개에서 정답 문서가 Top-3에 있었다면 다음과 같습니다.

\[
Recall@3=\frac{8}{10}=0.8
\]

Recall이 낮으면 생성 모델이 아무리 좋아도 필요한 근거를 받지 못합니다.

## MRR은 정답이 얼마나 앞에 있는지 본다

첫 정답 순위가 각각 1, 2, 4라면 Reciprocal Rank는 (1, 1/2, 1/4)입니다.

\[
MRR=\frac{1+0.5+0.25}{3}\approx0.583
\]

정답을 포함하는 것뿐 아니라 앞쪽에 배치하는 능력을 측정합니다.

## 생성 답변 평가를 별도로 기록한다

| 항목 | 질문 |
|---|---|
| 근거성 | 답의 각 주장이 검색 문서에 있는가 |
| 완전성 | 질문의 핵심 항목을 빠뜨리지 않았는가 |
| 인용 | 출처 ID와 실제 Chunk가 일치하는가 |
| 거절 | 근거가 없을 때 모른다고 답하는가 |

## 오류를 네 종류로 분류한다

1. 수집 오류: 필요한 문서가 색인에 없음
2. 분할 오류: 답에 필요한 내용이 부적절하게 잘림
3. 검색 오류: 문서는 있지만 Top-k에 들어오지 않음
4. 생성 오류: 올바른 근거를 받았지만 답을 왜곡함

## 운영에서는 문서 생명주기를 관리한다

문서 ID, 버전, 갱신일, 접근 권한과 삭제 상태를 Metadata로 보존합니다. 사용자가 볼 수 없는 문서는 검색 결과에도 포함되면 안 됩니다. Prompt Injection 문구가 포함된 문서 역시 신뢰할 수 없는 입력으로 처리합니다.

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

---

<!-- SOURCE: 04_Summary_and_Quiz.md -->

# 퀴즈
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

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

정책 원문으로 교육용 PDF를 생성하고, PDF text를 page별로 추출한 뒤 TF-IDF 검색과 출처 표시 QA를 수행합니다. API 키 없이 retrieval QA가 동작합니다.

- [안내](examples/05_pdf_qa_solution/README.md)
- [PDF 생성](examples/05_pdf_qa_solution/build_sample_pdf.py)
- [QA 코드](examples/05_pdf_qa_solution/pdf_qa.py)
- [정책 원문](examples/05_pdf_qa_solution/policy_source.txt)
- [평가셋](examples/05_pdf_qa_solution/evaluation.csv)

## PDF QA 구축 단계

1. PDF에서 텍스트와 page metadata 로드
2. 빈 페이지와 추출 오류 검사
3. 문단 또는 token 기준 chunk
4. Embedding 생성과 Vector Store 저장
5. 질문 검색과 top-k 출력
6. 문맥 기반 답변과 페이지 인용
7. 평가 CSV 실행

## Loader 검사

임의 페이지 5개를 원본 PDF와 비교합니다. 표·다단 편집·스캔 PDF는 읽기 순서나 OCR 오류가 발생할 수 있습니다.

## Chunk 실험표

| 크기/중첩 | Hit@3 | MRR | 근거성 | P95 |
|---|---:|---:|---:|---:|
| 300/50 | 기록 | 기록 | 기록 | 기록 |
| 600/100 | 기록 | 기록 | 기록 | 기록 |

## 검색 출력

질문마다 문서 ID, 페이지, score와 chunk 원문 일부를 저장합니다. 답변만 저장하면 검색 오류를 추적하기 어렵습니다.

## 권한과 보안

파일 경로를 사용자 입력과 직접 결합하지 않고 허용 디렉터리 안의 문서만 처리합니다. Prompt와 로그에서 개인정보를 마스킹합니다.

## 완료 기준

샘플 PDF, 구축 명령, 20개 이상 평가 질문, 검색·생성 분리 지표, 오류 사례, 재색인 방법과 인용 검증을 제출합니다.
