# 03. Unicode와 텍스트 정규화

## 눈에는 같지만 다른 문자

Unicode에서는 화면상 비슷한 문자가 서로 다른 코드 포인트 조합일 수 있습니다. 그대로 비교하면 중복 탐지와 검색이 실패할 수 있습니다.

```python
import unicodedata

normalized = unicodedata.normalize("NFC", text)
```

## NFC와 NFKC

| 방식 | 특징 | 권장 용도 |
|---|---|---|
| NFC | 표준적으로 결합 가능한 문자를 결합 | 일반 한국어 원문 보존 |
| NFKC | 호환 문자를 더 적극적으로 통합 | 검색 키·식별자 정규화 |

NFKC는 전각 문자 등을 통합하지만 표현 차이를 잃을 수 있으므로 원본 열은 보존합니다.

## 공백과 제어 문자

```python
import re
import unicodedata

def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\u200b", "")  # zero-width space
    text = text.replace("\xa0", " ")  # non-breaking space
    return re.sub(r"\s+", " ", text).strip()
```

## 대소문자와 숫자

영문 검색에서는 `casefold()`가 `lower()`보다 폭넓은 비교 정규화를 제공합니다. 반면 고유명사 표기나 개체명 인식에서는 대소문자를 보존해야 할 수 있습니다.

숫자를 모두 `<NUM>`으로 바꾸면 희소성은 줄지만 날짜·버전·가격 정보가 사라집니다. 목적별로 날짜, 금액, 일반 숫자를 구분해 마스킹할 수 있습니다.

## 문장부호 정책

- 감성 분석: `!`, `?`, 반복 횟수가 신호일 수 있음
- 검색: 문장부호 차이를 줄이는 편이 유리할 수 있음
- 개체명 인식: 하이픈과 점이 제품명·주소의 일부일 수 있음
- 생성 모델 학습: 원문의 문장 구조를 가능한 보존

## 정규화 기록

전처리 설정에 다음을 남깁니다.

```json
{
  "unicode_form": "NFC",
  "collapse_whitespace": true,
  "mask_url": true,
  "mask_email": true,
  "lowercase_english": false
}
```
