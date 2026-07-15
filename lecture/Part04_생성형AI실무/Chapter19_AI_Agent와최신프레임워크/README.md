# Chapter 19. AI Agent와 최신 프레임워크

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **함수 호출(Function Calling): 모델이 함수 이름과 인자를 구조화해 제안하는 방식**
- **도구 호출(Tool Calling): 모델이 외부 검색·계산·API 사용을 요청하는 방식**
- **AI 에이전트(AI Agent): 목표를 위해 여러 단계에서 도구를 선택하고 결과를 확인하는 시스템**
- **모델 컨텍스트 프로토콜(Model Context Protocol, MCP): 모델 앱과 외부 Resource·Tool을 연결하는 규약**
- **멱등성(Idempotency): 같은 요청을 반복해도 최종 결과가 같은 성질**

1. [Function Calling·Tool Calling·MCP](01_Tools_and_MCP.md)
2. [LangChain·LangGraph와 설계](02_Frameworks.md)
3. [안전과 평가](03_Safety_and_Evaluation.md)
4. [퀴즈](04_Summary_and_Quiz.md)
5. [실습: AI Assistant](05_Practice.md)

## 먼저 읽을 상세 가이드

- [비전공자용 AI Agent 신뢰성 워크북](00_비전공자_Agent_신뢰성워크북.md): 도구 호출, 권한, 전체 성공률, 재시도와 감사 로그를 쉽게 설명합니다.

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
