# 04. 조건문·반복문·컴프리헨션

## 조건문

```python
text = "배송이 정말 빨라요"

if not text.strip():
    category = "empty"
elif "배송" in text:
    category = "delivery"
else:
    category = "other"
```

빈 문자열, 빈 리스트, `0`, `None`은 조건식에서 거짓으로 평가됩니다. 다만 결측과 빈 문자열을 구분해야 할 때는 명시적으로 검사합니다.

```python
if text is None:
    status = "missing"
elif text.strip() == "":
    status = "blank"
```

## 반복문

```python
texts = ["좋아요", "", "배송이 빨라요"]

for index, text in enumerate(texts, start=1):
    if not text:
        continue
    print(index, text)
```

- `continue`: 현재 반복만 건너뜀
- `break`: 반복 전체를 종료
- `enumerate`: 순번과 값을 함께 제공
- `zip`: 여러 시퀀스를 나란히 순회

```python
texts = ["좋아요", "아쉬워요"]
labels = ["positive", "negative"]

for text, label in zip(texts, labels, strict=True):
    print(label, text)
```

Python 3.11의 `strict=True`는 두 목록 길이가 다르면 오류를 발생시켜 조용한 데이터 누락을 막습니다.

## 리스트 컴프리헨션

```python
raw_texts = ["  좋아요 ", "", " 배송이 빨라요 "]
clean_texts = [text.strip() for text in raw_texts if text.strip()]
```

복잡한 조건과 부수 효과가 섞이면 일반 반복문이 더 읽기 쉽습니다.

```python
clean_texts = []
for text in raw_texts:
    cleaned = text.strip()
    if cleaned:
        clean_texts.append(cleaned)
```

## 딕셔너리·집합 컴프리헨션

```python
words = ["자연어", "처리", "Python"]
lengths = {word: len(word) for word in words}
first_chars = {word[0] for word in words}
```

## 반복 가능한 객체와 제너레이터

큰 파일은 모든 데이터를 한 번에 메모리에 올리지 않는 편이 좋습니다.

```python
lengths = (len(text) for text in raw_texts)
for length in lengths:
    print(length)
```

제너레이터는 한 번 소비하면 다시 사용하려면 새로 만들어야 합니다.

## 실습: 유효 문장 선별

```python
records = [
    {"id": 1, "text": " 좋아요 "},
    {"id": 2, "text": None},
    {"id": 3, "text": ""},
]

valid_records = []
for record in records:
    text = record.get("text")
    if text is None or not text.strip():
        continue
    valid_records.append({**record, "text": text.strip()})
```

원본 딕셔너리를 직접 수정하지 않고 새 딕셔너리를 만들어 변경의 영향을 통제했습니다.

> 다음: [함수와 모듈](05_Functions_and_Modules.md)
