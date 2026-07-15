# Chapter 12. Transformer

<!-- BEGIN: BEGINNER_LEARNING_PATH -->
## 권장 학습 순서

```text
Step by Step → Basic Practice → Practice·Assignment → 피드백 → Solution
```

비전공자와 입문자는 [단계별 학습 경로](LEARNING_PATH.md)를 먼저 확인합니다. 완성형 solution의 고급 구조는 선택 학습입니다.
<!-- END: BEGINNER_LEARNING_PATH -->

## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **트랜스포머(Transformer): Attention 중심으로 Sequence를 처리하는 신경망 구조**
- **위치 인코딩(Positional Encoding): 토큰 순서를 알려 주는 위치 정보**
- **다중 헤드 어텐션(Multi-Head Attention): 여러 관점의 Attention을 병렬로 계산하는 구조**
- **층 정규화(Layer Normalization): 표현의 값 규모를 조정해 학습을 안정시키는 방법**
- **잔차 연결(Residual Connection): 입력을 변환 결과에 더해 정보 흐름을 돕는 연결**

1. [Architecture와 Positional Encoding](01_Architecture_and_Position.md)
2. [Multi-Head Attention·FFN·LayerNorm](02_Transformer_Blocks.md)
3. [퀴즈](03_Summary_and_Quiz.md)
4. [실습: Transformer 구현](04_Practice.md)

## 먼저 읽을 상세 가이드

- [비전공자용 Transformer 블록 워크북](00_비전공자_Transformer_블록워크북.md): 위치 정보, Multi-Head, FFN, 잔차 연결과 LayerNorm을 계산 흐름으로 연결합니다.

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
