import json
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.sparse import lil_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"


def main() -> None:
    sentences = [line.split() for line in (BASE_DIR / "sentences.txt").read_text(encoding="utf-8").splitlines() if line.strip()]
    counts = Counter(token for sentence in sentences for token in sentence)
    vocabulary = sorted(counts)
    index = {word: i for i, word in enumerate(vocabulary)}
    matrix = lil_matrix((len(vocabulary), len(vocabulary)), dtype=float)
    window = 2
    for sentence in sentences:
        for center, word in enumerate(sentence):
            for position in range(max(0, center - window), min(len(sentence), center + window + 1)):
                if position != center:
                    matrix[index[word], index[sentence[position]]] += 1

    dimensions = min(4, len(vocabulary) - 1)
    embedding = TruncatedSVD(n_components=dimensions, random_state=42).fit_transform(matrix.tocsr())
    query = "배송"
    scores = cosine_similarity(embedding[index[query]].reshape(1, -1), embedding).ravel()
    order = [i for i in scores.argsort()[::-1] if vocabulary[i] != query][:5]
    neighbors = [{"word": vocabulary[i], "score": float(scores[i])} for i in order]
    report = {"query": query, "vocabulary_size": len(vocabulary), "dimensions": dimensions, "neighbors": neighbors}
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "neighbors.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
