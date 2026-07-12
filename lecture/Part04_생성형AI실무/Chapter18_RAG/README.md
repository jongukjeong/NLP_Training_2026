# Chapter 18. Retrieval-Augmented Generation(RAG)


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
