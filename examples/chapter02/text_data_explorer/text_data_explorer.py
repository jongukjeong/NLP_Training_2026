from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / "reviews.csv"
DEFAULT_OUTPUT = BASE_DIR / "output" / "reviews_clean.csv"
REQUIRED_COLUMNS = {"id", "text", "label"}
ALLOWED_LABELS = {"positive", "negative", "neutral", "unknown"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="텍스트 CSV를 정제하고 요약합니다.")
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def validate_columns(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"필수 열이 없습니다: {', '.join(sorted(missing))}")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    validate_columns(df)
    result = df.copy()
    result = result.dropna(subset=["text"]).copy()
    result["text"] = (
        result["text"]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    result = result.loc[result["text"].str.len() > 0].copy()
    result["label"] = (
        result["label"]
        .fillna("unknown")
        .astype("string")
        .str.lower()
        .str.strip()
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
    cleaned, report = run(args.input, args.output)
    print(cleaned.to_string(index=False))
    print("\n" + json.dumps(report, ensure_ascii=False, indent=2))
    print("\n저장 경로:", args.output)


if __name__ == "__main__":
    main()
