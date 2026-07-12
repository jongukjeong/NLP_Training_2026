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
