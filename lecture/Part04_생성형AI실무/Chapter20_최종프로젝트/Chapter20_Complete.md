# Chapter 20 통합 강의 원고

> 이 문서는 Chapter  원본 강의 문서를 학습 순서대로 합친 통합본입니다. 개별 원본 파일은 그대로 유지합니다.

---

<!-- SOURCE: README.md -->

# Chapter 20. 최종 프로젝트

## 프로젝트: 근거 기반 고객지원 AI Assistant

내부 정책 지식에서 관련 문서를 검색하고 출처와 함께 답변합니다. API 키가 있으면 검색 근거만 사용하는 생성 답변을 만들고, 없으면 검색된 정책 문장을 그대로 제공하는 안전한 기준선으로 동작합니다.

## 학습 단계

1. [프로젝트 기획](01_Project_Planning.md)
2. [데이터 수집](02_Data_Collection.md)
3. [모델 개발](03_Model_Development.md)
4. [서비스 구현](04_Service_Implementation.md)
5. [발표 및 피드백](05_Presentation_and_Feedback.md)

## 완성 예제

[final_project_solution](final_project_solution/README.md)에 다음을 포함합니다.

- versioned knowledge/evaluation CSV
- TF-IDF hybrid-ready retriever
- 출처 포함 CLI assistant
- 선택형 OpenAI Responses API 생성
- Hit@1·Hit@3·MRR 평가
- 단위 테스트
- 프로젝트 보고서·발표 템플릿

## 완료 기준

- `pytest` 통과
- 평가셋 Hit@3 목표 달성
- 근거 없는 질문의 low-score 처리
- 모든 답변에 source 표시
- API key 없이도 실행
- 개인정보·권한·비용·실패 대응 설명

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.

---

<!-- SOURCE: 00_원리_수학_실습_가이드.md -->

# Chapter 20 원리·수학·실습 가이드

## 1. 프로젝트의 출발점

“챗봇 만들기”가 아니라 `누가, 어떤 상황에서, 어떤 결정을 더 잘하도록, 무엇을 제공하는가`를 한 문장으로 정의한다. 성공 지표와 실패 허용 범위를 구현 전에 정한다.

```text
사용자: 사내 상담원
문제: 정책 문서를 찾는 데 오래 걸림
입력/출력: 질문 → 근거 인용 답변
목표: Hit@3 ≥ 0.85, 근거 정확도 ≥ 0.90, P95 ≤ 5초
안전: 근거가 없으면 답변 보류
```

## 2. 데이터와 분할

데이터 명세에는 출처, 라이선스, 개인정보, 스키마, 중복 제거, 레이블 지침, 버전을 기록한다. 같은 문서의 청크가 train과 test에 동시에 들어가면 누수다. 사용자·문서·시간 단위 분할을 검토한다.

## 3. 기준선과 평가

가장 단순한 키워드 검색 또는 규칙 기반 모델을 먼저 만든다. 복잡한 모델은 같은 평가셋에서 기준선을 유의미하게 넘어야 한다.

\[
F1=\frac{2PR}{P+R},\quad MRR=\frac1N\sum_i\frac1{rank_i}
\]

최종 점수 하나로 합치기보다 품질, 근거성, 안전, 비용, 지연을 대시보드로 분리한다. 전체 평균과 함께 중요 하위 집단 및 실패 유형을 본다.

## 4. 서비스 구조와 예산

`UI/API → 입력 검증 → 검색/모델 → 출력 검증 → 로그·모니터링`

\[
MonthlyCost\approx Requests\times AverageCostPerRequest
\]

일 5,000건, 건당 20원이면 30일 기준 약 300만원이다. 캐시, 작은 모델 라우팅, 토큰 제한을 품질 저하와 함께 실험한다. 비밀키는 환경변수/secret manager로 관리하고 로그에서 개인정보를 마스킹한다.

## 5. 실험과 발표

| 버전 | 변경점 | 품질 | 근거성 | P95 | 비용 | 결론 |
|---|---|---:|---:|---:|---:|---|
| baseline | 키워드 검색 | 기록 | 기록 | 기록 | 기록 | 기준 |
| v1 | 임베딩 검색 | 기록 | 기록 | 기록 | 기록 | 비교 |
| v2 | hybrid+rerank | 기록 | 기록 | 기록 | 기록 | 채택/기각 |

발표는 문제와 사용자, 데이터, 기준선, 설계 선택, 정량 결과, 실제 실패 사례, 비용·안전, 다음 실험 순으로 구성한다. 성공 사례만 보여주지 말고 실패 원인과 완화책을 시연한다.

## 완료 기준

- 새 환경에서 README만으로 실행 가능
- 데이터·모델·프롬프트 버전 재현 가능
- 자동 평가와 대표 수동 평가 통과
- 오류·비용·지연 모니터링 존재
- 개인정보·라이선스·권한 검토 완료

1. 좋은 프로젝트 목표 문장에 포함할 요소는?
2. 기준선이 필요한 이유는?
3. 최종 발표에서 실패 사례를 보여줘야 하는 이유는?

---

<!-- SOURCE: 01_Project_Planning.md -->

# 20.1 프로젝트 기획

## 문제 정의

고객지원 담당자가 배송·환불·계정 정책을 빠르게 찾고, 고객에게 보낼 답변 초안을 근거와 함께 얻도록 돕습니다.

## 범위

포함: 정책 검색, 출처 표시, 답변 초안, retrieval 평가.  
제외: 환불 실행, 주문 변경, 개인정보 조회, 자동 발송.

## 성공 기준

| 구분 | 기준 |
|---|---|
| Retrieval | Hit@3 ≥ 목표값, MRR 기록 |
| Grounding | 답변마다 source ID 포함 |
| 안전 | 근거 부족 시 모른다고 응답 |
| 운영 | API key 없이 기준선 실행 |
| 재현 | 데이터·설정·평가 결과 version 기록 |

이해관계자, 사용자 journey, 위험, 일정과 역할을 `templates/PROJECT_REPORT_TEMPLATE.md`에 작성합니다.

## 좋은 프로젝트 문장 만들기

“RAG 챗봇 개발”은 기술 이름만 있고 성공 조건이 없습니다. 다음 다섯 요소를 포함합니다.

```text
사용자: 사내 상담원
상황: 고객 통화 중 정책 확인
입력/출력: 질문 → 출처가 포함된 답변
성공지표: Hit@3 0.85 이상, 근거 정확도 0.90 이상
제약: P95 5초, 개인정보 외부 전송 금지
```

## 목표 지표를 분리하기

검색 품질, 답변 정확성, 근거성, 안전, 지연, 비용을 하나의 점수로 숨기지 않습니다. 어떤 구성요소가 실패했는지 알 수 있도록 각각 측정합니다.

\[
MonthlyCost=MonthlyRequests\times AverageCostPerRequest
\]

월 100,000건, 건당 평균 15원이면 예상 월 비용은 150만원입니다. 개발 단계부터 비용 예산을 세우면 모델·문맥 길이·캐시 결정을 설명할 수 있습니다.

## 데이터 분할과 누수

같은 원문에서 나온 청크가 train과 test에 나뉘면 거의 같은 문장이 양쪽에 들어갈 수 있습니다. 문서 ID, 사용자, 시간 단위 분할을 검토합니다. test는 최종 판단에만 사용합니다.

## 기준선

키워드 검색, 다수 클래스, 규칙 기반 응답처럼 단순한 기준선을 먼저 만듭니다. 복잡한 모델은 같은 평가셋에서 품질이나 비용 면에서 기준선을 넘어야 채택 근거가 생깁니다.

## 위험 목록

| 위험 | 조기 신호 | 완화책 |
|---|---|---|
| 근거 없는 답 | 인용 불일치 | 답변 보류 규칙 |
| 검색 실패 | Recall@k 저하 | hybrid/rerank 실험 |
| 비용 초과 | 입력 토큰 증가 | 문맥 제한·캐시 |
| 개인정보 노출 | 로그 원문 저장 | 마스킹·보존 정책 |
| 지연 증가 | P95 초과 | 단계 축소·작은 모델 |

## 완료의 정의

코드 실행만이 아니라 새 환경 재현, 자동 평가 통과, 실패 사례 문서화, 비용·지연 측정, 보안 검토, 발표 자료까지 완료 기준에 포함합니다.

---

<!-- SOURCE: 02_Data_Collection.md -->

# 20.2 데이터 수집

Knowledge schema:

| field | 설명 |
|---|---|
| document_id | 안정적인 문서 ID |
| title | 정책 제목 |
| content | 검색·답변 근거 |
| source | 원본 위치 |
| version | 정책 version |
| access_level | 접근 등급 |

Evaluation schema는 `query`, `relevant_id`, `expected_fact`를 가집니다. 평가 질문을 knowledge 문장 그대로 복사하지 않고 실제 사용자 표현·동의어·모호한 질문을 포함합니다.

수집 시 개인정보와 기밀정보를 제거하고 문서별 owner, 갱신일, 삭제 절차를 관리합니다. train/evaluation 중복과 거의 동일한 질문을 점검합니다.

---

<!-- SOURCE: 03_Model_Development.md -->

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

---

<!-- SOURCE: 04_Service_Implementation.md -->

# 20.4 서비스 구현

완성 예제는 CLI service지만 UI/API로 확장 가능한 모듈 구조입니다.

- `src/retriever.py`: index와 search
- `src/app.py`: 답변·source·optional LLM
- `src/evaluate.py`: retrieval 평가
- `tests/`: 핵심 동작 회귀 테스트

운영 전 추가할 항목:

- 사용자 인증과 document-level authorization
- timeout/retry/rate limit
- secret manager
- request ID와 privacy-safe log
- health check와 rollback
- feedback 저장과 prompt injection 방어

검색 score가 threshold보다 낮으면 추측하지 않고 지원센터 확인을 안내합니다.

---

<!-- SOURCE: 05_Presentation_and_Feedback.md -->

# 20.5 발표 및 피드백

## 10분 발표 구성

1. 문제와 사용자(1분)
2. 데이터와 보안(1분)
3. architecture(2분)
4. live demo(2분)
5. 평가 결과와 실패 사례(2분)
6. 한계와 다음 단계(1분)
7. 질문(1분)

정답 사례만 보여주지 말고 low-score, 동의어 검색 실패, 정책 version 충돌 같은 실패 사례와 개선 우선순위를 제시합니다.

피드백은 사실성, 출처, usability, 안전, 운영 가능성으로 분류하고 다음 iteration의 issue와 담당자로 전환합니다. [발표 템플릿](final_project_solution/templates/PRESENTATION_TEMPLATE.md)을 사용합니다.

