# 12. 미니 프로젝트: 텍스트 데이터 탐색기

## 프로젝트 목표

CSV 파일을 읽어 품질을 진단하고 텍스트를 정제한 뒤, 정제 데이터와 처리 보고서를 저장하는 작은 프로그램을 설계합니다. 이 문서는 구현 명세와 완성 예제를 함께 제공합니다.

## 입력 명세

`reviews.csv`는 다음 열을 가집니다.

| 열 | 필수 | 설명 |
|---|---|---|
| `id` | 예 | 레코드 식별자 |
| `text` | 예 | 리뷰 문장 |
| `label` | 예 | `positive`, `negative`, `neutral`, `unknown` |

예시:

```csv
id,text,label
1,배송이 빨라요,positive
2,  환불하고 싶어요  ,negative
3,,unknown
4,배송이 빨라요,positive
```

## 권장 폴더 구조

예제 코드와 입력 데이터셋은 동일한 폴더에 둡니다. 실행 결과만 `output/`으로 분리합니다.

```text
examples/chapter02/text_data_explorer/
├── text_data_explorer.py
├── reviews.csv
└── output/                 # 실행 시 생성
    ├── reviews_clean.csv
    └── reviews_clean.report.json
```

## 기능 요구사항

1. 명령행에서 입력·출력 경로를 받습니다.
2. 파일 존재 여부와 필수 열을 검사합니다.
3. UTF-8/BOM CSV를 읽습니다.
4. 결측·빈 문장을 제거합니다.
5. 문장 공백과 레이블 표기를 정규화합니다.
6. 허용하지 않은 레이블이면 명확한 오류를 냅니다.
7. 정규화된 문장 기준 중복을 제거합니다.
8. 문장 길이와 레이블 분포를 계산합니다.
9. 정제 CSV와 JSON 보고서를 별도 저장합니다.
10. 원본 파일은 변경하지 않습니다.

## 처리 설계

```text
CLI 인수
  → 경로 검사
  → CSV 읽기
  → 스키마 검사
  → 정제
  → 결과 검증
  → CSV 저장
  → JSON 보고서 저장
```

## 완성 예제

아래 코드를 `text_data_explorer.py`로 저장하면 실행할 수 있습니다. 이번 작업에서는 문서만 작성하므로 코드는 별도 파일로 생성하지 않습니다.

```python
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {"id", "text", "label"}
ALLOWED_LABELS = {"positive", "negative", "neutral", "unknown"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="텍스트 CSV를 정제하고 요약합니다.")
    parser.add_argument("input", type=Path, help="입력 CSV 경로")
    parser.add_argument("output", type=Path, help="정제 CSV 경로")
    return parser.parse_args()


def validate_columns(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"필수 열이 없습니다: {', '.join(sorted(missing))}")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df)
    result = df.copy()
    result = result.dropna(subset=["text"])
    result["text"] = (
        result["text"]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    result = result.loc[result["text"].str.len() > 0].copy()
    result["label"] = (
        result["label"].fillna("unknown").astype("string").str.lower().str.strip()
    )

    invalid_labels = sorted(set(result["label"]) - ALLOWED_LABELS)
    if invalid_labels:
        raise ValueError(f"허용되지 않은 레이블: {invalid_labels}")

    result = result.drop_duplicates(subset=["text"], keep="first").copy()
    result["text_length"] = result["text"].str.len()
    return result.reset_index(drop=True)


def build_report(before: pd.DataFrame, after: pd.DataFrame) -> dict:
    return {
        "rows_before": len(before),
        "rows_after": len(after),
        "rows_removed": len(before) - len(after),
        "missing_text_before": int(before["text"].isna().sum()),
        "average_text_length": (
            round(float(after["text_length"].mean()), 2) if not after.empty else 0.0
        ),
        "label_counts": {
            str(key): int(value)
            for key, value in after["label"].value_counts().items()
        },
    }


def run(input_path: Path, output_path: Path) -> tuple[pd.DataFrame, dict]:
    if not input_path.is_file():
        raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {input_path}")

    original = pd.read_csv(input_path, encoding="utf-8-sig")
    cleaned = clean_dataframe(original)

    assert cleaned["text"].notna().all()
    assert cleaned["text"].str.len().gt(0).all()
    assert cleaned["text"].is_unique
    assert set(cleaned["label"]) <= ALLOWED_LABELS

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_path, index=False, encoding="utf-8-sig")

    report = build_report(original, cleaned)
    report_path = output_path.with_suffix(".report.json")
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return cleaned, report


def main() -> None:
    args = parse_args()
    _, report = run(args.input, args.output)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

## 실행 예시

```powershell
cd examples\chapter02\text_data_explorer
python text_data_explorer.py reviews.csv output\reviews_clean.csv
```

예상 보고서:

```json
{
  "rows_before": 4,
  "rows_after": 2,
  "rows_removed": 2,
  "missing_text_before": 1,
  "average_text_length": 8.5,
  "label_counts": {
    "positive": 1,
    "negative": 1
  }
}
```

## 테스트 시나리오

| 번호 | 입력 | 기대 결과 |
|---|---|---|
| 1 | 정상 CSV | 정제 CSV와 보고서 생성 |
| 2 | 파일 없음 | 경로를 포함한 오류 |
| 3 | `text` 열 없음 | 누락 열을 포함한 오류 |
| 4 | 결측·공백 문장 | 해당 행 제거 |
| 5 | 공백만 다른 중복 | 하나만 유지 |
| 6 | 잘못된 레이블 | 잘못된 값을 포함한 오류 |
| 7 | 유효 행 0개 | 빈 CSV와 평균 0 보고서 |

## 확장 아이디어

- 입력 형식에 JSON 추가
- 최소·최대 문장 길이를 명령행 옵션으로 제공
- 제외된 행과 제외 사유를 별도 파일로 저장
- 정제 규칙별 제거 건수를 단계별로 기록
- 단위 테스트와 자동화된 품질 검사 추가

## 완료 체크리스트

- [ ] 원본과 출력 경로가 분리되어 있다.
- [ ] 예제 코드와 입력 데이터셋이 같은 예제 폴더에 있다.
- [ ] 필수 열과 허용 레이블을 검사한다.
- [ ] 결측·공백·중복 처리 순서가 명확하다.
- [ ] 정제 결과를 단언문 또는 테스트로 검증한다.
- [ ] 처리 전후 통계를 JSON으로 남긴다.
- [ ] 오류 메시지만 보고도 사용자가 수정 방향을 알 수 있다.

Chapter 2를 마쳤습니다. 다음 장에서는 이 데이터를 정규표현식, 토큰화, 형태소 분석 등 NLP 전처리 기법에 연결합니다.
