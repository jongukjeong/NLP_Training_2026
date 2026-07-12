# Chapter 4. 텍스트의 수치화

컴퓨터가 텍스트를 비교하고 학습하려면 문서를 숫자 벡터로 표현해야 합니다. 이 장에서는 Bag of Words, n-gram, TF-IDF와 코사인 유사도를 사용해 문서 표현과 검색 기준선을 만듭니다.

## 학습 목표

- 문서-단어 행렬과 희소 벡터를 설명한다.
- `CountVectorizer`와 `TfidfVectorizer`를 목적에 맞게 설정한다.
- unigram과 n-gram의 장단점을 비교한다.
- 코사인 유사도로 유사 문서를 검색한다.
- 데이터 누수를 막는 학습·평가 절차를 적용한다.
- 어휘 크기, 희소도와 검색 품질을 검증한다.

## 문서 구성

1. [수치화의 목적과 BoW](01_Bag_of_Words.md)
2. [TF-IDF와 n-gram](02_TFIDF_and_Ngrams.md)
3. [코사인 유사도와 검색](03_Similarity_and_Search.md)
4. [평가와 실무 주의사항](04_Evaluation.md)
5. [핵심 정리](05_Summary.md)
6. [퀴즈](06_Quiz.md)
7. [실습 과제](07_Assignment.md)
8. [미니 프로젝트](08_Mini_Project.md)

배포용 코드와 데이터셋은 `examples/07_assignment_solution`과 `examples/08_mini_project_solution`에 함께 있습니다.
