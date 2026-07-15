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
