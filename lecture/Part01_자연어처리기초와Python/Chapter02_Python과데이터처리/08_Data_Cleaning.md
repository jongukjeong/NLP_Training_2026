# 08. 텍스트 데이터 정제와 검증

## 기본 실습: 위에서 아래로 정제하기

처음에는 함수나 타입 힌트 없이 각 줄의 결과를 확인합니다.

```python
import pandas as pd

df = pd.read_csv("reviews.csv", encoding="utf-8-sig")
rows_before = len(df)

df = df.dropna(subset=["text"])
df["text"] = df["text"].str.strip()
df["text"] = df["text"].str.replace(r"\s+", " ", regex=True)
df = df[df["text"] != ""]
df["label"] = df["label"].fillna("unknown")
df["label"] = df["label"].str.lower()
df = df.drop_duplicates(subset=["text"])

print("처리 전:", rows_before)
print("처리 후:", len(df))
df.to_csv("reviews_clean.csv", index=False, encoding="utf-8-sig")
```

이 흐름을 이해한 학습자는 아래의 함수화와 검증으로 확장합니다.

## 정제는 규칙의 집합이다

“깨끗하게 만든다”는 표현만으로는 재현할 수 없습니다. 입력, 규칙, 출력, 제외 건수와 예외를 명시해야 합니다.

이 장에서는 다음 순서를 사용합니다.

1. 필수 열 확인
2. 결측 문장 제거
3. 문자열 형식 통일
4. 빈 문장 제거
5. 허용 레이블 검사
6. 중복 제거
7. 파생 변수 생성
8. 처리 전후 통계 기록

## 선택 확장: 스키마 검사

```python
import pandas as pd

REQUIRED_COLUMNS = {"id", "text", "label"}

def validate_columns(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"필수 열이 없습니다: {names}")
```

## 선택 확장: 정제 함수

```python
ALLOWED_LABELS = {"positive", "negative", "neutral", "unknown"}

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df)
    result = df.copy()

    result = result.dropna(subset=["text"])
    result["text"] = (
        result["text"]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    result = result.loc[result["text"].str.len() > 0]

    result["label"] = result["label"].fillna("unknown").str.lower().str.strip()
    invalid = sorted(set(result["label"]) - ALLOWED_LABELS)
    if invalid:
        raise ValueError(f"허용되지 않은 레이블: {invalid}")

    result = result.drop_duplicates(subset=["text"], keep="first")
    result["text_length"] = result["text"].str.len()
    return result.reset_index(drop=True)
```

## 선택 확장: 처리 보고서

```python
def build_report(before: pd.DataFrame, after: pd.DataFrame) -> dict:
    return {
        "rows_before": len(before),
        "rows_after": len(after),
        "rows_removed": len(before) - len(after),
        "missing_text_before": int(before["text"].isna().sum()),
        "duplicate_text_after": int(after.duplicated(subset=["text"]).sum()),
        "labels": after["label"].value_counts().to_dict(),
    }
```

## 선택 확장: 검증 항목

```python
cleaned = clean_dataframe(df)

assert cleaned["text"].notna().all()
assert cleaned["text"].str.len().gt(0).all()
assert cleaned["text"].is_unique
assert set(cleaned["label"]) <= ALLOWED_LABELS
assert cleaned["text_length"].ge(1).all()
```

## 흔한 실수

| 실수 | 문제 | 개선 |
|---|---|---|
| 원본 파일 덮어쓰기 | 복구·비교 어려움 | 출력 경로 분리 |
| 모든 결측값을 빈 문자열로 치환 | 결측 의미 손실 | 열별 정책 정의 |
| 정제 전에 중복 제거 | 공백 차이 중복을 놓침 | 정규화 후 중복 제거 |
| 전체 예외 무시 | 손상된 결과를 정상처럼 저장 | 예상 오류만 처리 |
| 처리 건수 미기록 | 데이터 손실 원인 추적 불가 | 전후 통계 저장 |

## 개인정보와 민감정보

실제 고객 문장에는 이름, 전화번호, 이메일, 주소가 포함될 수 있습니다. 교육·분석 환경으로 옮기기 전에 조직의 정책에 따라 비식별화하고 접근 권한과 보존 기간을 확인해야 합니다. 샘플 출력과 오류 로그에도 원문 전체가 노출되지 않도록 주의합니다.
