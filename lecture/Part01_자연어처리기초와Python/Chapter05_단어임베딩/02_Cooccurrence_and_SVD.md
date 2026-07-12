# 02. 동시출현과 SVD

## 문맥 창

기준 단어 주변의 일정 범위를 문맥 창이라고 합니다.

```text
배송이 매우 빠르게 도착했다
          ↑ 기준 단어: 빠르게
창 크기 2: 배송이, 매우, 도착했다
```

창이 작으면 문법적·국소 관계를, 크면 주제적 관계를 더 많이 반영하는 경향이 있습니다.

## 동시출현 행렬

행은 기준 단어, 열은 문맥 단어이며 함께 등장한 횟수를 기록합니다. 원시 빈도는 고빈도 단어에 지배될 수 있어 PPMI 같은 가중치를 적용하기도 합니다.

## SVD 차원 축소

```python
from sklearn.decomposition import TruncatedSVD

svd = TruncatedSVD(n_components=20, random_state=42)
embeddings = svd.fit_transform(cooccurrence_matrix)
```

`TruncatedSVD`는 희소 행렬을 직접 다룰 수 있습니다. 차원 수는 어휘 크기보다 작아야 하며 데이터가 매우 작으면 안정적인 의미 관계를 학습할 수 없습니다.

## 재현성

- 토큰화·정규화 설정 고정
- 문맥 창과 최소 빈도 기록
- 무작위 시드 고정
- 어휘와 단어-인덱스 매핑 저장
- 데이터 버전과 학습 시점 기록

> 다음: [Word2Vec과 사전학습 임베딩](03_Word2Vec_and_Pretrained.md)
