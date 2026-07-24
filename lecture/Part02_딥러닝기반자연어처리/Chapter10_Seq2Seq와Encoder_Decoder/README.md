# Chapter 10. Seq2Seq와 Encoder-Decoder

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **시퀀스-투-시퀀스(Sequence-to-Sequence, Seq2Seq): 입력 Sequence를 다른 출력 Sequence로 바꾸는 모델**
- **인코더(Encoder): 입력을 내부 표현으로 바꾸는 부분**
- **디코더(Decoder): 내부 표현과 이전 출력을 이용해 다음 출력을 만드는 부분**
- **교사 강요(Teacher Forcing): 학습 중 이전 정답 토큰을 다음 입력으로 사용하는 방법**
- **빔 탐색(Beam Search): 점수가 높은 여러 생성 후보를 함께 유지하는 탐색 방법**

1. [10.1~10.3 Seq2Seq·Encoder·Decoder](01_Seq2Seq_Architecture.md)
2. [10.4 Teacher Forcing](02_Teacher_Forcing.md)
3. [10.5 Beam Search](03_Beam_Search.md)
4. [10.6 번역 파이프라인과 평가](04_Translation_Evaluation.md)
5. [퀴즈](05_Summary_and_Quiz.md)
6. [실습: 번역 모델 구현](06_Practice.md)

이 장은 교육용 문자 단위 번역 모델로 입력/출력 tensor와 inference loop를 이해합니다. 실제 번역 품질을 위한 규모의 모델이 아닙니다.

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
