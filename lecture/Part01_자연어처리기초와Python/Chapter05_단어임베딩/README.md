# Chapter 5. 단어 임베딩

단어 임베딩은 단어를 저차원의 밀집 벡터로 표현해 사용 맥락이 비슷한 단어를 가까이 배치합니다. 이 장에서는 분포 가설, 동시출현 행렬, Word2Vec 계열 개념, 사전학습 임베딩과 임베딩 평가를 다룹니다.

## 학습 목표

- 희소 표현과 밀집 임베딩의 차이를 설명한다.
- 분포 가설과 문맥 창의 역할을 이해한다.
- 동시출현 행렬과 SVD로 작은 임베딩을 만든다.
- 코사인 유사도로 유사 단어를 검색한다.
- Word2Vec의 CBOW와 Skip-gram을 구분한다.
- OOV, 편향, 도메인 변화와 평가 한계를 점검한다.

## 문서 구성

1. [임베딩의 개념](01_Embedding_Concepts.md)
2. [동시출현과 SVD](02_Cooccurrence_and_SVD.md)
3. [Word2Vec과 사전학습 임베딩](03_Word2Vec_and_Pretrained.md)
4. [유사도·평가·편향](04_Evaluation_and_Bias.md)
5. [핵심 정리](05_Summary.md)
6. [퀴즈](06_Quiz.md)
7. [실습 과제](07_Assignment.md)
8. [미니 프로젝트](08_Mini_Project.md)

배포 자료는 각 Chapter 하위 `examples/`에 코드와 데이터셋을 함께 둡니다.
