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
