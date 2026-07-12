# Chapter 2. Python과 데이터 처리 — 통합 원고

> 이 문서는 Chapter 2. Python과 데이터 처리 의 최상위 강의 마크다운을 학습 순서대로 합친 통합 원고입니다. 개별 원본 파일은 그대로 유지합니다.

## 통합 목차

- Chapter 2. Python과 데이터 처리 — `README.md`
- 01. 학습 안내 — `01_Opening.md`
- 06. 파일·CSV·JSON 처리 — `06_File_IO.md`
- 07. pandas로 표 데이터 다루기 — `07_Pandas.md`
- 08. 텍스트 데이터 정제와 검증 — `08_Data_Cleaning.md`
- 09. 핵심 정리 — `09_Summary.md`
- 10. 퀴즈 — `10_Quiz.md`
- 11. 실습 과제 — `11_Assignment.md`
- 12. 미니 프로젝트: 텍스트 데이터 탐색기 — `12_Mini_Project.md`

---

<!-- SOURCE: README.md -->

# Chapter 2. Python과 데이터 처리

# Chapter 2. Python과 데이터 처리

자연어 처리에서는 모델 학습 전에 **데이터를 읽고, 구조를 진단하고, 정제하고, 검증하여 다시 저장하는 과정**이 필요합니다. 이 장은 Python 기본 문법을 이미 알고 있다는 전제에서 실제 텍스트 데이터 처리에 집중합니다.

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다.

- 텍스트, CSV, JSON 파일을 UTF-8로 안전하게 읽고 쓴다.
- pandas로 표 데이터를 탐색하고 결측값·중복·문자열을 정제한다.
- 데이터 스키마와 정제 결과를 검증한다.
- 처리 전후 통계를 기록하는 작은 데이터 처리 프로그램을 완성한다.

## 선수 지식

변수, 기본 자료형, 조건문, 반복문, 함수 등 Python 기본 문법은 이 장에서 별도로 설명하지 않습니다. 필요한 코드는 데이터 처리 맥락의 완성 예제로 제공합니다.

## 권장 학습 시간

| 구분 | 시간 |
|---|---:|
| 개념 학습 | 4시간 |
| 따라 하기 | 4시간 |
| 퀴즈·과제 | 2시간 |
| 미니 프로젝트 | 3시간 |

## 문서 구성

1. [학습 안내](01_Opening.md)
2. [파일·CSV·JSON 처리](06_File_IO.md)
3. [pandas로 표 데이터 다루기](07_Pandas.md)
4. [텍스트 데이터 정제와 검증](08_Data_Cleaning.md)
5. [핵심 정리](09_Summary.md)
6. [퀴즈](10_Quiz.md)
7. [실습 과제](11_Assignment.md)
8. [미니 프로젝트: 텍스트 데이터 탐색기](12_Mini_Project.md)

## 실습 환경

- Python 3.11.x
- VS Code 또는 JupyterLab
- pandas 2.x
- 모든 텍스트 파일의 기본 인코딩: UTF-8

## 예제 파일 배치 규칙

각 예제의 Python 코드와 그 코드가 사용하는 데이터셋은 **동일한 예제 폴더**에 둡니다.

```text
Chapter02_Python과데이터처리/
├── 11_Assignment.md
├── 12_Mini_Project.md
└── examples/
    ├── 11_assignment_solution/
    │   ├── assignment_solution.py
    │   └── customer_inquiries.csv
    └── 12_mini_project_solution/
        ├── text_data_explorer.py
        └── reviews.csv
```

실행 결과는 원본과 섞이지 않도록 같은 폴더 아래 `output/`에 저장합니다.

> 예제는 Windows PowerShell 기준 명령도 함께 제시하지만, Python 코드는 운영체제와 무관하게 실행되도록 작성합니다.

## 완료 기준

- 퀴즈 8문항 중 6문항 이상 정답
- 실습 과제의 필수 항목 완료
- 미니 프로젝트가 정상 데이터와 잘못된 입력 모두를 처리
- 출력 결과에 원본 행 수, 정제 행 수, 결측·중복 제거 수가 기록됨

다음 장에서는 이 장에서 준비한 텍스트 데이터를 바탕으로 정규표현식과 형태소 분석 등 본격적인 텍스트 전처리를 학습합니다.


---

<!-- SOURCE: 01_Opening.md -->

# 01. 학습 안내

# 01. 학습 안내

## 왜 NLP 전에 Python 데이터 처리를 배우는가

모델에 문장을 넣기 전에는 데이터 수집, 인코딩 확인, 결측값 처리, 중복 제거, 형식 통일이 필요합니다. 모델의 성능 문제처럼 보이는 현상도 실제로는 데이터 처리 오류인 경우가 많습니다.

```text
원본 파일 → 읽기 → 구조 확인 → 정제 → 검증 → 저장 → NLP 모델
```

이 장에서는 다음 예제 데이터를 계속 사용합니다.

```python
records = [
    {"id": 1, "text": "배송이 빨라요", "label": "positive"},
    {"id": 2, "text": "  환불하고 싶어요  ", "label": "negative"},
    {"id": 3, "text": None, "label": "unknown"},
]
```

## 먼저 확인하기

다음 질문에 답해 봅시다.

1. CSV와 JSON은 어떤 데이터 구조에 각각 적합할까요?
2. 텍스트 열의 결측값과 공백 문자열을 어떻게 구분할까요?
3. 정규화와 중복 제거는 어떤 순서로 수행해야 할까요?
4. 데이터 정제 후 행 수가 줄었다면 무엇을 기록해야 할까요?

## 학습 원칙

### 1. 작은 데이터로 먼저 확인한다

전체 파일을 처리하기 전에 3~10개 행으로 입출력과 정제 규칙을 검증합니다.

### 2. 원본을 덮어쓰지 않는다

`raw`, `processed`처럼 입력과 출력을 분리합니다. 정제 규칙이 잘못되어도 원본에서 다시 시작할 수 있어야 합니다.

### 3. 결과뿐 아니라 근거를 남긴다

처리 전후 행 수, 결측값 수, 중복 수, 사용한 인코딩과 규칙을 기록합니다.

### 4. 오류를 숨기지 않는다

무조건 `except: pass`로 넘기지 말고, 예상 가능한 오류만 처리하며 사용자가 고칠 수 있는 메시지를 제공합니다.

## 준비 확인

PowerShell에서 다음을 실행합니다.

```powershell
python --version
python -c "import sys; print(sys.executable)"
python -m pip show pandas
```

Python 3.11.x가 표시되고 pandas 정보가 출력되면 준비가 끝났습니다. 설치가 필요하면 활성화된 가상환경에서 다음을 실행합니다.

```powershell
python -m pip install pandas
```

## 이번 장의 결과물

마지막에는 CSV 또는 JSON을 읽어 텍스트를 정제하고, 기초 통계를 화면과 파일로 출력하는 프로그램의 설계와 완성 예제를 구현합니다.

예제 코드는 해당 데이터셋과 같은 폴더에 배치합니다. 따라서 예제 폴더만 복사해도 코드와 입력 데이터를 함께 실행할 수 있습니다. 생성 결과는 예제 폴더의 `output` 하위 폴더로 분리합니다.

> 다음: [파일·CSV·JSON 처리](06_File_IO.md)


---

<!-- SOURCE: 06_File_IO.md -->

# 06. 파일·CSV·JSON 처리

# 06. 파일·CSV·JSON 처리

## pathlib로 경로 다루기

문자열 이어 붙이기보다 `pathlib.Path`를 사용하면 Windows와 다른 운영체제에서 같은 코드를 사용할 수 있습니다.

```python
from pathlib import Path

data_dir = Path("data")
input_path = data_dir / "raw" / "reviews.txt"
output_path = data_dir / "processed" / "reviews_clean.txt"
output_path.parent.mkdir(parents=True, exist_ok=True)
```

이 장의 예제 파일은 코드와 데이터셋을 같은 폴더에 둡니다. 코드 파일 위치를 기준으로 경로를 만들면 실행 위치가 달라져도 안정적입니다.

```python
BASE_DIR = Path(__file__).resolve().parent
input_path = BASE_DIR / "reviews.txt"
output_path = BASE_DIR / "output" / "reviews_clean.txt"
output_path.parent.mkdir(parents=True, exist_ok=True)
```

## 텍스트 파일

```python
from pathlib import Path

path = Path("reviews.txt")
text = path.read_text(encoding="utf-8")
lines = text.splitlines()

Path("reviews_clean.txt").write_text(
    "\n".join(line.strip() for line in lines if line.strip()),
    encoding="utf-8",
)
```

큰 파일은 줄 단위로 처리합니다.

```python
with path.open("r", encoding="utf-8") as file:
    for line in file:
        cleaned = line.strip()
        if cleaned:
            print(cleaned)
```

## CSV

CSV에는 쉼표가 포함된 필드와 따옴표 규칙이 있으므로 `csv` 모듈을 사용합니다.

```python
import csv
from pathlib import Path

records = []
with Path("reviews.csv").open("r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        records.append(row)
```

Windows Excel에서 저장한 CSV는 BOM이 포함될 수 있어 입력 시 `utf-8-sig`가 편리합니다. 출력은 일반적으로 `utf-8-sig`를 사용하면 Excel 호환성이 좋아집니다.

```python
fieldnames = ["id", "text", "label"]
with Path("reviews_clean.csv").open(
    "w", encoding="utf-8-sig", newline=""
) as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)
```

## JSON

```python
import json
from pathlib import Path

data = json.loads(Path("reviews.json").read_text(encoding="utf-8"))

Path("reviews_clean.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
```

`ensure_ascii=False`는 한글을 `\uXXXX` 형태가 아닌 읽을 수 있는 문자로 저장합니다.

## 안전한 오류 메시지

```python
def read_utf8(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {path}") from error
    except UnicodeDecodeError as error:
        raise ValueError(f"UTF-8 파일이 아닙니다: {path}") from error
```

## 형식 선택

| 형식 | 적합한 데이터 | 장점 | 주의점 |
|---|---|---|---|
| TXT | 한 줄에 한 문장 | 단순함 | 열 구조 표현이 어려움 |
| CSV | 행과 열이 일정한 표 | Excel·pandas 호환 | 중첩 구조에 부적합 |
| JSON | 중첩된 레코드·메타데이터 | 구조 표현이 유연 | 큰 파일은 메모리 고려 |

> 다음: [pandas로 표 데이터 다루기](07_Pandas.md)


---

<!-- SOURCE: 07_Pandas.md -->

# 07. pandas로 표 데이터 다루기

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

> 다음: [텍스트 데이터 정제와 검증](08_Data_Cleaning.md)


---

<!-- SOURCE: 08_Data_Cleaning.md -->

# 08. 텍스트 데이터 정제와 검증

# 08. 텍스트 데이터 정제와 검증

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

## 스키마 검사

```python
import pandas as pd

REQUIRED_COLUMNS = {"id", "text", "label"}


def validate_columns(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        names = ", ".join(sorted(missing))
        raise ValueError(f"필수 열이 없습니다: {names}")
```

## 정제 함수

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

## 처리 보고서

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

## 검증 항목

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

> 다음: [핵심 정리](09_Summary.md)


---

<!-- SOURCE: 09_Summary.md -->

# 09. 핵심 정리

# 09. 핵심 정리

## 한눈에 보는 처리 흐름

```text
경로 확인
  ↓
UTF-8로 파일 읽기
  ↓
열·자료형·결측·분포 탐색
  ↓
문자열 정규화
  ↓
결측·빈 값·중복 처리
  ↓
규칙 검증과 통계 계산
  ↓
새 파일로 저장 + 처리 보고서
```

## 핵심 개념

| 주제 | 기억할 내용 |
|---|---|
| 경로 | `pathlib.Path`로 운영체제 독립적인 경로를 만든다. |
| 인코딩 | 한글 텍스트는 UTF-8을 명시한다. |
| CSV·JSON | 전용 파서로 읽고 쓴다. |
| pandas | 구조 탐색 후 복사·정제·집계한다. |
| 품질 | 처리 전후 건수와 검증 결과를 남긴다. |

## 스스로 설명해 보기

1. `None`과 빈 문자열은 왜 구분해야 하나요?
2. CSV를 `split(",")`로 처리하면 왜 위험한가요?
3. 정제 함수가 원본 DataFrame을 복사하는 이유는 무엇인가요?
4. 정규화 후 중복을 제거해야 하는 이유는 무엇인가요?
5. 처리 보고서에는 어떤 항목이 들어가야 하나요?

## 다음 장을 위한 체크리스트

- [ ] TXT, CSV, JSON을 UTF-8로 읽고 쓸 수 있다.
- [ ] pandas로 선택, 필터링, 결측 처리, 중복 제거를 할 수 있다.
- [ ] 정제 결과를 검증하고 처리 건수를 기록할 수 있다.

다음 장에서는 정규표현식, 토큰화, 불용어, 형태소 분석 등 언어 데이터에 특화된 전처리로 확장합니다.

> 다음: [퀴즈](10_Quiz.md)


---

<!-- SOURCE: 10_Quiz.md -->

# 10. 퀴즈

# 10. 퀴즈

먼저 답을 적은 뒤 하단의 해설을 확인하세요.

## 문제

### 1

Windows Excel에서 만든 UTF-8 CSV의 BOM까지 안전하게 처리할 때 적합한 입력 인코딩은 무엇인가요?

A. `ascii`  
B. `utf-8-sig`  
C. `utf-16-le`  
D. `latin-1`

### 2

JSON 저장 시 한글을 읽을 수 있는 문자로 유지하는 설정은 무엇인가요?

A. `ensure_ascii=False`  
B. `indent=None`  
C. `sort_keys=True`  
D. `encoding="ascii"`

### 3

pandas에서 데이터 구조를 처음 진단할 때 우선 확인할 조합으로 가장 적절한 것은 무엇인가요?

A. 화면 색상과 글꼴  
B. 행·열 수, 열 이름, 자료형, 결측값  
C. 파일 생성자 이름만  
D. 첫 번째 셀만

### 4

Windows와 macOS에서 모두 동작하는 경로 조합에 가장 적절한 도구는 무엇인가요?

A. 문자열 `+`  
B. `pathlib.Path`  
C. `print`  
D. `input`

### 5

쉼표가 포함될 수 있는 CSV 필드를 안전하게 읽는 방법은 무엇인가요?

A. 각 줄에 `split(",")` 적용  
B. 글자별 반복  
C. `csv` 모듈 또는 `pandas.read_csv` 사용  
D. 쉼표 모두 삭제

### 6

pandas에서 `text` 열이 결측인 행만 제거하는 코드는 무엇인가요?

A. `df.dropna()`  
B. `df.dropna(subset=["text"])`  
C. `df.drop("text")`  
D. `df.fillna("text")`

### 7

텍스트 중복 제거를 문자열 공백 정규화 뒤에 수행하는 주된 이유는 무엇인가요?

A. 파일 크기를 늘리기 위해  
B. 공백만 다른 동일 문장을 발견하기 위해  
C. 레이블을 삭제하기 위해  
D. 인코딩을 바꾸기 위해

### 8

정제 파이프라인에서 반드시 함께 남겨야 할 정보로 가장 적절한 것은 무엇인가요?

A. 출력 파일명만  
B. 개발자 이름만  
C. 처리 전후 행 수와 제외 사유별 건수  
D. 화면 색상

## 정답과 해설

1. **B** — `utf-8-sig`는 UTF-8 BOM이 있는 CSV와 없는 CSV를 모두 읽는 데 편리합니다.
2. **A** — `ensure_ascii=False`를 사용하면 한글이 유니코드 이스케이프로 변환되지 않습니다.
3. **B** — 구조와 품질을 먼저 확인해야 정제 규칙을 안전하게 결정할 수 있습니다.
4. **B** — `Path`와 `/` 연산자로 플랫폼 독립적인 경로를 조합합니다.
5. **C** — CSV의 인용·이스케이프 규칙은 전용 파서가 처리해야 합니다.
6. **B** — `subset`을 지정하면 해당 열의 결측만 제거 기준으로 사용합니다.
7. **B** — `"좋아요"`와 `" 좋아요 "`를 같은 문장으로 판단할 수 있습니다.
8. **C** — 전후 건수와 제외 사유가 있어야 데이터 손실을 추적할 수 있습니다.

## 성취 기준

- 7~8개: 핵심 개념을 잘 이해했습니다.
- 5~6개: 틀린 주제의 코드 예제를 다시 실행해 보세요.
- 0~4개: 02~08 문서를 순서대로 복습한 뒤 다시 풉니다.

> 다음: [실습 과제](11_Assignment.md)


---

<!-- SOURCE: 11_Assignment.md -->

# 11. 실습 과제

# 11. 실습 과제

## 과제: 고객 문의 데이터 정제

다음 원본 데이터를 Python과 pandas로 정제합니다.

```python
raw_records = [
    {"id": 1, "text": "  배송이 빨라요 ", "label": "Positive"},
    {"id": 2, "text": None, "label": "unknown"},
    {"id": 3, "text": "환불하고   싶어요", "label": "NEGATIVE"},
    {"id": 4, "text": "배송이 빨라요", "label": "positive"},
    {"id": 5, "text": "   ", "label": "neutral"},
]
```

## 필수 요구사항

1. DataFrame으로 변환합니다.
2. 원본 행 수와 열 이름을 출력합니다.
3. `text`가 `None`이거나 공백뿐인 행을 제거합니다.
4. 앞뒤 공백과 내부 연속 공백을 정리합니다.
5. `label`을 소문자로 통일합니다.
6. 정제된 `text` 기준 중복을 제거합니다.
7. `text_length` 열을 추가합니다.
8. 레이블별 문장 수를 계산합니다.
9. 결과를 `customer_inquiries_clean.csv`에 UTF-8 계열 인코딩으로 저장합니다.
10. 처리 전후 행 수와 제거 건수를 딕셔너리로 출력합니다.

## 추가 도전

- 허용 레이블 집합을 만들고 잘못된 레이블을 탐지합니다.
- 입력과 출력 경로를 `pathlib.Path`로 관리합니다.
- 정제 로직을 `clean_dataframe()` 함수로 분리합니다.
- 빈 DataFrame이 입력되어도 이해하기 쉬운 결과를 반환합니다.
- 결과 검증용 `assert`를 네 개 이상 작성합니다.

## 제출물

사용자가 “마크다운 문서만” 범위를 선택했으므로 이 저장소 단계에서는 실행 파일을 만들지 않습니다. 과제를 수행할 때는 다음을 별도 제출합니다.

- 작성한 Python 코드 또는 노트북
- 생성된 CSV
- 처리 결과 요약 5줄 이내
- 검증 결과

코드와 원본 데이터셋은 하나의 과제 폴더에 함께 두고, 생성된 CSV는 그 폴더의 `output/`에 저장합니다.

## 배포용 완성 답안

강의 시간이 부족할 때 바로 배포할 수 있는 실행 코드와 입력 데이터셋은 이 문서와 같은 Chapter 디렉터리 아래에 있습니다.

- [완성 답안 안내](examples/11_assignment_solution/README.md)
- [완성 답안 코드](examples/11_assignment_solution/assignment_solution.py)
- [입력 데이터셋](examples/11_assignment_solution/customer_inquiries.csv)

## 평가 기준

| 항목 | 배점 |
|---|---:|
| 필수 정제 규칙 구현 | 40 |
| 함수 구조와 가독성 | 20 |
| 파일 입출력·인코딩 | 15 |
| 처리 통계와 검증 | 15 |
| 추가 도전 | 10 |

## 자기 점검

- [ ] 원본 객체를 의도치 않게 변경하지 않았다.
- [ ] `None`에서 문자열 메서드를 호출하지 않는다.
- [ ] 정규화한 뒤 중복을 제거했다.
- [ ] CSV에 불필요한 인덱스 열이 저장되지 않는다.
- [ ] 처리 전후 건수가 논리적으로 맞는다.

> 다음: [미니 프로젝트](12_Mini_Project.md)


---

<!-- SOURCE: 12_Mini_Project.md -->

# 12. 미니 프로젝트: 텍스트 데이터 탐색기

# 12. 미니 프로젝트: 텍스트 데이터 탐색기

## 프로젝트 목표

CSV 파일을 읽어 품질을 진단하고 텍스트를 정제한 뒤, 정제 데이터와 처리 보고서를 저장하는 작은 프로그램을 설계합니다. 이 문서는 구현 명세와 완성 예제를 함께 제공합니다.

## 입력 명세

`reviews.csv`는 다음 열을 가집니다.

| 열 | 필수 | 설명 |
|---|---|---|
| `id` | 예 | 레코드 식별자 |
| `text` | 예 | 리뷰 문장 |
| `label` | 예 | `positive`, `negative`, `neutral`, `unknown` |

예시:

```csv
id,text,label
1,배송이 빨라요,positive
2,  환불하고 싶어요  ,negative
3,,unknown
4,배송이 빨라요,positive
```

## 권장 폴더 구조

예제 코드와 입력 데이터셋은 동일한 폴더에 둡니다. 실행 결과만 `output/`으로 분리합니다.

```text
Chapter02_Python과데이터처리/examples/12_mini_project_solution/
├── text_data_explorer.py
├── reviews.csv
└── output/                 # 실행 시 생성
    ├── reviews_clean.csv
    └── reviews_clean.report.json
```

저장소에 포함된 배포용 파일:

- [완성 예제 안내](examples/12_mini_project_solution/README.md)
- [완성 예제 코드](examples/12_mini_project_solution/text_data_explorer.py)
- [입력 데이터셋](examples/12_mini_project_solution/reviews.csv)

## 기능 요구사항

1. 명령행에서 입력·출력 경로를 받습니다.
2. 파일 존재 여부와 필수 열을 검사합니다.
3. UTF-8/BOM CSV를 읽습니다.
4. 결측·빈 문장을 제거합니다.
5. 문장 공백과 레이블 표기를 정규화합니다.
6. 허용하지 않은 레이블이면 명확한 오류를 냅니다.
7. 정규화된 문장 기준 중복을 제거합니다.
8. 문장 길이와 레이블 분포를 계산합니다.
9. 정제 CSV와 JSON 보고서를 별도 저장합니다.
10. 원본 파일은 변경하지 않습니다.

## 처리 설계

```text
CLI 인수
  → 경로 검사
  → CSV 읽기
  → 스키마 검사
  → 정제
  → 결과 검증
  → CSV 저장
  → JSON 보고서 저장
```

## 완성 예제

아래 코드를 `text_data_explorer.py`로 저장하면 실행할 수 있습니다. 이번 작업에서는 문서만 작성하므로 코드는 별도 파일로 생성하지 않습니다.

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"id", "text", "label"}
ALLOWED_LABELS = {"positive", "negative", "neutral", "unknown"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="텍스트 CSV를 정제하고 요약합니다.")
    parser.add_argument("input", type=Path, help="입력 CSV 경로")
    parser.add_argument("output", type=Path, help="정제 CSV 경로")
    return parser.parse_args()


def validate_columns(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"필수 열이 없습니다: {', '.join(sorted(missing))}")


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
    result = result.loc[result["text"].str.len() > 0].copy()
    result["label"] = (
        result["label"].fillna("unknown").astype("string").str.lower().str.strip()
    )

    invalid_labels = sorted(set(result["label"]) - ALLOWED_LABELS)
    if invalid_labels:
        raise ValueError(f"허용되지 않은 레이블: {invalid_labels}")

    result = result.drop_duplicates(subset=["text"], keep="first").copy()
    result["text_length"] = result["text"].str.len()
    return result.reset_index(drop=True)


def build_report(before: pd.DataFrame, after: pd.DataFrame) -> dict:
    return {
        "rows_before": len(before),
        "rows_after": len(after),
        "rows_removed": len(before) - len(after),
        "missing_text_before": int(before["text"].isna().sum()),
        "average_text_length": (
            round(float(after["text_length"].mean()), 2) if not after.empty else 0.0
        ),
        "label_counts": {
            str(key): int(value)
            for key, value in after["label"].value_counts().items()
        },
    }


def run(input_path: Path, output_path: Path) -> tuple[pd.DataFrame, dict]:
    if not input_path.is_file():
        raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {input_path}")

    original = pd.read_csv(input_path, encoding="utf-8-sig")
    cleaned = clean_dataframe(original)

    assert cleaned["text"].notna().all()
    assert cleaned["text"].str.len().gt(0).all()
    assert cleaned["text"].is_unique
    assert set(cleaned["label"]) <= ALLOWED_LABELS

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False, encoding="utf-8-sig")

    report = build_report(original, cleaned)
    report_path = output_path.with_suffix(".report.json")
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return cleaned, report


def main() -> None:
    args = parse_args()
    _, report = run(args.input, args.output)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

## 실행 예시

```powershell
cd lecture\Part01_자연어처리기초와Python\Chapter02_Python과데이터처리\examples\12_mini_project_solution
python text_data_explorer.py reviews.csv output\reviews_clean.csv
```

예상 보고서:

```json
{
  "rows_before": 4,
  "rows_after": 2,
  "rows_removed": 2,
  "missing_text_before": 1,
  "average_text_length": 8.5,
  "label_counts": {
    "positive": 1,
    "negative": 1
  }
}
```

## 테스트 시나리오

| 번호 | 입력 | 기대 결과 |
|---|---|---|
| 1 | 정상 CSV | 정제 CSV와 보고서 생성 |
| 2 | 파일 없음 | 경로를 포함한 오류 |
| 3 | `text` 열 없음 | 누락 열을 포함한 오류 |
| 4 | 결측·공백 문장 | 해당 행 제거 |
| 5 | 공백만 다른 중복 | 하나만 유지 |
| 6 | 잘못된 레이블 | 잘못된 값을 포함한 오류 |
| 7 | 유효 행 0개 | 빈 CSV와 평균 0 보고서 |

## 확장 아이디어

- 입력 형식에 JSON 추가
- 최소·최대 문장 길이를 명령행 옵션으로 제공
- 제외된 행과 제외 사유를 별도 파일로 저장
- 정제 규칙별 제거 건수를 단계별로 기록
- 단위 테스트와 자동화된 품질 검사 추가

## 완료 체크리스트

- [ ] 원본과 출력 경로가 분리되어 있다.
- [ ] 예제 코드와 입력 데이터셋이 같은 예제 폴더에 있다.
- [ ] 필수 열과 허용 레이블을 검사한다.
- [ ] 결측·공백·중복 처리 순서가 명확하다.
- [ ] 정제 결과를 단언문 또는 테스트로 검증한다.
- [ ] 처리 전후 통계를 JSON으로 남긴다.
- [ ] 오류 메시지만 보고도 사용자가 수정 방향을 알 수 있다.

Chapter 2를 마쳤습니다. 다음 장에서는 이 데이터를 정규표현식, 토큰화, 형태소 분석 등 NLP 전처리 기법에 연결합니다.

