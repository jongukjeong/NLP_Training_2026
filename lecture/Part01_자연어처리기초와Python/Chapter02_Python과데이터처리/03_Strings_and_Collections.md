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
