from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import pandas as pd
from scipy.sparse import lil_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


def main() -> None:
    parser = argparse.ArgumentParser(description="도메인 말뭉치의 유사 단어를 검색합니다.")
    parser.add_argument("word", nargs="?", default="배송")
    parser.add_argument("--window", type=int, default=2)
    parser.add_argument("--dimensions", type=int, default=5)
    parser.add_argument("--min-count", type=int, default=1)
    args = parser.parse_args()

    sentences = [line.split() for line in (BASE_DIR / "support_corpus.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
    counts = Counter(token for sentence in sentences for token in sentence)
    vocabulary = sorted(word for word, count in counts.items() if count >= args.min_count)
    index = {word: i for i, word in enumerate(vocabulary)}
    if args.word not in index:
        raise ValueError(f"어휘에 없는 단어입니다: {args.word}")

    matrix = lil_matrix((len(vocabulary), len(vocabulary)), dtype=float)
    for sentence in sentences:
        filtered = [word for word in sentence if word in index]
        for center, word in enumerate(filtered):
            start, end = max(0, center - args.window), min(len(filtered), center + args.window + 1)
            for position in range(start, end):
                if position != center:
                    matrix[index[word], index[filtered[position]]] += 1

    dimensions = min(args.dimensions, len(vocabulary) - 1)
    model = TruncatedSVD(n_components=dimensions, random_state=42)
    embedding = model.fit_transform(matrix.tocsr())
    scores = cosine_similarity(embedding[index[args.word]].reshape(1, -1), embedding).ravel()
    order = [i for i in scores.argsort()[::-1] if vocabulary[i] != args.word][:10]
    results = pd.DataFrame({"rank": range(1, len(order) + 1), "word": [vocabulary[i] for i in order], "score": [float(scores[i]) for i in order]})
    report = {"query": args.word, "window": args.window, "dimensions": dimensions, "min_count": args.min_count, "vocabulary_size": len(vocabulary), "explained_variance_ratio": float(model.explained_variance_ratio_.sum())}

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_DIR / "similar_words.csv", index=False, encoding="utf-8-sig")
    (OUTPUT_DIR / "model_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()
