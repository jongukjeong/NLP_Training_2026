# 07. pandas로 표 데이터 다루기

## DataFrame 만들기

```python
import pandas as pd

df = pd.DataFrame(
    {
        "id": [1, 2, 3],
        "text": ["좋아요", " 환불하고 싶어요 ", None],
        "label": ["positive", "negative", "unknown"],
    }
)
```

## 구조 탐색

```python
print(df.head())
print(df.shape)
print(df.columns.tolist())
print(df.dtypes)
print(df.info())
print(df["label"].value_counts(dropna=False))
```

처음부터 전체 데이터를 출력하기보다 행 수, 열 이름, 자료형, 결측값, 범주 분포를 먼저 확인합니다.

## 선택과 필터링

```python
texts = df["text"]
subset = df[["id", "text"]]
negative = df.loc[df["label"] == "negative", ["id", "text"]]
first_row = df.iloc[0]
```

- `loc`: 레이블과 조건 기반
- `iloc`: 정수 위치 기반

## 결측값

```python
print(df.isna().sum())
valid = df.dropna(subset=["text"]).copy()
valid["label"] = valid["label"].fillna("unknown")
```

`inplace=True`에 의존하기보다 결과를 새 변수에 할당하면 처리 단계를 추적하기 쉽습니다.

## 문자열 정제

```python
valid["text"] = (
    valid["text"]
    .astype("string")
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)
valid = valid.loc[valid["text"].str.len() > 0].copy()
valid["text_length"] = valid["text"].str.len()
```

## 중복 제거

```python
duplicate_count = valid.duplicated(subset=["text"]).sum()
deduplicated = valid.drop_duplicates(subset=["text"], keep="first").copy()
```

무엇을 중복으로 볼지 먼저 정의해야 합니다. `id`가 달라도 정제된 `text`가 같으면 중복으로 볼 것인지 업무 규칙이 필요합니다.

## 그룹 집계

```python
summary = (
    deduplicated.groupby("label", dropna=False)
    .agg(
        count=("id", "count"),
        avg_length=("text_length", "mean"),
    )
    .sort_values("count", ascending=False)
)
print(summary)
```

## 파일 입출력

```python
df = pd.read_csv("reviews.csv", encoding="utf-8-sig")
df.to_csv("reviews_clean.csv", index=False, encoding="utf-8-sig")

json_df = pd.read_json("reviews.json")
json_df.to_json(
    "reviews_clean.json",
    orient="records",
    force_ascii=False,
    indent=2,
)
```

## 체인보다 단계 이름 붙이기

긴 메서드 체인은 편리하지만 교육과 디버깅에서는 중간 결과를 나누는 편이 좋습니다.

```python
without_missing = df.dropna(subset=["text"]).copy()
normalized = without_missing.assign(text=without_missing["text"].str.strip())
non_empty = normalized.loc[normalized["text"].ne("")].copy()
```

각 단계의 `shape`를 확인하면 어느 규칙에서 행이 사라졌는지 알 수 있습니다.
