# Chapter 9. LSTM과 GRU

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **장단기 메모리(Long Short-Term Memory, LSTM): Gate로 장기 정보를 선택적으로 보존하는 RNN**
- **셀 상태(Cell State): LSTM이 긴 시간 동안 전달하는 핵심 기억**
- **게이트(Gate): 정보를 얼마나 보존·추가·출력할지 조절하는 장치**
- **게이트 순환 유닛(Gated Recurrent Unit, GRU): LSTM보다 단순한 Gate 구조를 사용하는 RNN**

1. [LSTM 구조와 세 Gate](01_LSTM_Gates.md)
2. [GRU와 모델 선택](02_GRU_and_Selection.md)
3. [감성 분석 설계](03_Sentiment_Analysis.md)
4. [퀴즈](04_Summary_and_Quiz.md)
5. [실습: 감성 분석](05_Practice.md)

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
