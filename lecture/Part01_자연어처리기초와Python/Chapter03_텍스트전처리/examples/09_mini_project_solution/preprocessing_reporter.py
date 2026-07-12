from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / "messages.csv"
DEFAULT_OUTPUT = BASE_DIR / "output" / "messages_clean.csv"
REQUIRED_COLUMNS = {"id", "text"}
PATTERNS = {
    "url": re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE),
    "email": re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    "phone": re.compile(r"(?<!\d)01[016789][ -]?\d{3,4}[ -]?\d{4}(?!\d)"),
}


def preprocess(text: str) -> tuple[str, dict[str, int]]:
    result = unicodedata.normalize("NFC", text).replace("\u200b", "").replace("\xa0", " ")
    counts = {}
    for name, replacement in (("url", "<URL>"), ("email", "<EMAIL>"), ("phone", "<PHONE>")):
        result, counts[name] = PATTERNS[name].subn(replacement, result)
    result = re.sub(r"\s+", " ", result).strip()
    return result, counts


def run(input_path: Path, output_path: Path) -> dict:
    if not input_path.is_file():
        raise FileNotFoundError(f"입력 파일을 찾을 수 없습니다: {input_path}")
    original = pd.read_csv(input_path, encoding="utf-8-sig")
    missing = REQUIRED_COLUMNS - set(original.columns)
    if missing:
        raise ValueError(f"필수 열이 없습니다: {sorted(missing)}")

    result = original.copy()
    result["text"] = result["text"].fillna("").astype("string")
    processed = result["text"].map(preprocess)
    result["clean_text"] = processed.map(lambda item: item[0])
    result["char_count_before"] = result["text"].str.len()
    result["char_count_after"] = result["clean_text"].str.len()
    result["token_count"] = result["clean_text"].str.split().str.len()

    mask_counts = {
        name: int(sum(item[1][name] for item in processed)) for name in PATTERNS
    }
    report = {
        "rows": len(result),
        "empty_results": int(result["clean_text"].eq("").sum()),
        "average_length_before": round(float(result["char_count_before"].mean()), 2),
        "average_length_after": round(float(result["char_count_after"].mean()), 2),
        "mask_counts": mask_counts,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False, encoding="utf-8-sig")
    output_path.with_suffix(".report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="텍스트 전처리와 품질 보고서를 생성합니다.")
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("output", nargs="?", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
