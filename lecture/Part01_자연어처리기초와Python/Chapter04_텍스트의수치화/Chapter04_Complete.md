# Chapter 4 통합 강의 원고

---

<!-- SOURCE: README.md -->

# Chapter 4. 텍스트의 수치화


## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **단어 주머니(Bag of Words, BoW): 단어 순서보다 등장 횟수로 문서를 표현하는 방법**
- **단어 빈도-역문서 빈도(Term Frequency-Inverse Document Frequency, TF-IDF): 문서를 구분하는 단어에 더 큰 값을 주는 방법**
- **희소 행렬(Sparse Matrix): 값 대부분이 0인 행렬을 효율적으로 저장한 구조**
- **코사인 유사도(Cosine Similarity): 두 벡터 방향의 유사성을 측정하는 값**

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

<!-- SOURCE: 00_TFIDF_검색실습과_평가.md -->

# Chapter 4 TF-IDF 검색 실습과 평가

## 작은 검색기를 만드는 전체 과정

```text
문서 읽기 → 전처리 → TF-IDF 학습 → 문서 행렬
질문 전처리 → 같은 TF-IDF 변환 → cosine → 순위
```

질문에 별도 vocabulary를 만들지 않는 것이 핵심입니다.

## 최소 코드

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = [
    "배송은 영업일 기준 3일 걸립니다",
    "환불은 결제 취소 후 처리됩니다",
    "비밀번호는 계정 설정에서 변경합니다",
]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
doc_matrix = vectorizer.fit_transform(docs)

query = "배송 기간은 며칠인가요"
query_vector = vectorizer.transform([query])
scores = cosine_similarity(query_vector, doc_matrix)[0]
print(scores)
```

결과는 문서 3개에 대한 유사도 배열입니다. 가장 큰 값의 인덱스가 첫 검색 결과입니다.

## 행렬 shape

문서가 3개이고 학습된 특징이 25개면 `doc_matrix.shape==(3,25)`, 질문은 `(1,25)`입니다. 같은 열 25개를 사용하므로 cosine을 계산할 수 있습니다.

## Vocabulary 확인

```python
feature_names = vectorizer.get_feature_names_out()
print(feature_names[:20])
```

예상한 제품명과 bigram이 있는지 확인합니다. 전처리 때문에 중요한 코드가 사라졌다면 검색 전에 수정합니다.

## Top-k 반환

```python
import numpy as np

top_k = 2
indices = np.argsort(scores)[::-1][:top_k]
for rank, index in enumerate(indices, 1):
    print(rank, float(scores[index]), docs[index])
```

점수는 모델과 데이터에 따라 달라 절대적인 정답 확률로 해석하지 않습니다.

## 평가 데이터

| 질문 | 정답 문서 ID |
|---|---|
| 배송에 며칠 걸려요? | d001 |
| 암호를 바꾸고 싶어요 | d003 |
| 결제 취소 절차는? | d002 |

표현이 문서와 완전히 같은 질문만 사용하면 실제 검색 난이도를 과소평가합니다.

## Hit@k

10개 질문 중 1위에 정답이 7개면 Hit@1=0.7입니다. top-3에 9개면 Hit@3=0.9입니다. 서비스가 사용자에게 결과 세 개를 보여준다면 Hit@3이 중요할 수 있습니다.

## MRR

첫 정답 순위가 1, 2, 2, 4라면:

\[
MRR=(1+0.5+0.5+0.25)/4=0.5625
\]

정답이 앞에 나올수록 높은 점수를 받습니다.

## N-gram 비교

| 설정 | 장점 | 비용 |
|---|---|---|
| `(1,1)` | 단순, 작은 행렬 | 구 표현 손실 |
| `(1,2)` | `결제 취소` 보존 | 특징 수 증가 |
| `(1,3)` | 긴 구 보존 | 희소성과 메모리 증가 |

동일 평가셋에서 Hit와 행렬 크기, 검색시간을 기록합니다.

## min_df와 max_df

`min_df`는 너무 드문 특징, `max_df`는 지나치게 흔한 특징을 제한합니다. 제품 코드는 드물지만 중요하므로 높은 `min_df`가 검색을 망칠 수 있습니다.

## 오류 분석

- 동의어: “암호”와 “비밀번호”가 다른 단어
- 고유명사: 제품 코드가 정제됨
- 짧은 질문: 단서가 한 단어뿐
- 긴 문서: 관련 부분이 다른 내용에 묻힘
- 중복 문서: 거의 같은 결과가 상위를 차지

TF-IDF의 동의어 한계는 임베딩 검색 또는 동의어 사전과 비교할 수 있습니다.

## 모델 저장

```python
import joblib
joblib.dump(vectorizer, "tfidf.joblib")
```

서비스에서 다시 fit하지 않고 저장한 vectorizer를 불러옵니다. 학습 문서 버전과 vectorizer 버전을 함께 관리합니다.

## 완료 기준

1. 문서 ID와 원문 보존
2. 같은 전처리와 vectorizer 재사용
3. Hit@1·Hit@3·MRR 계산
4. 오류 질문 원문 분석
5. 행렬 shape와 메모리 확인
6. 저장 후 재로딩 검색 결과 확인

---

<!-- SOURCE: 00_쉬운_수치화_원리와계산.md -->

# Chapter 4 쉬운 텍스트 수치화 원리와 계산

## 왜 문장을 숫자로 바꾸는가

컴퓨터 모델은 `배송이 늦어요`라는 글자를 사람처럼 직접 이해하지 못합니다. 대신 단어가 몇 번 나왔는지, 어떤 문서에서 드문지, 두 문장이 얼마나 비슷한지 같은 숫자를 계산합니다.

수치화는 의미를 완벽히 보존하는 과정이 아니라 모델이 계산할 수 있는 특징을 선택하는 과정입니다.

## 문서-단어 행렬

세 문서를 생각해 봅시다.

```text
D1: 배송 빠름
D2: 배송 느림
D3: 환불 느림
```

어휘 순서를 `[배송, 빠름, 느림, 환불]`로 정하면 Bag of Words 행렬은 다음과 같습니다.

\[
X=\begin{bmatrix}
1&1&0&0\\
1&0&1&0\\
0&0&1&1
\end{bmatrix}
\]

행은 문서, 열은 단어입니다. `X[1,2]=1`은 두 번째 문서에 `느림`이 한 번 있다는 뜻입니다.

## Bag of Words가 잃는 것

`고양이가 개를 물었다`와 `개가 고양이를 물었다`는 단어 빈도가 거의 같습니다. BoW는 순서를 잃기 때문에 두 문장을 비슷하게 표현합니다. 분류에서는 핵심 단어만으로 충분할 수 있지만 번역과 생성에는 한계가 큽니다.

## Binary, Count, 빈도 정규화

- Binary: 단어가 있으면 1, 없으면 0
- Count: 등장 횟수 기록
- Term Frequency: 문서 길이로 나눈 상대 빈도

\[
TF(t,d)=\frac{count(t,d)}{\sum_{w}count(w,d)}
\]

10단어 문서에서 `배송`이 2번이면 TF는 0.2입니다. 문서 길이가 다른 경우 단순 횟수보다 비교하기 쉽습니다.

## TF-IDF를 출석 희소성으로 이해하기

모든 문서에 나오는 단어는 주제를 구분하는 힘이 작습니다. 일부 문서에만 나오는 단어는 더 중요한 단서일 수 있습니다.

\[
TFIDF(t,d)=TF(t,d)\times IDF(t)
\]

\[
IDF(t)=\log\left(\frac{N}{df(t)}\right)
\]

`N`은 전체 문서 수, `df(t)`는 단어가 등장한 문서 수입니다. 문서 100개 중 100개에 등장하면 `log(1)=0`, 10개에만 등장하면 `log(10)≈2.303`입니다. 드문 단어의 IDF가 큽니다.

실제 scikit-learn은 0으로 나누는 문제를 피하고 새 문서에도 안정적으로 적용하기 위해 smoothing이 포함된 식을 사용합니다. 손계산과 라이브러리 결과가 조금 다른 이유입니다.

## N-gram

Unigram은 한 단어, bigram은 연속 두 단어입니다. `안 좋다`를 unigram으로 나누면 `안`, `좋다`지만 bigram은 `안 좋다`를 하나의 특징으로 보존할 수 있습니다.

N-gram 범위를 늘리면 표현력은 커지지만 어휘 수와 희소성이 빠르게 증가합니다. 데이터가 적을 때 긴 n-gram은 거의 한 번만 등장할 수 있습니다.

## 희소 행렬

문서 10,000개, 어휘 50,000개면 원소가 5억 개입니다. 대부분 0이므로 0이 아닌 위치와 값만 저장하는 sparse matrix를 사용합니다. 실습에서 `toarray()`로 전체를 변환하면 메모리가 부족할 수 있습니다.

## 코사인 유사도

두 문서 벡터가 같은 방향을 가리키는지 계산합니다.

\[
cos(A,B)=\frac{A\cdot B}{\|A\|\|B\|}
\]

`A=[1,1]`, `B=[2,2]`이면 방향이 같아 cosine은 1입니다. 길이는 다르지만 단어 비율이 같습니다. `C=[1,0]`과 `D=[0,1]`은 내적이 0이므로 유사도 0입니다.

## 직접 숫자로 계산하기

`A=[1,2]`, `B=[2,1]`일 때 내적은 `1×2+2×1=4`입니다. 두 norm은 모두 `√5`이므로 cosine은 `4/5=0.8`입니다.

## 검색의 데이터 흐름

```text
문서 모음 → 동일 전처리 → TF-IDF fit_transform → 문서 행렬 저장
질문 → 같은 vectorizer transform → cosine 계산 → 상위 k개 반환
```

질문에 새 vectorizer를 다시 fit하면 문서와 열의 의미가 달라져 비교할 수 없습니다. 학습한 vectorizer를 저장해 재사용합니다.

## 평가

검색 결과 첫 k개 안에 정답이 있는지를 Hit@k 또는 Recall@k로 볼 수 있습니다.

\[
Hit@k=\frac{정답이상위k개에있는질문수}{전체질문수}
\]

질문 20개 중 17개가 top-3에 정답을 포함하면 Hit@3은 0.85입니다.

## 실무 오류

- train과 test를 합쳐 vectorizer를 fit해 어휘 정보 누수
- 숫자·제품 코드를 제거해 검색 정확도 하락
- `min_df`가 너무 커 희귀하지만 중요한 단어 제거
- `max_features`가 너무 작아 도메인 어휘 누락
- dense 변환으로 메모리 급증
- 같은 문서의 중복본이 평가셋에 포함

## 확인 문제

1. BoW가 단어 순서를 잃는다는 뜻은?
2. 문서 1,000개 중 10개에 나온 단어의 IDF가 큰 이유는?
3. `[1,0]`과 `[0,1]`의 cosine은?
4. 질문용 vectorizer를 새로 fit하면 안 되는 이유는?
5. N-gram을 늘릴 때 생기는 비용은?

---

<!-- SOURCE: 01_Bag_of_Words.md -->

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

## Binary와 Count 표현

Binary 방식은 단어가 한 번이라도 나오면 1, Count 방식은 실제 등장 횟수를 기록합니다. 스팸 문구처럼 반복 횟수가 중요하면 Count가 유용하고, 긴 문서가 단순히 더 큰 값을 갖는 문제를 줄이려면 Binary를 비교할 수 있습니다.

```python
binary_vectorizer = CountVectorizer(binary=True)
count_vectorizer = CountVectorizer(binary=False)
```

문장 `배송 배송 지연`은 어휘 `[배송, 지연]`에서 Binary `[1,1]`, Count `[2,1]`입니다.

## 행렬 shape 해석

문서 1,000개와 어휘 5,000개가 있으면 행렬 shape는 `(1000,5000)`입니다. 행은 문서, 열은 단어입니다. 새 문서를 `transform()`하면 `(새 문서 수,5000)`으로 같은 열을 사용합니다.

## 메모리 확인

```python
print(matrix.shape)
print("0이 아닌 원소:", matrix.nnz)
sparsity = 1 - matrix.nnz / (matrix.shape[0] * matrix.shape[1])
print("희소도:", sparsity)
```

희소도가 0.99라면 원소의 99%가 0입니다. 이 때문에 희소 행렬을 사용합니다.

## 어휘 누수와 미등록 단어

평가 문서까지 포함해 `fit()`하면 미래 어휘를 미리 알게 됩니다. Train에서 fit하고 validation/test에는 transform만 적용합니다. 학습 어휘에 없는 새 단어는 해당 열이 없으므로 벡터에 반영되지 않습니다.

## BoW가 적합한 경우

- 카테고리별 핵심 단어가 뚜렷한 문서 분류
- 제품 코드와 정확한 용어 중심 검색
- 빠르고 설명 가능한 기준선

번역·문장 생성처럼 순서가 핵심인 과제에는 적합하지 않습니다.

---

<!-- SOURCE: 02_TFIDF_and_Ngrams.md -->

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

## TF와 IDF 공식

\[
TF(t,d)=\frac{count(t,d)}{문서d의전체단어수}
\]

\[
IDF(t)=\log\frac{전체문서수}{단어t가등장한문서수}
\]

100개 문서 중 5개에만 등장한 단어의 IDF는 `log(20)≈2.996`입니다. 100개 모두에 등장하면 `log(1)=0`입니다. 라이브러리는 smoothing 때문에 손계산과 조금 다를 수 있습니다.

## sublinear_tf

`sublinear_tf=True`는 등장 횟수를 그대로 쓰지 않고 `1+log(count)`로 완화합니다. 한 문서에서 어떤 단어가 20번 나왔다고 1번 나온 단어보다 정확히 20배 중요하다고 보기 어려울 때 유용합니다.

## L2 정규화


orm="l2"`는 각 문서 벡터의 길이를 1로 맞춥니다. 긴 문서가 단어 수 때문에 무조건 큰 값을 갖는 현상을 줄이고 cosine 계산을 편리하게 합니다.

## 단어와 문자 n-gram 비교

| 데이터 | 권장 후보 | 이유 |
|---|---|---|
| 정제된 뉴스 | word `(1,2)` | 단어 의미와 구 보존 |
| 오타 많은 문의 | char `(2,5)` | 철자·띄어쓰기 변화 대응 |
| 제품 코드 | word+char 비교 | 정확한 문자열 보존 |

특징 수, Hit@k, 메모리와 검색시간을 같은 평가셋에서 비교합니다.

## 지나친 n-gram

긴 n-gram은 학습 문장 전체를 외우는 특징이 될 수 있습니다. Train 성능은 높지만 새 표현에서 실패할 수 있으므로 validation 결과와 `matrix.shape[1]`을 함께 봅니다.

---

<!-- SOURCE: 03_Similarity_and_Search.md -->

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

## 코사인 공식과 손계산

\[
cos(A,B)=\frac{A\cdot B}{\|A\|\|B\|}
\]

`A=[1,2]`, `B=[2,1]`이면 내적은 4, 두 벡터 길이는 각각 `√5`이므로 cosine은 `4/5=0.8`입니다.

## Top-k 검색 함수

```python
import numpy as np

def search(query, vectorizer, document_matrix, documents, k=3):
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, document_matrix).ravel()
    if query_vector.nnz == 0:
        return []
    indices = np.argsort(scores)[::-1][:k]
    return [(documents[i], float(scores[i])) for i in indices]
```

0 벡터를 별도로 처리하지 않으면 관련 없는 첫 문서를 결과처럼 보여줄 수 있습니다.

## 임계값

Top-1을 무조건 반환하기보다 validation 질문에서 최소 점수를 정할 수 있습니다. 점수가 낮으면 “관련 문서를 찾지 못했습니다”를 반환합니다. 점수는 정답 확률이 아니므로 업무 데이터로 임계값을 정합니다.

## 중복 결과

거의 같은 문서가 top-k를 채우면 사용자에게 다양한 정보를 주지 못합니다. 문서 중복 제거, 문서 그룹별 하나만 선택, MMR 같은 다양성 검색을 검토합니다.

## 검색 로그

질문, 문서 ID, rank, score, vectorizer 버전과 사용자 선택 여부를 기록합니다. 개인정보가 포함된 질문은 마스킹과 보존 기간을 적용합니다.

---

<!-- SOURCE: 04_Evaluation.md -->

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

## Hit@k 손계산

질문 10개 중 정답 문서가 top-1에 6개, top-3에 9개 있으면 Hit@1은 0.6, Hit@3은 0.9입니다. 화면에 세 결과를 보여주는 검색 서비스라면 Hit@3이 실제 경험과 관련될 수 있습니다.

## MRR 손계산

첫 정답 순위가 1, 2, 4라면:

\[
MRR=(1+1/2+1/4)/3\approx0.583
\]

정답을 찾는 것뿐 아니라 앞 순위에 배치하는 능력을 평가합니다.

## 평가셋 구성

- 문서 표현과 같은 쉬운 질문
- 동의어를 사용한 질문
- 오타와 띄어쓰기 오류
- 제품 코드·숫자 포함
- 정답 문서가 없는 질문
- 여러 관련 문서가 있는 질문

정답이 없는 질문을 포함해야 무조건 결과를 반환하는 오류를 평가할 수 있습니다.

## 실패 분류

어휘에 없는 표현, 전처리 손실, 동점, 중복 문서, 너무 긴 문서, 잘못된 정답 라벨로 나눕니다. 실패 유형별 건수를 세면 다음 개선 방향이 명확해집니다.

## 배포 전 확인

저장한 vectorizer를 새 프로세스에서 불러와 같은 질문의 top-k가 같은지 확인합니다. 전처리 함수와 문서 순서도 같은 버전이어야 합니다.

---

<!-- SOURCE: 05_Summary.md -->

# 다음 Chapter로 연결하기

다음 Chapter에서는 단어를 밀집 벡터로 표현해 의미적 유사성을 다룹니다.

---

<!-- SOURCE: 06_Quiz.md -->

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

---

<!-- SOURCE: 07_Assignment.md -->

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

---

<!-- SOURCE: 08_Mini_Project.md -->

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
