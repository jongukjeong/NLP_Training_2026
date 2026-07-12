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
