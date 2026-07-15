# Chapter 2 통합 강의 원고

---

<!-- SOURCE: README.md -->

# Chapter 2. Python과 데이터 처리


## 핵심 용어 미리보기

본문을 읽기 전에 다음 용어의 뜻과 영어 원어를 먼저 확인합니다. 전체 정의는 [교육과정 핵심 용어집](../../TERMINOLOGY.md)에서 확인할 수 있습니다.

- **데이터셋(Dataset): 분석·학습에 사용하는 데이터 묶음**
- **데이터프레임(DataFrame): 행과 열로 구성된 표 형태의 데이터 구조**
- **스키마(Schema): 열 이름·자료형·필수 여부처럼 데이터가 지켜야 할 구조**
- **결측값(Missing Value): 값이 없거나 관측되지 않은 상태**

자연어 처리에서는 모델 학습 전에 **데이터를 읽고, 구조를 진단하고, 정제하고, 검증하여 다시 저장하는 과정**이 필요합니다. 이 장은 비전공자도 따라올 수 있도록 짧은 코드부터 시작하고, 같은 작업을 점차 실무적인 구조로 확장합니다.

## 학습 목표

이 장을 마치면 다음을 할 수 있습니다.

- 텍스트, CSV, JSON 파일을 UTF-8로 안전하게 읽고 쓴다.
- pandas로 표 데이터를 탐색하고 결측값·중복·문자열을 정제한다.
- 데이터 스키마와 정제 결과를 검증한다.
- 처리 전후 통계를 기록하는 작은 데이터 처리 프로그램을 완성한다.

## 선수 지식

별도의 Python 선수 지식 없이 시작할 수 있습니다. 변수, 문자열, 리스트, 조건문, 반복문과 간단한 함수는 이 Chapter의 `02~05` 문서에서 다시 학습합니다. 타입 힌트, 예외 처리와 CLI는 선택 확장입니다.

## 권장 학습 순서

```text
Python 기초 복습(02~05)
  → Step by Step(함께 따라 하기)
  → Basic Practice(짧은 전체 코드)
  → Assignment(개별 과제)
  → Assignment Solution(시도 후 해설)
  → Mini Project(종합 적용)
  → Mini Project Solution(피드백 후 공개)
```

solution은 정답 복사용 자료가 아니라 수강생 코드와 비교하는 해설 자료입니다. 강사는 다수의 수강생이 기본 요구사항을 시도한 뒤 공개합니다.

## 문서 구성

1. [학습 안내](01_Opening.md)
2. [Python 실행과 기본 문법](02_Python_Basics.md)
3. [문자열과 컬렉션](03_Strings_and_Collections.md)
4. [조건문과 반복문](04_Control_Flow.md)
5. [함수와 모듈](05_Functions_and_Modules.md)
6. [파일·CSV·JSON 처리](06_File_IO.md)
7. [pandas로 표 데이터 다루기](07_Pandas.md)
8. [텍스트 데이터 정제와 검증](08_Data_Cleaning.md)
9. [Step by Step](examples/01_step_by_step/README.md)
10. [Basic Practice](examples/02_basic_practice/README.md)
11. [핵심 정리](09_Summary.md)
12. [퀴즈](10_Quiz.md)
13. [실습 과제](11_Assignment.md)
14. [미니 프로젝트: 텍스트 데이터 탐색기](12_Mini_Project.md)

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
    ├── 01_step_by_step/             # 강사와 함께 실행
    ├── 02_basic_practice/            # 입문용 통합 실습
    ├── 11_assignment_solution/
    │   ├── assignment_solution.py
    │   └── customer_inquiries.csv
    ├── 12_mini_project_starter/      # 수강생 시작 코드
    └── 12_mini_project_solution/     # 피드백 후 공개
        ├── text_data_explorer.py
        └── reviews.csv
```

실행 결과는 원본과 섞이지 않도록 같은 폴더 아래 `output/`에 저장합니다.

> 예제는 Windows PowerShell 기준 명령도 함께 제시하지만, Python 코드는 운영체제와 무관하게 실행되도록 작성합니다.

## 완료 기준

- 변수·리스트·조건문·반복문·간단한 함수 예제를 직접 수정
- Step by Step에서 각 단계 후 행 수가 달라진 이유를 설명
- Basic Practice의 입력 파일과 저장 파일을 바꿔 실행
- 퀴즈 8문항 중 6문항 이상 정답
- 실습 과제의 기본 요구사항 완료
- 미니 프로젝트에서 읽기·정제·저장 흐름 완료

파일 검사, 사용자 정의 오류, CLI, JSON 보고서는 빠른 학습자를 위한 선택 목표입니다.

다음 장에서는 이 장에서 준비한 텍스트 데이터를 바탕으로 정규표현식과 형태소 분석 등 본격적인 텍스트 전처리를 학습합니다.

---

<!-- SOURCE: 01_Opening.md -->

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

이 장의 코드는 한 번에 완성하지 않습니다. 먼저 한 줄씩 실행하고, 다음에는 짧은 프로그램으로 합친 뒤, 마지막에 함수와 검증을 추가합니다.

```text
Python 기초 복습 → 한 단계씩 실행 → 짧은 전체 코드 → 과제 → 프로젝트 → 완성형 코드 비교
```

Python이 익숙하지 않다면 [기본 문법](02_Python_Basics.md)부터 [함수와 모듈](05_Functions_and_Modules.md)까지 먼저 진행합니다. 이미 익숙한 수강생은 예제를 빠르게 실행해 확인하고 파일 처리로 이동할 수 있습니다.

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

Python 기초 `02~05`를 확인한 뒤 [Step by Step](examples/01_step_by_step/README.md)을 강사와 함께 진행하고, 이어서 [Basic Practice](examples/02_basic_practice/README.md)를 완성합니다. 과제와 미니 프로젝트 solution은 직접 시도한 뒤 확인합니다.

---

<!-- SOURCE: 02_Python_Basics.md -->

# 02. Python 실행과 기본 문법

> **기본 목표:** 값을 변수에 저장하고, 자료형을 확인하고, 화면에 출력할 수 있으면 충분합니다.

## 변수와 자료형

변수는 값에 붙이는 이름입니다.

```python
course = "NLP Training"
year = 2026
score = 0.8
is_ready = True
missing_text = None

print(course)
print(year)
```

`type()`으로 값의 자료형을 확인합니다.

```python
print(type(course))       # str
print(type(year))         # int
print(type(score))        # float
print(type(is_ready))     # bool
print(type(missing_text)) # NoneType
```

| 자료형 | 의미 | 예시 |
|---|---|---|
| `str` | 문자열 | `"배송이 빨라요"` |
| `int` | 정수 | `10` |
| `float` | 실수 | `0.8` |
| `bool` | 참·거짓 | `True` |
| `None` | 값이 없음 | `None` |

## 변수 이름 짓기

- 의미가 드러나는 이름을 사용합니다.
- 단어 사이는 `_`로 구분합니다.
- Python이 이미 사용하는 `list`, `str` 같은 이름은 피합니다.

```python
review_count = 120
default_encoding = "utf-8"
```

## 기본 연산과 비교

```python
total = 10
valid = 7
ratio = valid / total

print(ratio)
print(valid == 7)                 # True
print(valid >= 5)                 # True
print("배송" in "배송이 빨라요") # True
```

- `=`: 값을 변수에 저장
- `==`: 두 값이 같은지 비교
- `in`: 문자열이나 목록 안에 값이 있는지 확인

## 값이 없는지 확인하기

```python
text = None

if text is None:
    print("문장이 없습니다.")
```

`None`은 빈 문자열 `""`과 다릅니다.

## 문자열과 숫자 변환

파일에서 읽은 숫자는 문자열일 수 있습니다.

```python
raw_count = "15"
count = int(raw_count)
print(count + 5)
```

```python
score = float("0.92")
print(score)
```

## f-string으로 출력하기

```python
course = "NLP"
student_count = 20

message = f"{course} 과정의 수강생은 {student_count}명입니다."
print(message)
```

## 입력받기

```python
keyword = input("검색어를 입력하세요: ")
keyword = keyword.strip()
print("검색어:", keyword)
```

## 선택 확장: 변환 오류 처리

처음에는 읽기만 하고, 오류 처리는 기본 실습을 마친 뒤 확인합니다.

```python
try:
    count = int("15개")
except ValueError:
    print("숫자로 바꿀 수 없습니다.")
```

## 실습

1. 과정명, 연도, 수강 인원과 개설 여부를 변수에 저장합니다.
2. 각 값의 자료형을 `type()`으로 출력합니다.
3. f-string으로 과정 정보를 한 줄로 출력합니다.
4. 문자열 `"42"`를 정수로 바꾸고 8을 더합니다.

> 다음: [문자열과 컬렉션](03_Strings_and_Collections.md)

---

<!-- SOURCE: 03_Strings_and_Collections.md -->

# 03. 문자열과 컬렉션

> **기본 목표:** 문자열을 정리하고, 여러 문장을 리스트와 딕셔너리에 저장할 수 있으면 충분합니다.

## 문자열 정리

```python
text = "  자연어 처리는 재미있다!  "

cleaned = text.strip()
print(cleaned)
print(cleaned.lower())
print(cleaned.replace("재미있다", "유용하다"))
print(len(cleaned))
```

- `strip()`: 앞뒤 공백 제거
- `lower()`: 영문을 소문자로 변경
- `replace()`: 문자열 일부 교체
- `len()`: 글자 수 확인

## 문자열 나누기와 합치기

```python
sentence = "자연어 처리는 재미있다"
words = sentence.split()

print(words)
print(" | ".join(words))
```

CSV는 쉼표가 포함된 문장이 있을 수 있으므로 직접 `split(",")`하지 않습니다.

## 문자열 일부 선택

```python
word = "자연어처리"

print(word[:3]) # 자연어
print(word[3:]) # 처리
```

## 리스트

리스트는 여러 값을 순서대로 저장합니다.

```python
texts = ["배송이 빨라요", "가격이 비싸요"]

texts.append("품질이 좋아요")

for text in texts:
    print(text)
```

```python
print(texts[0])
print(len(texts))
```

## 딕셔너리

딕셔너리는 이름과 값을 한 쌍으로 저장합니다.

```python
review = {
    "id": 1,
    "text": "배송이 빨라요",
    "label": "positive",
}

print(review["text"])
print(review["label"])
```

여러 딕셔너리를 리스트에 저장할 수 있습니다.

```python
reviews = [
    {"id": 1, "text": "좋아요", "label": "positive"},
    {"id": 2, "text": "아쉬워요", "label": "negative"},
]

for review in reviews:
    print(review["id"], review["text"])
```

## 집합

집합은 중복을 제거할 때 사용할 수 있습니다.

```python
labels = ["positive", "negative", "positive"]
unique_labels = set(labels)

print(unique_labels)
```

집합의 출력 순서는 달라질 수 있습니다.

## 선택 확장: 딕셔너리로 개수 세기

```python
counts = {}

for label in labels:
    counts[label] = counts.get(label, 0) + 1

print(counts)
```

## 실습

1. 문장 세 개를 리스트에 저장합니다.
2. 각 문장의 앞뒤 공백을 제거해 출력합니다.
3. 리뷰 하나를 `id`, `text`, `label` 딕셔너리로 만듭니다.
4. 레이블 목록의 중복을 집합으로 제거합니다.

> 다음: [조건문과 반복문](04_Control_Flow.md)

---

<!-- SOURCE: 04_Control_Flow.md -->

# 04. 조건문과 반복문

> **기본 목표:** 조건에 따라 다른 작업을 하고, 여러 문장을 차례대로 처리할 수 있으면 충분합니다.

## 조건문

```python
text = "배송이 정말 빨라요"

if "배송" in text:
    category = "배송 문의"
else:
    category = "기타 문의"

print(category)
```

조건이 여러 개라면 `elif`를 사용합니다.

```python
text = "상품을 환불하고 싶어요"

if "환불" in text:
    category = "환불 문의"
elif "배송" in text:
    category = "배송 문의"
else:
    category = "기타 문의"

print(category)
```

## 결측값과 빈 문자열 구분

```python
text = None

if text is None:
    print("결측값입니다.")
elif text.strip() == "":
    print("공백뿐인 문장입니다.")
else:
    print("처리할 문장입니다.")
```

## 반복문

```python
texts = ["좋아요", "배송이 빨라요", "환불하고 싶어요"]

for text in texts:
    print(text)
```

번호와 값을 함께 출력하려면 `enumerate()`를 사용합니다.

```python
for number, text in enumerate(texts, start=1):
    print(number, text)
```

## 조건문과 반복문 연결

```python
texts = ["좋아요", "", "배송이 빨라요"]

for text in texts:
    if text == "":
        continue
    print(text)
```

`continue`는 현재 항목만 건너뛰고 다음 항목을 처리합니다.

## 두 리스트 함께 처리하기

```python
texts = ["좋아요", "아쉬워요"]
labels = ["positive", "negative"]

for text, label in zip(texts, labels):
    print(label, text)
```

## 유효한 문장만 모으기

```python
raw_texts = ["  좋아요 ", "", " 배송이 빨라요 "]
clean_texts = []

for text in raw_texts:
    cleaned = text.strip()
    if cleaned != "":
        clean_texts.append(cleaned)

print(clean_texts)
```

## 선택 확장: 리스트 컴프리헨션

위 코드를 짧게 쓸 수도 있지만, 처음에는 일반 반복문을 권장합니다.

```python
clean_texts = [text.strip() for text in raw_texts if text.strip()]
```

## 실습

1. 질문에 `배송`이 있으면 배송 문의로 분류합니다.
2. 환불·배송·기타 문의를 `if`, `elif`, `else`로 구분합니다.
3. 문장 리스트를 반복하며 빈 문자열은 건너뜁니다.
4. 정제한 문장만 새 리스트에 저장합니다.

> 다음: [함수와 모듈](05_Functions_and_Modules.md)

---

<!-- SOURCE: 05_Functions_and_Modules.md -->

# 05. 함수와 모듈

> **기본 목표:** 반복되는 코드에 함수 이름을 붙이고, 입력값을 받아 결과를 반환할 수 있으면 충분합니다.

## 함수가 필요한 이유

같은 처리를 여러 번 사용할 때 함수로 묶습니다.

```python
def clean_text(text):
    cleaned = text.strip()
    return cleaned


print(clean_text("  배송이 빨라요  "))
print(clean_text("  환불하고 싶어요  "))
```

## 매개변수와 반환값

```python
def add(a, b):
    result = a + b
    return result


answer = add(3, 5)
print(answer)
```

- `a`, `b`: 함수가 받는 값
- `return`: 함수가 돌려주는 결과

## 기본값 사용하기

```python
def is_long_text(text, min_length=10):
    return len(text) >= min_length


print(is_long_text("짧은 문장"))
print(is_long_text("이 문장은 비교적 긴 문장입니다"))
```

## 문의 분류 함수

```python
def detect_intent(text):
    if "환불" in text:
        return "환불 문의"
    elif "배송" in text:
        return "배송 문의"
    else:
        return "기타 문의"


questions = [
    "상품을 환불하고 싶어요",
    "배송이 아직 안 왔어요",
    "상담원과 통화하고 싶어요",
]

for question in questions:
    print(question, "→", detect_intent(question))
```

## 한 함수에는 한 가지 역할

처음에는 읽기 쉬운 작은 함수로 나눕니다.

```python
def clean_text(text):
    return " ".join(text.split())


def text_length(text):
    return len(text)
```

파일 읽기, 정제, 통계와 저장을 하나의 긴 함수에 모두 넣지 않습니다.

## 모듈 사용하기

다른 Python 파일에 있는 함수를 가져올 수 있습니다.

```python
from text_utils import clean_text
```

처음에는 한 파일에서 함수를 연습한 뒤 여러 파일로 나눕니다.

## 선택 확장: 타입 힌트

```python
def clean_text(text: str) -> str:
    return " ".join(text.split())
```

타입 힌트는 함수가 받을 값과 반환값을 설명합니다. 기본 실습에서는 생략해도 됩니다.

## 선택 확장: 진입점

```python
def main():
    print(clean_text("  자연어   처리  "))


if __name__ == "__main__":
    main()
```

진입점 구조는 완성형 solution에서 다시 설명합니다.

## 실습

1. 문자열 앞뒤 공백을 제거하는 함수를 만듭니다.
2. 문자열 길이를 반환하는 함수를 만듭니다.
3. 배송·환불·기타 문의를 구분하는 함수를 만듭니다.
4. 문장 리스트를 반복하며 분류 함수를 호출합니다.

> 다음: [파일·CSV·JSON 처리](06_File_IO.md)

---

<!-- SOURCE: 06_File_IO.md -->

# 06. 파일·CSV·JSON 처리

> **기본 목표:** 파일 이름을 지정해 읽고 저장할 수 있으면 충분합니다. `pathlib`, 예외 처리, 대용량 파일 처리는 선택 확장입니다.

## 가장 간단한 CSV 입출력

처음에는 코드와 CSV를 같은 폴더에 두고 파일 이름만 사용합니다.

```python
import pandas as pd

df = pd.read_csv("reviews.csv", encoding="utf-8-sig")
print(df)

df.to_csv("reviews_clean.csv", index=False, encoding="utf-8-sig")
```

이 코드가 실행된 뒤 아래의 경로 관리와 파일 형식으로 확장합니다.

## 선택 확장: pathlib로 경로 다루기

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

## 선택 확장: 텍스트 파일

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

## 선택 확장: 표준 라이브러리로 CSV 처리

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

## 선택 확장: JSON

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

## 선택 확장: 안전한 오류 메시지

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

---

<!-- SOURCE: 07_Pandas.md -->

# 07. pandas로 표 데이터 다루기

> **기본 목표:** 코드를 위에서 아래로 한 줄씩 실행하며 데이터가 어떻게 바뀌는지 확인합니다. 메서드 체이닝과 그룹 집계는 기본 흐름을 익힌 뒤 다룹니다.

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
valid["text"] = valid["text"].astype("string")
valid["text"] = valid["text"].str.strip()
valid["text"] = valid["text"].str.replace(r"\s+", " ", regex=True)
valid = valid[valid["text"] != ""]
valid["text_length"] = valid["text"].str.len()
```

한 줄을 실행할 때마다 `print(valid)`로 결과를 확인합니다.

## 중복 제거

```python
duplicate_count = valid.duplicated(subset=["text"]).sum()
deduplicated = valid.drop_duplicates(subset=["text"], keep="first").copy()
```

무엇을 중복으로 볼지 먼저 정의해야 합니다. `id`가 달라도 정제된 `text`가 같으면 중복으로 볼 것인지 업무 규칙이 필요합니다.

## 선택 확장: 그룹 집계

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

## 선택 확장: 단계 이름 붙이기

긴 메서드 체인은 편리하지만 교육과 디버깅에서는 중간 결과를 나누는 편이 좋습니다.

```python
without_missing = df.dropna(subset=["text"]).copy()
normalized = without_missing.assign(text=without_missing["text"].str.strip())
non_empty = normalized.loc[normalized["text"].ne("")].copy()
```

각 단계의 `shape`를 확인하면 어느 규칙에서 행이 사라졌는지 알 수 있습니다.

---

<!-- SOURCE: 08_Data_Cleaning.md -->

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

---

<!-- SOURCE: 09_Summary.md -->

# 09. 핵심 정리

## 기본 처리 흐름

```text
CSV 읽기 → 구조 확인 → 결측 제거 → 공백 정리 → 중복 제거 → 저장
```

- 처음에는 코드와 데이터 파일을 같은 폴더에 둡니다.
- 한 줄씩 실행하고 `print()`로 중간 결과를 확인합니다.
- 처리 전후 행 수가 달라진 이유를 기록합니다.
- 원본 파일과 정제 결과 파일을 분리합니다.

## 난이도별 도달 목표

| 단계 | 할 수 있어야 하는 일 |
|---|---|
| 기본 | CSV를 읽고 결측·공백·중복을 처리해 저장 |
| 발전 | 함수로 정제 로직을 분리하고 결과 검증 |
| 선택 확장 | 경로 검사, CLI, JSON 보고서 구현 |

## 다음 학습 순서

1. Step by Step을 강사와 함께 실행합니다.
2. Basic Practice로 전체 흐름을 연결합니다.
3. Assignment를 직접 시도한 뒤 solution과 비교합니다.
4. Mini Project starter를 완성합니다.
5. 피드백 후 완성형 solution의 확장 구조를 살펴봅니다.

## 다음 Chapter로 연결하기

다음 Chapter에서는 정규표현식, 토큰화, 불용어, 형태소 분석 등 언어 데이터에 특화된 전처리로 확장합니다.

---

<!-- SOURCE: 10_Quiz.md -->

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

---

<!-- SOURCE: 11_Assignment.md -->

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

처음에는 1~7번을 **기본 목표**로 수행합니다. 8~10번은 기본 목표를 실행한 뒤 추가합니다.

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

> **강사용 공개 시점:** 수강생이 기본 목표 1~7번을 시도하고, 처리 전후 데이터가 달라진 이유를 설명한 뒤 공개합니다.

완성 답안은 함수, 검증과 경로 관리를 포함한 실무형 확장 코드입니다. 처음부터 같은 구조로 작성할 필요는 없습니다.

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

---

<!-- SOURCE: 12_Mini_Project.md -->

# 12. 미니 프로젝트: 텍스트 데이터 탐색기

## 프로젝트 목표

CSV 파일을 읽어 텍스트를 정제하고, 정제 결과와 간단한 요약을 저장합니다. 처음에는 함수, CLI, JSON 보고서 없이 기본 흐름을 완성합니다.

```text
입력 → 확인 → 정제 → 요약 → 저장
```

## 시작 전 확인

다음 항목 중 네 가지 이상을 설명할 수 있으면 시작합니다.

- `pd.read_csv()`로 CSV를 읽는 방법
- `dropna()`로 결측 문장을 제거하는 방법
- `.str.strip()`으로 앞뒤 공백을 제거하는 방법
- 빈 문자열을 조건으로 제외하는 방법
- `drop_duplicates()`로 중복을 제거하는 방법
- `to_csv()`로 결과를 저장하는 방법

설명이 어렵다면 [Basic Practice](examples/02_basic_practice/README.md)를 한 번 더 실행합니다.

## 입력 데이터

`reviews.csv`는 `id`, `text`, `label` 열을 가집니다.

```csv
id,text,label
1,배송이 빨라요,positive
2,  환불하고 싶어요  ,negative
3,,unknown
4,배송이 빨라요,positive
```

## 시작 코드

다음 폴더에는 단계별 주석과 입력 데이터가 있습니다.

- [시작 안내](examples/12_mini_project_starter/README.md)
- [시작 코드](examples/12_mini_project_starter/text_data_explorer_starter.py)
- [입력 데이터](examples/12_mini_project_starter/reviews.csv)

```powershell
cd examples\12_mini_project_starter
python text_data_explorer_starter.py
```

## 1단계: 기본 요구사항

1. `reviews.csv`를 읽습니다.
2. 처리 전 행 수를 저장합니다.
3. `text`가 결측인 행을 제거합니다.
4. `text`의 앞뒤 공백과 연속 공백을 정리합니다.
5. 정제 후 빈 문자열인 행을 제거합니다.
6. `label`을 소문자로 통일합니다.
7. 정제된 `text` 기준으로 중복을 제거합니다.
8. `text_length` 열을 추가합니다.
9. 처리 전후 행 수와 레이블 분포를 출력합니다.
10. `reviews_clean.csv`로 저장합니다.

처음부터 열 항목을 모두 작성하지 말고 2~3개씩 구현한 뒤 실행합니다.

## 중간 점검

solution을 보기 전에 다음을 확인합니다.

- 프로그램이 오류 없이 끝까지 실행되는가?
- 결측 행과 공백뿐인 행이 제거됐는가?
- 공백만 다른 중복 문장이 하나로 줄었는가?
- `Positive`가 `positive`로 바뀌었는가?
- 처리 전후 행 수 차이를 설명할 수 있는가?
- 생성된 CSV를 다시 읽을 수 있는가?

## 막혔을 때 사용하는 힌트

### 힌트 1: 결측 제거

```python
df = df.dropna(subset=["text"])
```

### 힌트 2: 공백 정리

```python
df["text"] = df["text"].str.strip()
df["text"] = df["text"].str.replace(r"\s+", " ", regex=True)
```

### 힌트 3: 중복 제거

```python
df = df.drop_duplicates(subset=["text"])
```

힌트는 위에서부터 필요한 만큼만 확인합니다.

## 2단계: 선택 도전

기본 요구사항을 완성한 학습자만 진행합니다.

- 필수 열 `id`, `text`, `label`이 있는지 검사
- 허용되지 않은 레이블 탐지
- 정제 로직을 함수로 분리
- `assert`로 결과 검증
- 입력·출력 경로를 명령행에서 받기
- 처리 결과를 JSON 보고서로 저장
- 입력 파일이 없을 때 이해하기 쉬운 오류 출력

선택 도전을 모두 구현할 필요는 없습니다. 한 가지를 골라 기존 코드에 추가합니다.

## 테스트 시나리오

| 번호 | 입력 | 기본 기대 결과 |
|---|---|---|
| 1 | 정상 CSV | 정제 CSV 생성 |
| 2 | 결측 문장 | 해당 행 제거 |
| 3 | 공백 문장 | 해당 행 제거 |
| 4 | 공백만 다른 중복 | 하나만 유지 |
| 5 | 대문자 레이블 | 소문자로 통일 |

파일 없음, 필수 열 누락, 잘못된 레이블 검사는 선택 도전에서 확인합니다.

## Solution 공개 및 해설

> **강사용 공개 시점:** 수강생이 기본 요구사항을 충분히 시도하고, 공통 오류에 대한 피드백을 받은 뒤 공개합니다.

완성형 solution에는 함수, 타입 힌트, CLI, 오류 검사와 JSON 보고서가 포함되어 있습니다. 수강생의 기본 코드보다 복잡한 것이 정상이며, 처음부터 동일하게 작성하는 것이 목표가 아닙니다.

- [완성형 solution 안내](examples/12_mini_project_solution/README.md)
- [완성형 solution 코드](examples/12_mini_project_solution/text_data_explorer.py)
- [solution 입력 데이터](examples/12_mini_project_solution/reviews.csv)

해설에서는 전체 코드를 다시 입력하기보다 다음 순서로 수강생 코드와 비교합니다.

1. 반복되는 처리를 함수로 분리한 부분
2. 잘못된 입력을 미리 검사한 부분
3. 처리 결과를 보고서로 만든 부분
4. 실행할 때 파일 경로를 바꿀 수 있게 만든 부분

## 완료 기준

- 기본 요구사항 10개 중 8개 이상 구현
- 처리 전후 결과가 달라진 이유 설명
- 자신의 코드에서 정제 단계 하나를 찾아 수정
- solution과 자신의 코드 차이 한 가지 설명

선택 도전 구현 여부는 기본 완료 기준에 포함하지 않습니다.
