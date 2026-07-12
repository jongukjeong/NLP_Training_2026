import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "reviews_raw.csv"
OUTPUT_DIR = BASE_DIR / "output"

URL = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"(?<!\d)01[016789][ -]?\d{3,4}[ -]?\d{4}(?!\d)")
SPACES = re.compile(r"\s+")


def preprocess(text: str) -> str:
    text = unicodedata.normalize("NFC", text).replace("\u200b", "")
    text = URL.sub("<URL>", text)
    text = EMAIL.sub("<EMAIL>", text)
    text = PHONE.sub("<PHONE>", text)
    return SPACES.sub(" ", text).strip()


def main() -> None:
    original = pd.read_csv(INPUT_PATH, encoding="utf-8-sig")
    if "text" not in original.columns:
        raise ValueError("필수 열이 없습니다: text")
    if original["text"].isna().any():
        raise ValueError("text 열에 결측값이 있습니다.")

    result = original.copy()
    result["clean_text"] = result["text"].astype("string").map(preprocess)
    result["token_count"] = result["clean_text"].str.split().str.len()
    assert result["clean_text"].str.len().gt(0).all()

    report = {
        "rows": len(result),
        "url_masks": int(result["clean_text"].str.count(r"<URL>").sum()),
        "email_masks": int(result["clean_text"].str.count(r"<EMAIL>").sum()),
        "phone_masks": int(result["clean_text"].str.count(r"<PHONE>").sum()),
        "average_tokens": round(float(result["token_count"].mean()), 2),
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_DIR / "reviews_clean.csv", index=False, encoding="utf-8-sig")
    (OUTPUT_DIR / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
