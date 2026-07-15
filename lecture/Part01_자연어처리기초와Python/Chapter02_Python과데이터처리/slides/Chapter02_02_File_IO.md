---
marp: true
theme: nlp-training
paginate: true
size: 16:9
title: Chapter 2-2. 파일·CSV·JSON 처리
description: NLP Training 2026 Chapter 2 Lecture 2
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Chapter 2-2
## 파일·CSV·JSON 처리

NLP Training 2026

---

# 이번 강의의 학습 목표

- 파일 이름으로 CSV를 읽고 저장한다
- 입력과 출력 파일을 구분한다
- 인코딩이 필요한 이유를 설명한다
- TXT·CSV·JSON의 차이를 구분한다
- 목적에 맞는 파일 형식을 선택한다

---

# `pathlib.Path`로 경로 만들기

> 선택 확장: 기본 실습에서는 `"reviews.csv"`처럼 파일 이름을 사용한다

```python
from pathlib import Path

data_dir = Path("data")
input_path = data_dir / "raw" / "reviews.txt"
output_path = data_dir / "processed" / "reviews_clean.txt"
```

- 문자열 경로는 운영체제별 구분자와 연결 오류에 취약하다
- `/` 연산자로 경로 요소를 읽기 쉽게 연결한다
- 부모 폴더 생성과 파일 속성 확인도 간결해진다

---

# 출력 폴더를 먼저 준비한다

```python
output_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)
```

- `parent`: 파일의 부모 폴더
- `parents=True`: 상위 폴더도 함께 생성
- `exist_ok=True`: 이미 있어도 오류를 내지 않음

---

# 실행 위치와 코드 위치는 다를 수 있다

```python
BASE_DIR = Path(__file__).resolve().parent
input_path = BASE_DIR / "reviews.txt"
```

터미널을 어디에서 실행하더라도 코드 파일을 기준으로 경로를 만든다

---

# 텍스트 파일 읽기

```python
path = Path("reviews.txt")
text = path.read_text(encoding="utf-8")
lines = text.splitlines()
```

- 인코딩을 명시한다
- `splitlines()`는 운영체제별 줄바꿈을 처리한다
- 작은 파일은 한 번에 읽어도 편리하다

---

# 텍스트 파일 쓰기

```python
cleaned = [line.strip() for line in lines if line.strip()]

Path("reviews_clean.txt").write_text(
    "\n".join(cleaned),
    encoding="utf-8",
)
```

출력 인코딩과 줄바꿈 규칙을 코드로 고정한다

---

# 큰 파일은 한 줄씩 처리한다

> 선택 확장: 작은 실습 파일은 한 번에 읽어도 충분하다

```python
with path.open("r", encoding="utf-8") as file:
    for line in file:
        cleaned = line.strip()
        if cleaned:
            print(cleaned)
```

전체 파일을 메모리에 올리지 않아도 된다

---

# CSV를 문자열로 나누면 안 되는 이유

```text
1,"배송은 빠르지만, 포장이 아쉬워요",negative
```

단순히 쉼표로 나누면 따옴표 안의 쉼표도 열 구분자로 오해한다

**CSV 규칙은 `csv` 모듈에 맡긴다**

---

# CSV 읽기

```python
import csv

records = []
with Path("reviews.csv").open(
    "r", encoding="utf-8-sig", newline=""
) as file:
    reader = csv.DictReader(file)
    records.extend(reader)
```

각 행을 열 이름 기반의 딕셔너리로 읽는다

---

# CSV 쓰기

```python
fieldnames = ["id", "text", "label"]

with Path("reviews_clean.csv").open(
    "w", encoding="utf-8-sig", newline=""
) as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)
```

---

# `utf-8`과 `utf-8-sig`

| 인코딩 | 일반적 용도 |
|---|---|
| `utf-8` | 코드·서버·대부분의 텍스트 처리 |
| `utf-8-sig` | Excel과 주고받는 한글 CSV |

- 입력 시 BOM이 있으면 `utf-8-sig`가 제거한다
- 팀에서 사용할 인코딩 규칙을 미리 정한다

---

# JSON 읽기와 쓰기

```python
import json

data = json.loads(
    Path("reviews.json").read_text(encoding="utf-8")
)
Path("reviews_clean.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
```

`ensure_ascii=False`로 한글을 읽을 수 있는 형태로 저장한다

---

# 목적에 맞는 형식 선택

| 형식 | 적합한 데이터 | 주의점 |
|---|---|---|
| TXT | 한 줄에 한 문장 | 열 구조 표현이 어려움 |
| CSV | 일정한 행과 열 | 중첩 구조에 부적합 |
| JSON | 레코드와 메타데이터 | 큰 파일의 메모리 사용 |

형식은 익숙함보다 **데이터 구조와 사용 도구**로 선택한다

---

# 핵심 정리

- 기본 실습에서는 코드와 CSV를 같은 폴더에 둔다
- 텍스트 입출력에는 인코딩을 명시한다
- CSV는 `csv` 모듈로 따옴표와 쉼표를 처리한다
- `Path`와 JSON은 기본 흐름 이후 선택적으로 확장한다
- 다음 강의에서는 `pandas`로 표 데이터를 탐색한다
