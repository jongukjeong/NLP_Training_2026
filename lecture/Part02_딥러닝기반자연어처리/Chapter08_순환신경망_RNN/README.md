# Chapter 8. 순환신경망(RNN)

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **순환신경망(Recurrent Neural Network, RNN): 이전 정보를 다음 시점으로 전달하는 신경망**
- **은닉 상태(Hidden State): 현재까지 읽은 정보를 요약해 다음 시점으로 전달하는 값**
- **시간 역전파(Backpropagation Through Time, BPTT): RNN을 시간축으로 펼쳐 기울기를 계산하는 방법**
- **기울기 소실(Vanishing Gradient): 역전파 과정에서 기울기가 지나치게 작아지는 문제**

1. [Sequence Data와 Vanilla RNN](01_Sequence_and_RNN.md)
2. [BPTT와 Vanishing Gradient](02_BPTT_and_Gradient.md)
3. [문장 분류 설계](03_Sentence_Classification.md)
4. [퀴즈](04_Summary_and_Quiz.md)
5. [실습: 문장 분류](05_Practice.md)

목표는 timestep, hidden state, padding/masking과 RNN의 gradient 한계를 이해하고 문장 분류 모델을 완성하는 것입니다.

## 먼저 읽을 상세 가이드

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
