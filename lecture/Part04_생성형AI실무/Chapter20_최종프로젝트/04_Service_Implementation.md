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

## 서비스 경계

UI/API, 입력 검증, 모델·검색, 출력 검증, 로그·모니터링을 분리합니다. 각 구성요소의 입력·출력과 timeout을 정합니다.

## API 계약

요청 필드, 최대 길이, 응답 schema, 오류 코드와 버전을 문서화합니다. 모델 내부 오류를 그대로 사용자에게 노출하지 않습니다.

## 안전

비밀키는 환경변수, 사용자 파일은 허용 경로, 외부 쓰기는 승인, 로그는 개인정보 마스킹을 적용합니다.

## 성능

P50/P95, 처리량, peak memory와 오류율을 동시 사용자 조건에서 측정합니다. 평균 한 번의 속도만 보고 운영 용량을 결정하지 않습니다.

## 모니터링

요청 수, 오류 코드, 지연, 비용, 모델·Prompt 버전, 검색 실패율과 사용자 피드백을 추적합니다.

## 배포·복구

Health check, 이전 버전 rollback, 데이터·index 갱신, 장애 중 안전한 안내와 담당자 연락 절차를 준비합니다.
