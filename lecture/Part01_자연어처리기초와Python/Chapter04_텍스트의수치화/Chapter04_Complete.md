# Chapter 4. 텍스트의 수치화 — 통합 원고

> 이 문서는 Chapter 4. 텍스트의 수치화 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 4. 텍스트의 수치화 — `README.md`
- 01. 수치화의 목적과 Bag of Words — `01_Bag_of_Words.md`
- 02. TF-IDF와 n-gram — `02_TFIDF_and_Ngrams.md`
- 03. 코사인 유사도와 검색 — `03_Similarity_and_Search.md`
- 04. 평가와 실무 주의사항 — `04_Evaluation.md`
- 05. 핵심 정리 — `05_Summary.md`
- 06. 퀴즈 — `06_Quiz.md`
- 07. 실습 과제 — `07_Assignment.md`
- 08. 미니 프로젝트: 평가 가능한 FAQ 검색기 — `08_Mini_Project.md`

---

<!-- SOURCE: README.md -->

# Chapter 4. 텍스트의 수치화

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


---

<!-- SOURCE: 01_Bag_of_Words.md -->

# 01. 수치화의 목적과 Bag of Words

# 01. 수치화의 목적과 Bag of Words

## 문서를 벡터로 바꾸기

Bag of Words(BoW)는 문서에 어떤 단어가 몇 번 등장했는지를 벡터로 표현합니다.

```text
문서 A: 배송 빠름
문서 B: 배송 지연
어휘: [배송, 빠름, 지연]
A:     [1,   1,   0]
B:     [1,   0,   1]
```

단순하고 설명하기 쉬우며 분류·검색의 강력한 기준선입니다. 다만 단어 순서와 문맥을 대부분 잃습니다.

## CountVectorizer

```python
from sklearn.feature_extraction.text import CountVectorizer

documents = ["배송 빠름", "배송 지연", "환불 요청"]
vectorizer = CountVectorizer(token_pattern=r"(?u)\b\w+\b")
matrix = vectorizer.fit_transform(documents)

print(vectorizer.get_feature_names_out())
print(matrix.toarray())
```

한국어 전처리 결과가 공백 토큰으로 준비됐다면 `token_pattern`을 명시해 한 글자 토큰 처리 정책을 통제합니다.

## 희소 행렬

실제 어휘가 50,000개여도 한 문서에 등장하는 단어는 일부입니다. scikit-learn은 0을 모두 저장하지 않는 희소 행렬을 사용합니다. 큰 데이터에서 `toarray()`로 전체를 밀집 행렬로 바꾸면 메모리가 급증하므로 작은 확인용으로만 사용합니다.

## 어휘 제어

```python
CountVectorizer(
    min_df=2,
    max_df=0.95,
    max_features=20_000,
)
```

- `min_df`: 너무 드문 항목 제거
- `max_df`: 거의 모든 문서에 나오는 항목 제거
- `max_features`: 최대 특징 수 제한

이 값은 데이터 크기와 평가 결과를 기준으로 정하며 평가 데이터에 맞춰 조정하지 않습니다.

> 다음: [TF-IDF와 n-gram](02_TFIDF_and_Ngrams.md)


---

<!-- SOURCE: 02_TFIDF_and_Ngrams.md -->

# 02. TF-IDF와 n-gram

# 02. TF-IDF와 n-gram

## TF-IDF

TF-IDF는 한 문서에서 자주 등장하지만 전체 문서에서는 드문 단어에 높은 가중치를 줍니다.

```text
TF-IDF = 문서 내 빈도(TF) × 역문서 빈도(IDF)
```

모든 문서에 등장하는 단어보다 특정 문서를 구분하는 단어를 강조합니다.

```python
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    min_df=1,
    sublinear_tf=True,
    norm="l2",
)
matrix = vectorizer.fit_transform(documents)
```

## n-gram

- unigram: 단어 하나 (`환불`)
- bigram: 연속 단어 둘 (`환불 요청`)
- trigram: 연속 단어 셋

bigram은 `배송 지연`, `환불 불가`처럼 일부 순서를 보존하지만 특징 수가 증가하고 드문 조합이 많아집니다.

## 문자 n-gram

띄어쓰기 변이가 큰 데이터에서는 문자 n-gram이 유용할 수 있습니다.

```python
TfidfVectorizer(analyzer="char", ngram_range=(2, 5), min_df=2)
```

오탈자와 띄어쓰기 변화에 강하지만 특징 의미를 해석하기 어렵고 행렬이 커질 수 있습니다.

## fit과 transform 분리

```python
train_matrix = vectorizer.fit_transform(train_texts)
test_matrix = vectorizer.transform(test_texts)
```

평가 데이터까지 `fit_transform()`하면 평가 데이터의 어휘와 문서 빈도가 학습에 반영되어 데이터 누수가 발생합니다.

> 다음: [코사인 유사도와 검색](03_Similarity_and_Search.md)


---

<!-- SOURCE: 03_Similarity_and_Search.md -->

# 03. 코사인 유사도와 검색

# 03. 코사인 유사도와 검색

코사인 유사도는 두 벡터의 방향이 얼마나 비슷한지 측정합니다. 값이 1에 가까울수록 방향이 유사합니다.

```python
from sklearn.metrics.pairwise import cosine_similarity

query_vector = vectorizer.transform(["배송이 늦어요"])
scores = cosine_similarity(query_vector, document_matrix).ravel()
best_indices = scores.argsort()[::-1][:3]
```

## 검색 결과에 포함할 정보

- 문서 ID
- 원문 또는 제목
- 유사도 점수
- 순위
- 사용한 벡터라이저 설정과 버전

## 0점과 동점

질의의 단어가 어휘에 하나도 없으면 질의 벡터가 0이 되고 모든 점수가 0일 수 있습니다. 이때 첫 문서를 정답처럼 반환하지 말고 “검색 가능한 단어가 없습니다”라는 상태를 처리합니다.

동점은 문서 ID 등 안정적인 보조 기준으로 정렬해 재현성을 확보합니다.

## TF-IDF 검색의 한계

`반품`과 `환불`처럼 의미는 비슷하지만 표면 단어가 다르면 유사도가 낮을 수 있습니다. 이는 Chapter 5의 임베딩이 필요한 이유입니다. 그럼에도 TF-IDF는 빠르고 설명 가능하며 도메인 단어가 명확한 검색에서 좋은 기준선입니다.

> 다음: [평가와 실무 주의사항](04_Evaluation.md)


---

<!-- SOURCE: 04_Evaluation.md -->

# 04. 평가와 실무 주의사항

# 04. 평가와 실무 주의사항

## 검색 평가 데이터

질의별로 관련 문서 ID를 준비합니다.

```text
질의: 배송이 늦어요
관련 문서: delivery_delay
```

대표 지표:

- Hit@k: 상위 k개 안에 관련 문서가 있는 비율
- MRR: 첫 관련 문서 순위의 역수 평균
- Precision@k: 상위 k개 중 관련 문서 비율

## 수치화 품질 점검

| 점검 항목 | 위험 신호 |
|---|---|
| 어휘 크기 | 지나치게 크거나 작음 |
| 0 벡터 비율 | 새 문서의 어휘가 대부분 미등록 |
| 희소도 | 특징 증가로 메모리·속도 악화 |
| 상위 가중치 | 개인정보·오류 문자열이 특징을 지배 |
| 검색 오답 | 동의어·띄어쓰기·오탈자 문제 반복 |

## 파이프라인 저장

학습한 어휘와 IDF를 재학습 없이 같은 상태로 사용해야 합니다. 운영에서는 전처리 코드, 벡터라이저, 설정, 학습 데이터 버전을 묶어 관리합니다.

## 보안

어휘 목록에는 이메일, 전화번호와 식별자가 남을 수 있습니다. Chapter 3에서 마스킹한 데이터를 사용하고, 모델·로그·직렬화 파일 접근 권한을 관리합니다.

> 다음: [핵심 정리](05_Summary.md)


---

<!-- SOURCE: 05_Summary.md -->

# 05. 핵심 정리

# 05. 핵심 정리

```text
정제 텍스트 → 어휘 학습 → 문서-단어 행렬 → TF-IDF 가중치
→ 질의 벡터화 → 코사인 유사도 → 순위와 품질 평가
```

- BoW는 단어 등장 횟수로 문서를 표현한다.
- TF-IDF는 문서를 구분하는 단어를 강조한다.
- n-gram은 일부 순서를 보존하지만 특징 수를 늘린다.
- 희소 행렬은 큰 어휘를 효율적으로 저장한다.
- 벡터라이저는 학습 데이터에만 fit한다.
- 0 벡터와 동점 검색 결과를 명시적으로 처리한다.
- TF-IDF 검색은 의미적 동의어 처리에 한계가 있다.

다음 장에서는 단어를 밀집 벡터로 표현해 의미적 유사성을 다룹니다.

> 다음: [퀴즈](06_Quiz.md)


---

<!-- SOURCE: 06_Quiz.md -->

# 06. 퀴즈

# 06. 퀴즈

## 문제

1. BoW가 주로 잃는 정보는 무엇인가요?
2. TF-IDF가 전체 문서에서 흔한 단어의 가중치를 낮추는 이유는 무엇인가요?
3. bigram을 추가할 때 발생하는 대표적인 비용은 무엇인가요?
4. 평가 데이터에 `fit_transform()`을 사용하면 안 되는 이유는 무엇인가요?
5. 질의 벡터가 0이면 검색 결과를 어떻게 처리해야 하나요?
6. TF-IDF 검색이 동의어 처리에 약한 이유는 무엇인가요?

## 정답

1. 단어 순서와 문맥입니다.
2. 문서를 구분하는 정보가 적기 때문입니다.
3. 특징 수와 희소성이 증가합니다.
4. 평가 데이터 정보가 학습에 섞이는 데이터 누수가 생깁니다.
5. 임의의 1위 문서를 반환하지 말고 검색 불가 상태를 알려야 합니다.
6. 표면 단어가 다르면 의미가 비슷해도 벡터 차원을 공유하지 않기 때문입니다.

> 다음: [실습 과제](07_Assignment.md)


---

<!-- SOURCE: 07_Assignment.md -->

# 07. 실습 과제

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

> 다음: [미니 프로젝트](08_Mini_Project.md)


---

<!-- SOURCE: 08_Mini_Project.md -->

# 08. 미니 프로젝트: 평가 가능한 FAQ 검색기

# 08. 미니 프로젝트: 평가 가능한 FAQ 검색기

## 목표

FAQ 검색기와 평가 질의셋을 함께 제공해 설정 변화가 검색 품질에 미치는 영향을 측정합니다.

## 필수 기능

- FAQ와 평가 CSV의 스키마 검사
- TF-IDF 기반 상위 k개 검색
- 0 벡터 처리
- 결과 CSV 저장
- Hit@1, Hit@3과 MRR 계산
- 설정과 평가 결과 JSON 저장

## 실행

```powershell
cd lecture\Part01_자연어처리기초와Python\Chapter04_텍스트의수치화\examples\08_mini_project_solution
python faq_search_evaluator.py
```

## 배포용 예제

- [안내](examples/08_mini_project_solution/README.md)
- [코드](examples/08_mini_project_solution/faq_search_evaluator.py)
- [FAQ](examples/08_mini_project_solution/faq.csv)
- [평가 질의](examples/08_mini_project_solution/evaluation.csv)

