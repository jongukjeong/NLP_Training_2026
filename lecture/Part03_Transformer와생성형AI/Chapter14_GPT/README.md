# Chapter 14. GPT

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **디코더 전용 모델(Decoder-only Model): Decoder 블록만 사용해 다음 토큰을 생성하는 모델**
- **자기회귀(Autoregression): 이전 출력들을 조건으로 다음 값을 순서대로 예측하는 방식**
- **프롬프트(Prompt): 모델에 전달하는 목표·입력·제약·출력 형식**
- **구조화 출력(Structured Output): JSON처럼 프로그램이 검사할 수 있는 정해진 형식**
- **환각(Hallucination): 근거 없이 그럴듯한 사실을 생성하는 현상**

1. [Decoder Only와 Auto Regression](01_GPT_Architecture.md)
2. [Prompting·Text Generation·ChatGPT](02_Prompting_and_Generation.md)
3. [퀴즈](03_Summary_and_Quiz.md)
4. [실습: GPT API 활용](04_Practice.md)

API 실습은 OpenAI Responses API와 공식 Python SDK를 사용하며 키를 저장소에 저장하지 않습니다.

## 먼저 읽을 상세 가이드

- [비전공자용 GPT 생성 워크북](00_비전공자_GPT_생성워크북.md): 자기회귀 확률, 생성 설정, 구조화 출력과 오류 검증을 쉽게 설명합니다.

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
