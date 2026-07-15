# Chapter 11. Attention Mechanism

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **어텐션(Attention): 출력에 필요한 입력 위치를 점수화해 선택적으로 참고하는 계산**
- **쿼리(Query, Q): 현재 찾고 싶은 정보**
- **키(Key, K): Query와 비교하기 위한 색인 표현**
- **값(Value, V): Attention 가중치에 따라 가져올 실제 정보**
- **마스크(Mask): 보면 안 되는 위치를 계산에서 제외하는 장치**

Attention의 등장 배경, Bahdanau(Additive), Luong(Multiplicative), Self Attention을 학습하고 attention weight를 시각화합니다.

1. [핵심 강의](01_Attention.md)
2. [퀴즈](02_Summary_and_Quiz.md)
3. [실습: Attention Visualization](03_Practice.md)

## 먼저 읽을 상세 가이드

- [비전공자용 Attention 계산 워크북](00_비전공자_Attention_계산워크북.md): Query·Key·Value부터 Mask와 행렬 shape까지 작은 숫자로 확인합니다.

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
