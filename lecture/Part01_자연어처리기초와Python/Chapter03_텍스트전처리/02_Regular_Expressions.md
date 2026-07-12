# 02. 정규표현식 기반 정제

## 정규표현식의 역할

정규표현식은 문자 패턴을 탐색하고 치환하는 도구입니다. Python에서는 `re` 모듈을 사용합니다.

```python
import re

text = "문의: help@example.com, https://example.com"
emails = re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", text)
urls = re.findall(r"https?://\S+", text)
```

## 실무에서 자주 쓰는 패턴

```python
PATTERNS = {
    "url": re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE),
    "email": re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    "phone": re.compile(r"(?<!\d)01[016789][ -]?\d{3,4}[ -]?\d{4}(?!\d)"),
    "spaces": re.compile(r"\s+"),
}
```

```python
def mask_patterns(text: str) -> str:
    text = PATTERNS["url"].sub("<URL>", text)
    text = PATTERNS["email"].sub("<EMAIL>", text)
    text = PATTERNS["phone"].sub("<PHONE>", text)
    return PATTERNS["spaces"].sub(" ", text).strip()
```

## 탐욕적 패턴 주의

`.*`는 가능한 한 길게 일치합니다. HTML 태그를 단순 제거할 때도 예상보다 넓은 범위가 삭제될 수 있습니다.

```python
re.sub(r"<.*?>", " ", text)  # 최소 반복이지만 완전한 HTML 파서는 아님
```

HTML 구조가 중요하면 정규표현식보다 전용 파서를 사용합니다.

## 한글과 영문을 남기는 규칙

```python
cleaned = re.sub(r"[^가-힣A-Za-z0-9\s!?.,<>]", " ", text)
```

허용 문자 방식은 이모지와 다른 언어를 제거할 수 있습니다. 적용 전에 데이터 언어와 분석 목적을 확인합니다.

## 반복 문자 완화

```python
def reduce_repeats(text: str, limit: int = 2) -> str:
    return re.sub(r"(.)\1{" + str(limit) + r",}", r"\1" * limit, text)
```

`ㅋㅋㅋㅋ`를 `ㅋㅋ`로 줄이는 것이 감성 분류에 도움이 될 수 있지만 반복 횟수 자체가 신호라면 원본 특징을 별도로 보존합니다.

## 테스트 사례

| 입력 | 기대 결과 |
|---|---|
| `https://a.com 확인` | `<URL> 확인` |
| `help@example.com` | `<EMAIL>` |
| `010-1234-5678` | `<PHONE>` |
| `정말    좋아요` | `정말 좋아요` |

> 다음: [Unicode와 텍스트 정규화](03_Normalization.md)
