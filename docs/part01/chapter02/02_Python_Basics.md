# 02. Python 실행과 기본 문법

## 변수와 객체

Python 변수는 값을 담는 고정 상자라기보다 객체를 가리키는 이름입니다.

```python
course = "NLP Training"
year = 2026
threshold = 0.8
is_ready = True
missing_text = None
```

`type()`으로 자료형을 확인합니다.

```python
print(type(course))       # <class 'str'>
print(type(year))         # <class 'int'>
print(type(threshold))    # <class 'float'>
print(type(is_ready))     # <class 'bool'>
print(type(missing_text)) # <class 'NoneType'>
```

## 이름 짓기

- 변수와 함수: `snake_case`
- 상수로 취급할 값: `UPPER_SNAKE_CASE`
- 의미가 드러나는 이름 사용: `text_count`가 `n`보다 명확함
- `list`, `str`, `id`처럼 내장 함수 이름을 변수로 덮어쓰지 않기

```python
DEFAULT_ENCODING = "utf-8"
review_count = 120
```

## 연산자

```python
total = 10
valid = 7
ratio = valid / total

print(valid == 7)               # True
print(valid >= 5 and total > 0) # True
print("배송" in "배송이 빨라요") # True
```

`==`는 값 비교, `is`는 동일 객체 여부 비교입니다. `None`은 `is`로 확인합니다.

```python
text = None
if text is None:
    print("문장이 없습니다.")
```

## 형 변환

파일에서 읽은 값은 숫자처럼 보여도 문자열일 수 있습니다.

```python
raw_count = "15"
count = int(raw_count)
score = float("0.92")
message = f"문장 수: {count}, 점수: {score:.1%}"
print(message)
```

잘못된 값은 `ValueError`를 일으킵니다.

```python
try:
    count = int("15개")
except ValueError as error:
    print(f"정수로 변환할 수 없습니다: {error}")
```

## 입력과 출력

```python
keyword = input("검색어를 입력하세요: ").strip()
print(f"검색어: {keyword!r}")
```

`!r`은 공백이나 이스케이프 문자를 확인할 때 유용합니다.

## 얕은 복사 주의

```python
original = ["좋아요", "보통이에요"]
copied = original.copy()
copied.append("싫어요")

print(original)
print(copied)
```

단순 대입 `copied = original`은 같은 리스트를 가리키므로 한쪽 변경이 다른 쪽에도 보입니다.

## 실습

1. 과정명, 연도, 수강 인원, 개설 여부를 서로 알맞은 자료형으로 저장합니다.
2. f-string으로 한 줄 요약을 출력합니다.
3. 문자열 `"42"`를 정수로 변환하고 8을 더합니다.
4. `None` 여부를 안전하게 검사합니다.

> 다음: [문자열과 컬렉션](03_Strings_and_Collections.md)
