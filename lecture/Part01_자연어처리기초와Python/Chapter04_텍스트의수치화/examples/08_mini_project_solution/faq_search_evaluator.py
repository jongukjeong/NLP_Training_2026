import json
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


def main() -> None:
    faq = pd.read_csv(BASE_DIR / "faq.csv", encoding="utf-8-sig")
    evaluation = pd.read_csv(BASE_DIR / "evaluation.csv", encoding="utf-8-sig")
    if missing := {"id", "question", "answer"} - set(faq.columns):
        raise ValueError(f"FAQ 필수 열 누락: {sorted(missing)}")
    if missing := {"query", "relevant_id"} - set(evaluation.columns):
        raise ValueError(f"평가 필수 열 누락: {sorted(missing)}")

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), token_pattern=r"(?u)\b\w+\b", sublinear_tf=True)
    matrix = vectorizer.fit_transform(faq["question"])
    rows, reciprocal_ranks = [], []
    hits1 = hits3 = 0

    for item in evaluation.itertuples(index=False):
        query_vector = vectorizer.transform([item.query])
        scores = cosine_similarity(query_vector, matrix).ravel()
        order = sorted(range(len(faq)), key=lambda i: (-scores[i], str(faq.iloc[i]["id"])))
        ranked_ids = [str(faq.iloc[i]["id"]) for i in order]
        rank = ranked_ids.index(str(item.relevant_id)) + 1
        hits1 += rank <= 1
        hits3 += rank <= 3
        reciprocal_ranks.append(1 / rank)
        rows.append({"query": item.query, "relevant_id": item.relevant_id, "rank": rank, "top_id": ranked_ids[0], "top_score": float(scores[order[0]])})

    count = len(evaluation)
    report = {"queries": count, "hit_at_1": hits1 / count, "hit_at_3": hits3 / count, "mrr": sum(reciprocal_ranks) / count, "vocabulary_size": len(vectorizer.vocabulary_)}
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUTPUT_DIR / "evaluation_results.csv", index=False, encoding="utf-8-sig")
    (OUTPUT_DIR / "metrics.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
