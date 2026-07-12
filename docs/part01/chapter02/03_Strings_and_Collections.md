# 03. 문자열과 컬렉션

## 문자열

문자열은 NLP에서 가장 자주 다루는 자료형이며 변경 불가능합니다.

```python
text = "  자연어 처리는 재미있다!  "
cleaned = text.strip()

print(cleaned.lower())
print(cleaned.replace("재미있다", "유용하다"))
print(cleaned.startswith("자연어"))
print(len(cleaned))
```

### 분할과 결합

```python
tokens = "자연어 처리는 재미있다".split()
sentence = " | ".join(tokens)
print(tokens)
print(sentence)
```

`split()`은 기본적으로 연속 공백을 하나의 구분으로 처리합니다. CSV처럼 따옴표와 쉼표 규칙이 있는 데이터는 직접 `split(",")`하지 말고 `csv` 모듈이나 pandas를 사용합니다.

### 슬라이싱

```python
word = "자연어처리"
print(word[:3])   # 자연어
print(word[3:])   # 처리
print(word[::-1]) # 역순
```

## 리스트

순서가 있고 변경 가능한 여러 값을 저장합니다.

```python
texts = ["배송이 빨라요", "가격이 비싸요"]
texts.append("품질이 좋아요")
texts.extend(["포장이 깔끔해요"])

for text in texts:
    print(text)
```

## 튜플

순서가 있지만 변경하지 않을 묶음에 적합합니다.

```python
label_pair = ("positive", 1)
label, value = label_pair
```

## 집합

중복 제거와 소속 검사가 빠릅니다. 순서를 보장하는 용도로 사용하지 않습니다.

```python
labels = ["positive", "negative", "positive"]
unique_labels = set(labels)
allowed = {"positive", "negative", "neutral"}
print(unique_labels)
print("unknown" in allowed)
```

입력 순서를 유지하며 중복을 제거하려면 다음 패턴을 사용할 수 있습니다.

```python
unique_in_order = list(dict.fromkeys(labels))
```

## 딕셔너리

키와 값으로 한 레코드나 빈도표를 표현합니다.

```python
review = {"id": 1, "text": "좋아요", "label": "positive"}
print(review["text"])
print(review.get("score", 0.0))

counts = {}
for label in labels:
    counts[label] = counts.get(label, 0) + 1
print(counts)
```

필수 키는 `record["text"]`로 접근해 누락을 즉시 발견하고, 선택 키는 `record.get("score")`로 접근하는 것이 의도를 잘 드러냅니다.

## 중첩 구조

```python
dataset = {
    "name": "reviews",
    "records": [
        {"id": 1, "text": "좋아요", "label": "positive"},
        {"id": 2, "text": "아쉬워요", "label": "negative"},
    ],
}

for record in dataset["records"]:
    print(record["id"], record["text"])
```

## 실습

1. 문장 다섯 개를 리스트에 저장합니다.
2. 각 문장의 앞뒤 공백을 제거합니다.
3. 레이블 목록의 고유값을 집합으로 구합니다.
4. 레이블별 개수를 딕셔너리로 계산합니다.

> 다음: [조건문·반복문·컴프리헨션](04_Control_Flow.md)
