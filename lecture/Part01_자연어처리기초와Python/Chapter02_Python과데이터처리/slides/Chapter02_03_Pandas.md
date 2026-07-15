---
marp: true
theme: nlp-training
paginate: true
size: 16:9
title: Chapter 2-3. pandas로 표 데이터 다루기
description: NLP Training 2026 Chapter 2 Lecture 3
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Chapter 2-3
## pandas로 표 데이터 다루기

NLP Training 2026

---

# 이번 강의의 학습 목표

- `DataFrame`의 행과 열 구조를 이해한다
- 데이터의 크기·자료형·분포를 탐색한다
- 한 줄씩 실행하며 중간 결과를 확인한다
- 결측값과 중복을 일관된 규칙으로 처리한다
- 정제 결과를 CSV로 저장한다

---

# DataFrame이란

| id | text | label |
|---:|---|---|
| 1 | 좋아요 | positive |
| 2 | 환불하고 싶어요 | negative |
| 3 | 결측 | unknown |

- 행: 하나의 관측 또는 문서
- 열: 관측의 속성
- 각 열은 고유한 자료형을 가진다

---

# DataFrame 만들기

```python
import pandas as pd

df = pd.DataFrame({
    "id": [1, 2, 3],
    "text": ["좋아요", " 환불하고 싶어요 ", None],
    "label": ["positive", "negative", "unknown"],
})
```

딕셔너리의 키가 열 이름, 리스트의 항목이 각 행의 값이 된다

---

# 전체 출력보다 구조를 먼저 본다

```python
print(df.head())
print(df.shape)
print(df.columns.tolist())
print(df.dtypes)
df.info()
```

- `head()`: 앞부분 표본
- `shape`: `(행 수, 열 수)`
- `columns`: 열 이름
- `dtypes`: 열별 자료형
- `info()`: non-null 개수와 메모리 사용량

---

# 범주 분포 확인

```python
counts = df["label"].value_counts(dropna=False)
print(counts)
```

- 예상하지 못한 레이블이 있는가?
- 특정 레이블이 지나치게 적거나 많은가?
- 결측 레이블도 분포에 포함했는가?

**분포는 정제 전후 모두 비교한다**

---

# 열 선택

```python
texts = df["text"]
subset = df[["id", "text"]]
```

- 대괄호 한 쌍: `Series` 하나
- 열 이름 리스트: 여러 열의 `DataFrame`
- 필요한 열만 선택하면 처리 의도가 선명해진다

---

# 조건으로 행 선택: `loc`

```python
negative = df.loc[
    df["label"] == "negative",
    ["id", "text"],
]
```

`loc[행 조건, 열 선택]`은 레이블과 조건에 기반한다

---

# 위치로 행 선택: `iloc`

```python
first_row = df.iloc[0]
first_two = df.iloc[:2, :2]
```

| 도구 | 선택 기준 |
|---|---|
| `loc` | 열·행 레이블과 논리 조건 |
| `iloc` | 0부터 시작하는 정수 위치 |

---

# 결측값 찾기

```python
missing_by_column = df.isna().sum()
print(missing_by_column)
```

결측값을 발견한 뒤 업무 의미에 따라 결정한다:

- 제거한다
- 기본값으로 채운다
- 별도 범주로 보존한다

---

# 결측값 처리

```python
valid = df.dropna(subset=["text"]).copy()
valid["label"] = valid["label"].fillna("unknown")
```

- 텍스트 결측은 학습 입력이 될 수 없어 제거
- 레이블 결측은 목적에 따라 `unknown`으로 보존 가능
- 처리 기준은 열마다 다를 수 있다

---

# 문자열 열 정제

```python
valid["text"] = valid["text"].astype("string")
valid["text"] = valid["text"].str.strip()
valid["text"] = valid["text"].str.replace(r"\s+", " ", regex=True)
valid = valid[valid["text"] != ""]
```

한 줄마다 `print(valid)`로 변화를 확인한다

---

# 중복은 기준부터 정의한다

```python
duplicate_count = valid.duplicated(subset=["text"]).sum()
deduplicated = valid.drop_duplicates(
    subset=["text"], keep="first"
).copy()
```

ID가 달라도 정제된 텍스트가 같다면 중복인가?

> 코드보다 먼저 업무 규칙이 필요하다

---

# 선택 확장: 그룹 집계

```python
summary = (
    deduplicated.groupby("label", dropna=False)
    .agg(
        count=("id", "count"),
        avg_length=("text_length", "mean"),
    )
    .sort_values("count", ascending=False)
)
```

레이블별 문서 수와 평균 길이를 한 표로 확인한다

---

# 핵심 정리

- `shape`, `dtypes`, `info()`로 구조를 먼저 확인한다
- `loc`은 조건, `iloc`은 정수 위치로 선택한다
- 결측과 중복은 열의 의미에 따라 처리한다
- 정제 전후 행 수와 범주 분포를 비교한다
- 함수화와 집계는 기본 코드를 이해한 뒤 확장한다
