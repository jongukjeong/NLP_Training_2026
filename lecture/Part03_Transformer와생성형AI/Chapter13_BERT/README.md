# Chapter 13. BERT


## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **양방향 인코더(Bidirectional Encoder): 토큰의 앞뒤 문맥을 함께 참고하는 Encoder**
- **마스크 언어 모델링(Masked Language Modeling, MLM): 가린 토큰을 맞히는 사전학습 방법**
- **미세조정(Fine-tuning): 사전학습 모델을 특정 과제로 추가 학습하는 과정**
- **로짓(Logit): 확률 변환 전 클래스별 원점수**

1. [Bidirectional Encoder·MLM·NSP](01_BERT_Pretraining.md)
2. [Fine-tuning과 Sentence Classification](02_Fine_Tuning.md)
3. [퀴즈](03_Summary_and_Quiz.md)
4. [실습: 한국어 BERT 활용](04_Practice.md)

## 먼저 읽을 상세 가이드

- [비전공자용 BERT 분류 워크북](00_비전공자_BERT_분류워크북.md): MLM부터 Logit, Fine-tuning과 분류 평가까지 단계별로 확인합니다.

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
