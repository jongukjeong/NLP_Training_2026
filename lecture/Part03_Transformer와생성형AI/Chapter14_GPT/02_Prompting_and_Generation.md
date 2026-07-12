# 14.3 Prompting · 14.4 Text Generation · 14.5 ChatGPT 이해

좋은 prompt는 역할, 목표, 입력, 제약, 출력 형식과 평가 기준을 명확히 합니다. 중요한 규칙은 모호한 수사보다 검사 가능한 조건으로 작성합니다.

ChatGPT는 모델 하나의 이름이 아니라 대화형 제품 경험이며, API 애플리케이션은 모델 호출, 상태, 도구, 보안, 평가를 개발자가 구성합니다.

운영 원칙:

- API key는 환경변수·secret manager에 저장
- 사용자 입력과 모델 출력을 신뢰 경계로 취급
- timeout, retry, rate limit과 비용 예산 설정
- model ID, prompt version, request ID, latency 기록
- 개인·기밀정보 전송 정책 확인
- 고위험 결정에는 사람 검토
