# Agent 안전과 평가

최소 권한 원칙으로 tool별 읽기/쓰기 scope, 허용 resource, timeout과 호출 횟수를 제한합니다.

필수 평가:

- 올바른 tool 선택률
- argument schema 정확도
- 불필요한 tool 호출률
- 권한 없는 요청 거부율
- loop/재시도 상한
- 최종 답변 정확도와 출처
- latency·비용·실패 복구

Prompt injection, tool output injection과 데이터 exfiltration을 위협 모델에 포함합니다. 중요한 쓰기는 모델이 바로 실행하지 않고 계획 표시 → 사용자 확인 → 실행 → 결과 검증 단계를 둡니다.
