# 07. 실습 과제

## 과제: TF-IDF 문서 검색

`faq.csv`를 읽어 다음을 구현합니다.

1. `question`과 `answer` 필수 열을 검사합니다.
2. 질문 텍스트로 unigram+bigram TF-IDF 행렬을 만듭니다.
3. 질의 `배송이 늦습니다`와 유사한 FAQ 상위 3개를 출력합니다.
4. 순위, 문서 ID, 점수와 답변을 CSV로 저장합니다.
5. 어휘 크기, 행렬 크기와 0점 결과 수를 보고합니다.

## 배포용 답안

- [안내](examples/07_assignment_solution/README.md)
- [코드](examples/07_assignment_solution/tfidf_search.py)
- [데이터셋](examples/07_assignment_solution/faq.csv)
