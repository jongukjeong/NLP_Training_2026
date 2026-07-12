# 05. 함수와 모듈

## 함수가 필요한 이유

함수는 처리 규칙에 이름을 붙이고, 입력과 출력을 명확히 하며, 반복 테스트를 가능하게 합니다.

```python
def normalize_text(text: str) -> str:
    """문장의 앞뒤 공백을 제거하고 내부 연속 공백을 하나로 줄인다."""
    return " ".join(text.split())

print(normalize_text("  배송이   빨라요 "))
```

타입 힌트는 실행을 강제하지 않지만 함수 사용법을 문서화하고 도구의 오류 탐지를 돕습니다.

## 매개변수와 반환값

```python
def is_valid_text(text: str | None, min_length: int = 2) -> bool:
    if text is None:
        return False
    return len(text.strip()) >= min_length
```

기본값은 변경 불가능한 값을 사용합니다. 리스트를 기본값으로 두면 호출 간 상태가 공유될 수 있습니다.

```python
def add_text(text: str, bucket: list[str] | None = None) -> list[str]:
    if bucket is None:
        bucket = []
    bucket.append(text)
    return bucket
```

## 한 가지 책임

읽기, 정제, 통계, 저장을 한 함수에 모두 넣지 않습니다.

```python
def clean_records(records: list[dict]) -> list[dict]:
    cleaned_records = []
    for record in records:
        text = record.get("text")
        if not is_valid_text(text):
            continue
        cleaned_records.append({**record, "text": normalize_text(text)})
    return cleaned_records
```

## 예외 처리

```python
def parse_score(value: str) -> float:
    try:
        score = float(value)
    except ValueError as error:
        raise ValueError(f"점수는 숫자여야 합니다: {value!r}") from error

    if not 0 <= score <= 1:
        raise ValueError(f"점수 범위는 0~1입니다: {score}")
    return score
```

예외는 오류를 없애는 장치가 아니라 적절한 계층에서 의미 있는 정보로 바꾸는 장치입니다.

## 모듈과 진입점

`text_utils.py`에 함수를 두면 다른 파일에서 가져올 수 있습니다.

```python
from text_utils import normalize_text
```

직접 실행할 때만 동작할 코드는 진입점 아래에 둡니다.

```python
def main() -> None:
    print(normalize_text("  자연어   처리  "))


if __name__ == "__main__":
    main()
```

## 간단한 검증

```python
assert normalize_text(" a   b ") == "a b"
assert is_valid_text(None) is False
assert is_valid_text("가") is False
```

`assert`는 학습용 빠른 확인에 유용합니다. 실제 입력 검증은 명시적 조건문과 예외를 사용합니다.

> 다음: [파일·CSV·JSON 처리](06_File_IO.md)
