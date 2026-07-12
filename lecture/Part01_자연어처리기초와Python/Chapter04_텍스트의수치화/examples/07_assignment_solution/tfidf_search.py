import json
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


def main() -> None:
    faq = pd.read_csv(BASE_DIR / "faq.csv", encoding="utf-8-sig")
    required = {"id", "question", "answer"}
    if missing := required - set(faq.columns):
        raise ValueError(f"필수 열이 없습니다: {sorted(missing)}")

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), token_pattern=r"(?u)\b\w+\b")
    matrix = vectorizer.fit_transform(faq["question"])
    query = "배송이 늦습니다"
    query_vector = vectorizer.transform([query])
    scores = cosine_similarity(query_vector, matrix).ravel()
    order = sorted(range(len(faq)), key=lambda i: (-scores[i], str(faq.iloc[i]["id"])))[:3]

    results = faq.iloc[order].copy()
    results.insert(0, "rank", range(1, len(results) + 1))
    results["score"] = [float(scores[i]) for i in order]
    report = {"vocabulary_size": len(vectorizer.vocabulary_), "matrix_shape": list(matrix.shape), "zero_scores": int((scores == 0).sum())}

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_DIR / "search_results.csv", index=False, encoding="utf-8-sig")
    (OUTPUT_DIR / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(results[["rank", "id", "score", "answer"]].to_string(index=False))


if __name__ == "__main__":
    main()
