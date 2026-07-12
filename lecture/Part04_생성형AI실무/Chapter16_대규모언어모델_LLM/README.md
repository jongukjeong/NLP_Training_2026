# Chapter 16. 대규모 언어모델(LLM)


## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **대규모 언어모델(Large Language Model, LLM): 많은 파라미터와 텍스트로 학습한 언어모델**
- **양자화(Quantization): 숫자 정밀도를 낮춰 모델 메모리와 계산량을 줄이는 방법**
- **키-값 캐시(Key-Value Cache, KV Cache): 생성 중 이전 토큰의 Attention 계산 결과를 저장하는 공간**
- **첫 토큰 지연(Time To First Token, TTFT): 요청부터 첫 토큰 출력까지 걸린 시간**

1. [LLM 개요와 모델 계열](01_LLM_and_Model_Families.md)
2. [로컬 실행과 운영 판단](02_Local_LLM_Operations.md)
3. [퀴즈](03_Summary_and_Quiz.md)
4. [실습: 로컬 LLM 실행](04_Practice.md)

## 먼저 읽을 상세 가이드

- [비전공자용 로컬 LLM 용량 워크북](00_비전공자_로컬LLM_용량워크북.md): 파라미터 메모리, 양자화, KV Cache와 성능 지표를 손으로 계산합니다.

- [원리·수학·실습 연결 가이드](00_원리_수학_실습_가이드.md): 직관, 핵심 공식, 수치 예, 구현 점검을 한 흐름으로 학습합니다.
