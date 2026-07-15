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
