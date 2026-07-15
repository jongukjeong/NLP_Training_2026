# Chapter 15. Hugging Face

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **체크포인트(Checkpoint): 특정 시점의 모델 가중치와 설정**
- **토크나이저(Tokenizer): 문자열을 토큰과 정수 ID로 바꾸는 도구**
- **파이프라인(Pipeline): 전처리·추론·후처리를 연결한 실행 흐름**
- **미세조정(Fine-tuning): 사전학습 모델을 특정 데이터로 추가 학습하는 과정**
- **동적 패딩(Dynamic Padding): Batch마다 가장 긴 입력에 맞춰 Padding하는 방식**

1. [Transformers·AutoTokenizer·AutoModel](01_Auto_Classes.md)
2. [Pipeline과 Fine-tuning](02_Pipeline_and_Fine_Tuning.md)
3. [퀴즈](03_Summary_and_Quiz.md)
4. [실습: 한국어 모델 활용](04_Practice.md)

## 먼저 읽을 상세 가이드

- [비전공자용 Hugging Face 실행 워크북](00_비전공자_HuggingFace_실행워크북.md): Checkpoint와 Auto Class부터 저장·재로딩 검증까지 다룹니다.

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
