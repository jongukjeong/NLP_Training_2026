from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "customer_inquiries.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_PATH = OUTPUT_DIR / "customer_inquiries_clean.csv"

ALLOWED_LABELS = {"positive", "negative", "neutral", "unknown"}
REQUIRED_COLUMNS = {"id", "text", "label"}


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """고객 문의 데이터의 결측값, 공백, 레이블과 중복을 정제한다."""
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError(f"필수 열이 없습니다: {sorted(missing_columns)}")

    cleaned = df.copy()
    cleaned = cleaned.dropna(subset=["text"]).copy()
    cleaned["text"] = (
        cleaned["text"]
        .astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    cleaned = cleaned.loc[cleaned["text"].str.len() > 0].copy()
    cleaned["label"] = (
        cleaned["label"]
        .fillna("unknown")
        .astype("string")
        .str.strip()
        .str.lower()
    )

    invalid_labels = sorted(set(cleaned["label"]) - ALLOWED_LABELS)
    if invalid_labels:
        raise ValueError(f"허용되지 않은 레이블: {invalid_labels}")

    cleaned = cleaned.drop_duplicates(subset=["text"], keep="first").copy()
    cleaned["text_length"] = cleaned["text"].str.len()
    return cleaned.reset_index(drop=True)


def main() -> None:
    original = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")
    cleaned = clean_dataframe(original)

    assert cleaned["text"].notna().all()
    assert cleaned["text"].str.len().gt(0).all()
    assert cleaned["text"].is_unique
    assert set(cleaned["label"]) <= ALLOWED_LABELS

    report = {
        "rows_before": len(original),
        "rows_after": len(cleaned),
        "rows_removed": len(original) - len(cleaned),
        "label_counts": cleaned["label"].value_counts().to_dict(),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print(cleaned.to_string(index=False))
    print("\n처리 보고서:", report)
    print("저장 경로:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
