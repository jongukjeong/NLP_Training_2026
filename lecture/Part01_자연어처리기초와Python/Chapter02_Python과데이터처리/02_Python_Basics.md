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
