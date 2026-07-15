# 실습: 번역 모델 구현

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 난이도와 Solution 공개 원칙

- 기본 요구사항을 먼저 작은 단계로 나누어 실행합니다.
- 함수화, 타입 힌트, 복합 평가와 운영 기능은 선택 확장입니다.
- solution은 직접 시도하고 공통 오류 피드백을 받은 뒤 공개합니다.
- 처음부터 solution과 같은 구조로 작성하는 것은 목표가 아닙니다.
<!-- END: BEGINNER_LEARNING_PATH -->

짧은 영어-한국어 문자 단위 번역쌍으로 Encoder-Decoder를 학습하고 greedy inference 예제를 실행합니다.

- [안내](examples/06_translation_solution/README.md)
- [완성 코드](examples/06_translation_solution/seq2seq_translation.py)
- [데이터셋](examples/06_translation_solution/translations.csv)

실습 완료 후 tensor shape, teacher forcing용 shift, 시작·종료 token과 inference loop를 설명할 수 있어야 합니다.
