# Chapter 20. 최종 프로젝트 — 통합 원고

> 이 문서는 Chapter 20. 최종 프로젝트 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 20. 최종 프로젝트 — `README.md`
- 20.1 프로젝트 기획 — `01_Project_Planning.md`
- 20.2 데이터 수집 — `02_Data_Collection.md`
- 20.3 모델 개발 — `03_Model_Development.md`
- 20.4 서비스 구현 — `04_Service_Implementation.md`
- 20.5 발표 및 피드백 — `05_Presentation_and_Feedback.md`

---

<!-- SOURCE: README.md -->

# Chapter 20. 최종 프로젝트

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


---

<!-- SOURCE: 01_Project_Planning.md -->

# 20.1 프로젝트 기획

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


---

<!-- SOURCE: 02_Data_Collection.md -->

# 20.2 데이터 수집

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

