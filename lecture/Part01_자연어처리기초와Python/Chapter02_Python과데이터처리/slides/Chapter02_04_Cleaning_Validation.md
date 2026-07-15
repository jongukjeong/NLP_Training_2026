---
marp: true
theme: nlp-training
paginate: true
size: 16:9
title: Chapter 2-4. 텍스트 데이터 정제와 검증
description: NLP Training 2026 Chapter 2 Lecture 4
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Chapter 2-4
## 텍스트 데이터 정제와 검증

NLP Training 2026

---

# 이번 강의의 학습 목표

- 정제를 명시적인 규칙의 집합으로 설계한다
- 위에서 아래로 기본 정제 흐름을 완성한다
- 처리 전후 행 수를 비교한다
- 함수와 검증이 필요한 이유를 이해한다
- 개인정보와 의미 훼손 위험을 점검한다

---

# 정제는 ‘깨끗하게 만들기’가 아니다

```text
업무 목적 → 정제 규칙 → 처리 → 검증 → 기록
```

- 무엇을 삭제했는가?
- 어떤 값을 바꿨는가?
- 그 변화가 모델 목적에 적합한가?
- 같은 규칙을 다시 실행할 수 있는가?

---

# 정제 규칙을 먼저 선언한다

```text
1. 필수 열이 없으면 중단한다
2. text 결측 행은 제거한다
3. 앞뒤·연속 공백을 정리한다
4. 빈 문자열과 중복을 제거한다
5. 처리 건수를 보고서로 남긴다
```

규칙의 순서가 결과에 영향을 줄 수 있다

---

# 선택 확장: 스키마 검사

```python
required = {"id", "text", "label"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"필수 열 누락: {sorted(missing)}")
```

데이터 내용보다 먼저 **구조가 계약과 일치하는지** 확인한다

---

# 자료형과 값의 범위도 계약이다

| 열 | 기대 조건 |
|---|---|
| `id` | 고유하며 결측이 없음 |
| `text` | 문자열이며 정제 후 비어 있지 않음 |
| `label` | 허용된 범주 안의 값 |

열 이름만 맞아도 데이터가 올바르다는 뜻은 아니다

---

# 선택 확장: 정제 함수

```python
def clean_reviews(df):
    cleaned = df.copy()
    # 규칙 적용
    return cleaned
```

- 입력을 직접 변경하지 않는다
- 한 함수의 책임을 명확히 한다
- 반환값으로 다음 처리 단계를 연결한다

---

# 선택 확장: 표준화 함수

```python
def normalize_text(series):
    return (
        series.astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
```

반복되는 규칙을 함수로 만들면 테스트와 재사용이 쉬워진다

---

# 처리 순서를 코드에 드러낸다

```python
without_missing = df.dropna(subset=["text"]).copy()
normalized = without_missing.assign(
    text=normalize_text(without_missing["text"])
)
non_empty = normalized.loc[normalized["text"].ne("")].copy()
cleaned = non_empty.drop_duplicates(subset=["text"]).copy()
```

중간 단계 이름이 디버깅 지점이 된다

---

# 선택 확장: 처리 보고서

```python
report = {
    "input_rows": len(df),
    "missing_text": int(df["text"].isna().sum()),
    "output_rows": len(cleaned),
}
report["removed_rows"] = (
    report["input_rows"] - report["output_rows"]
)
```

결과 데이터와 처리 보고서를 함께 산출한다

---

# 무엇을 검증할 것인가

- 필수 열이 모두 존재하는가?
- ID는 고유하고 결측이 없는가?
- 텍스트는 문자열이며 비어 있지 않은가?
- 허용하지 않은 레이블이 남아 있는가?
- 정제 후 중복 텍스트가 남아 있는가?
- 출력 행 수가 입력 행 수보다 커지지 않았는가?

```python
assert required.issubset(cleaned.columns)
assert cleaned["id"].notna().all()
assert not cleaned.duplicated(subset=["text"]).any()
assert len(cleaned) <= len(df)
```

검증 실패는 조용히 넘어가지 않고 즉시 드러나야 한다

---

# 흔한 실수

| 실수 | 결과 |
|---|---|
| 모든 결측값을 같은 값으로 채움 | 열 의미 왜곡 |
| 정제 전에 중복 제거 | 표기 차이 중복을 놓침 |
| 긴 체인만 사용 | 행이 사라진 지점 추적 어려움 |
| 원본 파일에 저장 | 비교와 복구 불가능 |
| 검증 없이 저장 | 오류가 다음 단계로 전파 |

---

# 개인정보와 민감정보

- 이름·전화번호·이메일·주소가 포함됐는가?
- 주민등록번호나 계정 식별자가 있는가?
- 원문 공개가 필요한가, 가명화할 수 있는가?
- 정제 결과와 로그에 민감정보가 남는가?
- 접근 권한과 보관 기간이 정해져 있는가?

**데이터를 읽을 수 있다고 사용해도 되는 것은 아니다**

---

# 완성된 처리 파이프라인

<div class="flow">입력 → 스키마 검사 → 정제 → 품질 검증 → 보고서 → 저장</div>

```text
reviews_raw.csv
      ↓ clean_reviews.py
reviews_clean.csv + cleaning_report.json
```

데이터와 함께 **처리 과정의 증거**를 남긴다

---

# Chapter 2 핵심 정리

- 경로와 인코딩을 명시해 파일을 안전하게 읽는다
- `pandas`로 구조·결측·분포를 먼저 탐색한다
- 기본 실습은 한 줄씩 실행하며 변화를 확인한다
- 함수·검증·CLI는 solution에서 선택적으로 확장한다
- 정제된 텍스트는 다음 Chapter의 전처리 입력이 된다
